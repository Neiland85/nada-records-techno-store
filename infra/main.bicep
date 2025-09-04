param environmentName string
param location string = 'eastus'
param resourceGroupName string
param resourceToken string = uniqueString(subscription().id, resourceGroup().id, location, environmentName)
param resourcePrefix string = 'nts'
param databaseAdminLogin string
@secure()
param databaseAdminPassword string
param stripeSecretKey string
param stripePublishableKey string

targetScope = 'resourceGroup'

// User-assigned Managed Identity
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'az-${resourcePrefix}-mi-${resourceToken}'
  location: location
}

// Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'az-${resourcePrefix}-kv-${resourceToken}'
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
  }
}

// Role assignment for MI on Key Vault (Key Vault Secrets Officer)
resource keyVaultRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().id, resourceGroup().id, managedIdentity.id, '00482a5a-887f-4fb3-b363-3b7fe8e74483')
  scope: keyVault
  properties: {
    principalId: managedIdentity.properties.principalId
    roleDefinitionId: '/providers/Microsoft.Authorization/roleDefinitions/00482a5a-887f-4fb3-b363-3b7fe8e74483'
    principalType: 'ServicePrincipal'
  }
}

// Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2020-08-01' = {
  name: 'az-${resourcePrefix}-la-${resourceToken}'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
  }
}

// Application Insights
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'az-${resourcePrefix}-ai-${resourceToken}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

// PostgreSQL Flexible Server
resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: 'az-${resourcePrefix}-pg-${resourceToken}'
  location: location
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: databaseAdminLogin
    administratorLoginPassword: databaseAdminPassword
    version: '15'
    storage: {
      storageSizeGB: 32
    }
    backup: {
      backupRetentionDays: 7
    }
  }
}

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'az${resourcePrefix}st${resourceToken}'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
  }
}

// Redis Cache
resource redisCache 'Microsoft.Cache/redis@2023-04-01' = {
  name: 'az-${resourcePrefix}-redis-${resourceToken}'
  location: location
  properties: {
    sku: {
      name: 'Basic'
      family: 'C'
      capacity: 0
    }
    enableNonSslPort: false
  }
}

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: 'az-${resourcePrefix}-asp-${resourceToken}'
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  properties: {
    reserved: true
  }
}

// App Service for backend
resource appService 'Microsoft.Web/sites@2022-03-01' = {
  name: 'az-${resourcePrefix}-as-${resourceToken}'
  location: location
  kind: 'app'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      cors: {
        allowedOrigins: ['*']
      }
      appSettings: [
        {
          name: 'AZURE_ENV_NAME'
          value: environmentName
        }
        {
          name: 'DATABASE_URL'
          value: 'postgresql://${databaseAdminLogin}:${databaseAdminPassword}@${postgresServer.properties.fullyQualifiedDomainName}/postgres?sslmode=require'
        }
        {
          name: 'REDIS_URL'
          value: 'rediss://:${redisCache.listKeys().primaryKey}@${redisCache.properties.hostName}:${redisCache.properties.sslPort}'
        }
        {
          name: 'AZURE_STORAGE_CONNECTION_STRING'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net'
        }
        {
          name: 'STRIPE_SECRET_KEY'
          value: stripeSecretKey
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
      ]
    }
    identity: {
      type: 'UserAssigned'
      userAssignedIdentities: {
        '${managedIdentity.id}': {}
      }
    }
  }
  tags: {
    'azd-service-name': 'backend'
  }
}

// Diagnostic settings for App Service
resource appServiceDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'az-${resourcePrefix}-as-diag-${resourceToken}'
  scope: appService
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      {
        category: 'AppServiceHTTPLogs'
        enabled: true
      }
      {
        category: 'AppServiceConsoleLogs'
        enabled: true
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
      }
    ]
  }
}

// Static Web App for frontend
resource staticWebApp 'Microsoft.Web/staticSites@2022-09-01' = {
  name: 'az-${resourcePrefix}-swa-${resourceToken}'
  location: location
  sku: {
    name: 'Free'
    tier: 'Free'
  }
  properties: {
    repositoryUrl: 'https://github.com/Neiland85/nada-records-techno-store'
    branch: 'main'
    buildProperties: {
      appLocation: 'frontend'
      apiLocation: 'backend'
      outputLocation: 'out'
    }
    templateProperties: {
      isPrivate: false
    }
  }
  tags: {
    'azd-service-name': 'frontend'
  }
}

// Outputs
output RESOURCE_GROUP_ID string = resourceGroup().id
output BACKEND_URL string = 'https://${appService.properties.defaultHostName}'
output FRONTEND_URL string = 'https://${staticWebApp.properties.defaultHostname}'
output DATABASE_URL string = 'postgresql://${databaseAdminLogin}:${databaseAdminPassword}@${postgresServer.properties.fullyQualifiedDomainName}/postgres?sslmode=require'
output REDIS_URL string = 'rediss://:${redisCache.listKeys().primaryKey}@${redisCache.properties.hostName}:${redisCache.properties.sslPort}'
output AZURE_STORAGE_CONNECTION_STRING string = 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net'

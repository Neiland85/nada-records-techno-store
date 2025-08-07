# 🎵 Nada Records Techno Store

**EN:** Full-stack music store platform with audio streaming, multi-format downloads (WAV/MP3/FLAC), automated distribution services, and integrated payment processing. Built with FastAPI + Next.js.

**ES:** Plataforma de tienda musical completa con streaming de audio, descargas multi-formato (WAV/MP3/FLAC), servicios de distribución automatized y procesamiento de pagos integrado. Construida con FastAPI + Next.js.

## 🚀 Quick Start

### Prerequisites

- Node.js >= 18.0.0
- Python >= 3.8
- Docker & Docker Compose
- npm >= 8.0.0

### Installation

```bash
# Clone the repository
git clone https://github.com/Neiland85/nada-records-techno-store.git
cd nada-records-techno-store

# Setup development environment
npm run setup:dev
```

### Development

```bash
# Start all services (database, redis, minio, etc.)
npm run dev:services

# Start backend and frontend
npm run dev
```

## 📦 Deployment

### Vercel Deployment Strategy

This project is configured for automatic deployment on Vercel with branch-based environments:

#### 🌟 Production Environment

- **Branch:** `main`
- **URL:** <https://nada-records-techno-store.vercel.app>
- **Trigger:** Automatic on push to `main`

#### 🧪 Staging Environment  

- **Branch:** `develop`
- **URL:** <https://nada-records-techno-store-git-develop.vercel.app>
- **Trigger:** Automatic on push to `develop`

#### 🔧 Feature Environments

- **Branches:** `feature/*`
- **URL:** <https://nada-records-techno-store-git-[branch-name].vercel.app>
- **Trigger:** Automatic on push to feature branches

### Configure Vercel Deployment

Run the configuration script to set up branch-based deployments:

```bash
./scripts/configure-vercel-deployment.sh
```

Or manually configure in [Vercel Dashboard](https://vercel.com/dashboard):

1. Go to Settings > Git
2. Enable "Deploy all branches"
3. Set Production Branch to `main`
4. Configure environment variables per branch

## 🛠️ Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database
- **Redis** - Caching and sessions
- **MinIO** - File storage
- **SendGrid** - Email service
- **Asyncio** - Async processing

### Frontend

- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Vercel** - Deployment platform

### Development Tools

- **Docker Compose** - Local development
- **GitGuardian** - Security scanning
- **Concurrent** - Process management
- **Pre-commit hooks** - Code quality

## 📁 Project Structure

```
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core functionality
│   │   └── models/      # Database models
│   └── requirements.txt
├── frontend/            # Next.js frontend
├── scripts/             # Automation scripts
├── docker-compose.yml   # Development services
├── vercel.json         # Vercel configuration
└── package.json        # Root package configuration
```

## 🔧 Available Scripts

### Development Scripts

```bash
npm run dev              # Start backend + frontend
npm run dev:backend      # Start only backend
npm run dev:frontend     # Start only frontend
npm run dev:services     # Start docker services
npm run dev:full         # Start services + application
```

### Build & Test

```bash
npm run build            # Build frontend
npm run test             # Run all tests
npm run test:backend     # Run backend tests
npm run test:frontend    # Run frontend tests
npm run test:e2e         # Run E2E tests
```

### Database

```bash
npm run db:init          # Initialize database
npm run db:migrate       # Run migrations
npm run db:seed          # Seed test data
npm run db:reset         # Reset database
```

### Code Quality

```bash
npm run lint             # Lint all code
npm run lint:fix         # Fix linting issues
npm run format           # Format code
npm run types:check      # Check TypeScript
```

### Security

```bash
npm run security:scan    # Security audit
npm run security:fix     # Fix security issues
```

## 🌍 Environment Variables

### Backend (.env.docker)

```bash
# Database
POSTGRES_USER=nada_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=nada_records

# Redis
REDIS_URL=redis://redis:6379

# Email
SENDGRID_API_KEY=your_sendgrid_key
SENDGRID_FROM_EMAIL=noreply@nada-records.com

# MinIO (File Storage)
MINIO_ACCESS_KEY=your_minio_key
MINIO_SECRET_KEY=your_minio_secret
```

### Frontend (Vercel Environment Variables)

Configure in Vercel Dashboard per environment:

**Production (main branch):**

```bash
NEXT_PUBLIC_API_URL=https://api.nada-records.com
NEXT_PUBLIC_APP_ENV=production
```

**Staging (develop branch):**

```bash
NEXT_PUBLIC_API_URL=https://api-staging.nada-records.com
NEXT_PUBLIC_APP_ENV=staging
```

**Development (feature branches):**

```bash
NEXT_PUBLIC_API_URL=https://api-dev.nada-records.com
NEXT_PUBLIC_APP_ENV=development
```

## 🔒 Security

- All sensitive data uses environment variables
- GitGuardian integration for secret scanning
- CORS configuration for API security
- Security headers in Vercel deployment
- Docker secrets management

## 📊 Monitoring & Health

```bash
# Health checks
npm run health           # Backend health
npm run health:services  # Docker services health

# Logs
npm run logs            # All service logs
npm run logs:postgres   # Database logs
npm run logs:redis      # Redis logs
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Branch Strategy

- `main` - Production code
- `develop` - Integration branch
- `feature/*` - New features
- `hotfix/*` - Critical fixes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/Neiland85/nada-records-techno-store/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Neiland85/nada-records-techno-store/discussions)
- **Email:** <support@nada-records.com>

---

**Nada Records** - Electronic Music Distribution Platform

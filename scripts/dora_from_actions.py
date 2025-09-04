#!/usr/bin/env python3
"""
DORA Metrics from GitHub Actions
Calculates Lead Time and Deployment Frequency from GitHub Actions data
"""

import os
import json
import requests
import argparse
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional

def get_github_token():
    """Get GitHub token from environment."""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("⚠️  GITHUB_TOKEN environment variable not set")
        print("💡 Generate token at: https://github.com/settings/tokens")
        print("💡 Permissions needed: repo, actions:read")
    return token

def get_repo_info():
    """Extract repository info from git remote."""
    try:
        import subprocess
        remote_url = subprocess.check_output(
            ['git', 'config', '--get', 'remote.origin.url'], 
            text=True
        ).strip()
        
        # Parse GitHub URL
        if 'github.com' in remote_url:
            if remote_url.startswith('https://'):
                parts = remote_url.replace('https://github.com/', '').replace('.git', '').split('/')
            elif remote_url.startswith('git@'):
                parts = remote_url.replace('git@github.com:', '').replace('.git', '').split('/')
            
            if len(parts) >= 2:
                return parts[0], parts[1]  # owner, repo
    except:
        pass
    
    print("❌ Could not determine GitHub repository info")
    print("💡 Ensure you're in a git repository with GitHub remote")
    return None, None

def fetch_workflow_runs(owner: str, repo: str, token: str, days: int = 30) -> List[Dict]:
    """Fetch workflow runs from GitHub API."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs'
    params = {
        'created': f'>={since}',
        'per_page': 100,
        'status': 'completed'
    }
    
    all_runs = []
    page = 1
    
    while True:
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"❌ GitHub API error: {response.status_code}")
            print(f"   Response: {response.text}")
            break
        
        data = response.json()
        runs = data.get('workflow_runs', [])
        
        if not runs:
            break
            
        all_runs.extend(runs)
        
        # Check if we have more pages
        if len(runs) < 100:
            break
            
        page += 1
    
    return all_runs

def analyze_deployment_workflows(runs: List[Dict]) -> Dict[str, Any]:
    """Analyze deployment-related workflows."""
    deployment_keywords = [
        'deploy', 'deployment', 'release', 'production', 
        'staging', 'build', 'publish', 'cd', 'delivery'
    ]
    
    deployment_runs = []
    
    for run in runs:
        workflow_name = run.get('name', '').lower()
        if any(keyword in workflow_name for keyword in deployment_keywords):
            deployment_runs.append(run)
    
    # Calculate deployment frequency
    if not deployment_runs:
        return {
            'deployment_frequency_weekly': 0,
            'successful_deployments': 0,
            'failed_deployments': 0,
            'deployment_success_rate': 0,
            'workflows_analyzed': len(runs)
        }
    
    # Group by week
    weeks = {}
    successful = 0
    failed = 0
    
    for run in deployment_runs:
        created_at = datetime.fromisoformat(run['created_at'].replace('Z', '+00:00'))
        week_key = created_at.strftime('%Y-W%U')
        
        if week_key not in weeks:
            weeks[week_key] = 0
        weeks[week_key] += 1
        
        if run['conclusion'] == 'success':
            successful += 1
        else:
            failed += 1
    
    avg_deployments_per_week = sum(weeks.values()) / len(weeks) if weeks else 0
    success_rate = (successful / len(deployment_runs)) * 100 if deployment_runs else 0
    
    return {
        'deployment_frequency_weekly': round(avg_deployments_per_week, 2),
        'successful_deployments': successful,
        'failed_deployments': failed,
        'deployment_success_rate': round(success_rate, 2),
        'weeks_analyzed': len(weeks),
        'workflows_analyzed': len(runs)
    }

def calculate_lead_time(runs: List[Dict]) -> Dict[str, Any]:
    """Calculate lead time metrics from workflow runs."""
    if not runs:
        return {'avg_lead_time_minutes': 0, 'median_lead_time_minutes': 0}
    
    lead_times = []
    
    for run in runs:
        created_at = datetime.fromisoformat(run['created_at'].replace('Z', '+00:00'))
        updated_at = datetime.fromisoformat(run['updated_at'].replace('Z', '+00:00'))
        
        duration = (updated_at - created_at).total_seconds() / 60  # minutes
        if duration > 0:  # Valid duration
            lead_times.append(duration)
    
    if not lead_times:
        return {'avg_lead_time_minutes': 0, 'median_lead_time_minutes': 0}
    
    avg_lead_time = sum(lead_times) / len(lead_times)
    median_lead_time = sorted(lead_times)[len(lead_times) // 2]
    
    return {
        'avg_lead_time_minutes': round(avg_lead_time, 2),
        'median_lead_time_minutes': round(median_lead_time, 2),
        'avg_lead_time_hours': round(avg_lead_time / 60, 2),
        'median_lead_time_hours': round(median_lead_time / 60, 2)
    }

def get_dora_classification(deployment_freq: float, lead_time_hours: float, 
                           success_rate: float) -> Dict[str, str]:
    """Classify performance according to DORA research."""
    
    # Deployment Frequency Classification
    if deployment_freq >= 7:  # Multiple times per week
        deploy_class = "🚀 Elite"
    elif deployment_freq >= 1:  # Weekly
        deploy_class = "🏆 High"
    elif deployment_freq >= 0.25:  # Monthly
        deploy_class = "📈 Medium"
    else:
        deploy_class = "📉 Low"
    
    # Lead Time Classification
    if lead_time_hours <= 1:  # Less than 1 hour
        lead_class = "🚀 Elite"
    elif lead_time_hours <= 24:  # Less than 1 day
        lead_class = "🏆 High"
    elif lead_time_hours <= 168:  # Less than 1 week
        lead_class = "📈 Medium"
    else:
        lead_class = "📉 Low"
    
    # Success Rate Classification
    if success_rate >= 95:
        success_class = "🚀 Elite"
    elif success_rate >= 85:
        success_class = "🏆 High"
    elif success_rate >= 70:
        success_class = "📈 Medium"
    else:
        success_class = "📉 Low"
    
    # Overall Classification
    classes = [deploy_class, lead_class, success_class]
    if all("🚀" in c for c in classes):
        overall = "🚀 Elite Performer"
    elif any("🚀" in c for c in classes) and all("📉" not in c for c in classes):
        overall = "🏆 High Performer"
    elif all("📉" not in c for c in classes):
        overall = "📈 Medium Performer"
    else:
        overall = "📉 Low Performer"
    
    return {
        'deployment_frequency': deploy_class,
        'lead_time': lead_class,
        'success_rate': success_class,
        'overall': overall
    }

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Generate DORA metrics from GitHub Actions')
    parser.add_argument('--days', type=int, default=30, help='Analysis window in days')
    parser.add_argument('--out', default='dora_metrics.json', help='Output JSON file')
    parser.add_argument('--owner', help='GitHub repository owner (auto-detected if not provided)')
    parser.add_argument('--repo', help='GitHub repository name (auto-detected if not provided)')
    
    args = parser.parse_args()
    
    # Get GitHub token
    token = get_github_token()
    if not token:
        return 1
    
    # Get repository info
    owner = args.owner
    repo = args.repo
    
    if not owner or not repo:
        detected_owner, detected_repo = get_repo_info()
        owner = owner or detected_owner
        repo = repo or detected_repo
    
    if not owner or not repo:
        print("❌ Could not determine repository information")
        print("💡 Use --owner and --repo flags or run from git repository")
        return 1
    
    print(f"📊 Analyzing DORA metrics for {owner}/{repo} (last {args.days} days)...")
    
    # Fetch workflow runs
    try:
        runs = fetch_workflow_runs(owner, repo, token, args.days)
        print(f"📈 Found {len(runs)} workflow runs")
    except Exception as e:
        print(f"❌ Failed to fetch workflow runs: {e}")
        return 1
    
    if not runs:
        print("⚠️  No workflow runs found in the specified period")
        return 1
    
    # Analyze deployments
    deployment_metrics = analyze_deployment_workflows(runs)
    
    # Calculate lead time
    lead_time_metrics = calculate_lead_time(runs)
    
    # Get DORA classification
    dora_class = get_dora_classification(
        deployment_metrics['deployment_frequency_weekly'],
        lead_time_metrics['avg_lead_time_hours'],
        deployment_metrics['deployment_success_rate']
    )
    
    # Compile results
    dora_data = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'repository': f'{owner}/{repo}',
        'analysis_period_days': args.days,
        'deployment_metrics': deployment_metrics,
        'lead_time_metrics': lead_time_metrics,
        'dora_classification': dora_class,
        'recommendations': generate_recommendations(deployment_metrics, lead_time_metrics, dora_class)
    }
    
    # Write output
    with open(args.out, 'w') as f:
        json.dump(dora_data, f, indent=2)
    
    # Print summary
    print(f"✅ DORA metrics generated: {args.out}")
    print(f"\n📊 DORA Summary:")
    print(f"   • Deployment Frequency: {deployment_metrics['deployment_frequency_weekly']:.1f}/week ({dora_class['deployment_frequency']})")
    print(f"   • Lead Time: {lead_time_metrics['avg_lead_time_hours']:.1f}h ({dora_class['lead_time']})")
    print(f"   • Success Rate: {deployment_metrics['deployment_success_rate']:.1f}% ({dora_class['success_rate']})")
    print(f"   • Overall: {dora_class['overall']}")
    
    return 0

def generate_recommendations(deploy_metrics: Dict, lead_metrics: Dict, 
                           classification: Dict) -> List[str]:
    """Generate actionable recommendations based on DORA metrics."""
    recommendations = []
    
    if deploy_metrics['deployment_frequency_weekly'] < 1:
        recommendations.append("🚀 Increase deployment frequency - aim for at least weekly deployments")
    
    if lead_metrics['avg_lead_time_hours'] > 24:
        recommendations.append("⚡ Reduce lead time - optimize CI/CD pipeline for faster delivery")
    
    if deploy_metrics['deployment_success_rate'] < 90:
        recommendations.append("🔧 Improve deployment reliability - add more comprehensive testing")
    
    if "Elite" not in classification['overall']:
        recommendations.append("📈 Consider implementing trunk-based development and feature flags")
        recommendations.append("🔄 Automate more of your deployment pipeline")
    
    if not recommendations:
        recommendations.append("🏆 Excellent DORA metrics! Consider sharing best practices with other teams")
    
    return recommendations

if __name__ == "__main__":
    exit(main())

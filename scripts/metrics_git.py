#!/usr/bin/env python3
"""
Enhanced Git Metrics Script with Regional Benchmarks and DORA Analysis
Supports monorepo analysis and international comparisons (ES/EU/US)
"""

import os
import sys
import json
import subprocess
import statistics
import argparse
from datetime import datetime, timedelta, timezone
from collections import Counter

def sh(cmd):
    """Execute shell command and return stripped output."""
    return subprocess.check_output(cmd, shell=True, text=True).strip()

def parse_args():
    """Parse command line arguments."""
    ap = argparse.ArgumentParser(description='Enhanced Git metrics with regional benchmarks')
    ap.add_argument("--window-days", type=int, default=90, help="Analysis window in days")
    ap.add_argument("--out", default="metrics.json", help="Output JSON file")
    return ap.parse_args()

def commits_since(days):
    """Get commits since N days with scope analysis (monorepo-aware)."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    fmt = "%H|%ct|%an|%s"
    
    try:
        out = sh(f"git log --since='{since}' --pretty=format:'{fmt}' --no-merges")
    except subprocess.CalledProcessError:
        return []
    
    items = []
    if out:
        for line in out.splitlines():
            try:
                h, ts, an, msg = line.split("|", 3)
                
                # Determine scope based on changed files (monorepo-aware)
                try:
                    changed_files = sh(f"git diff-tree --no-commit-id --name-only -r {h}")
                    scope = "mixed"  # default
                    if "frontend/" in changed_files:
                        scope = "frontend"
                    elif "backend/" in changed_files:
                        scope = "backend"
                    elif "infra/" in changed_files:
                        scope = "infrastructure"
                    elif any(ext in changed_files for ext in [".yml", ".yaml", ".json"]):
                        scope = "devops"
                    elif ".md" in changed_files:
                        scope = "documentation"
                except:
                    scope = "unknown"
                
                items.append((h, int(ts), an, msg, scope))
            except Exception:
                continue
    return items

def numstat_since(days):
    """Get line changes and file activity since N days."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    
    try:
        out = sh(f"git log --since='{since}' --numstat --pretty=format:'COMMIT:%H' --no-merges")
    except subprocess.CalledProcessError:
        return 0, 0, []
    
    add = del_ = 0
    file_hits = Counter()
    
    for ln in out.splitlines():
        if ln.startswith("COMMIT:"):
            continue
        elif ln.strip():
            parts = ln.split("\t")
            if len(parts) == 3:
                a, d, f = parts
                if a.isdigit():
                    add += int(a)
                if d.isdigit():
                    del_ += int(d)
                file_hits[f] += 1
    
    return add, del_, file_hits.most_common(15)

def envf(key):
    """Get environment variable as float."""
    value = os.getenv(key)
    return float(value) if value else None

def calculate_dora_metrics(commits, window_days):
    """Calculate DORA metrics from commit data."""
    if not commits:
        return {}
    
    # Extract timestamps
    timestamps = [ts for _, ts, _, _, _ in commits]
    timestamps.sort()
    
    # Deployment frequency (approximated by commit frequency)
    deploy_freq_per_week = len(commits) / (window_days / 7.0) if window_days > 0 else 0
    
    # Lead time (average time between commits)
    gaps = [t2 - t1 for t1, t2 in zip(timestamps, timestamps[1:])]
    avg_lead_time_hours = (sum(gaps) / len(gaps) / 3600.0) if gaps else None
    
    # Change failure rate (approximated by revert/fix commits)
    fix_commits = len([msg for _, _, _, msg, _ in commits 
                      if any(word in msg.lower() for word in ['fix', 'revert', 'hotfix', 'patch'])])
    change_failure_rate = (fix_commits / len(commits)) * 100 if commits else 0
    
    return {
        "deployment_frequency_weekly": round(deploy_freq_per_week, 2),
        "lead_time_hours": round(avg_lead_time_hours, 2) if avg_lead_time_hours else None,
        "change_failure_rate_percent": round(change_failure_rate, 2)
    }

def get_regional_benchmarks():
    """Get regional benchmarks from environment variables."""
    return {
        "SP": {
            "commits_wk": envf("SP_COMMITS_WK") or 10,  # Default Spain benchmark
            "time_between_h": envf("SP_TIME_BETWEEN_H") or 12,
            "lead_time_h": envf("SP_LEAD_TIME_H") or 24,
            "deploy_freq_wk": envf("SP_DEPLOY_FREQ_WK") or 5
        },
        "EU": {
            "commits_wk": envf("EU_COMMITS_WK") or 11,  # Default EU benchmark
            "time_between_h": envf("EU_TIME_BETWEEN_H") or 11,
            "lead_time_h": envf("EU_LEAD_TIME_H") or 20,
            "deploy_freq_wk": envf("EU_DEPLOY_FREQ_WK") or 6
        },
        "US": {
            "commits_wk": envf("US_COMMITS_WK") or 12,  # Default US benchmark
            "time_between_h": envf("US_TIME_BETWEEN_H") or 10,
            "lead_time_h": envf("US_LEAD_TIME_H") or 18,
            "deploy_freq_wk": envf("US_DEPLOY_FREQ_WK") or 8
        }
    }

def compare_with_benchmarks(metrics, dora_metrics, benchmarks):
    """Compare project metrics with regional benchmarks."""
    comparisons = {}
    
    for region, bench in benchmarks.items():
        comparisons[region] = {
            "commits_wk_delta": round(metrics["commits_per_week"] - bench["commits_wk"], 2),
            "time_between_delta_h": round(metrics["avg_gap_hours"] - bench["time_between_h"], 2) if metrics["avg_gap_hours"] else None,
            "lead_time_delta_h": round(dora_metrics.get("lead_time_hours", 0) - bench["lead_time_h"], 2) if dora_metrics.get("lead_time_hours") else None,
            "deploy_freq_delta_wk": round(dora_metrics.get("deployment_frequency_weekly", 0) - bench["deploy_freq_wk"], 2),
            "performance_vs_region": calculate_performance_score(metrics, dora_metrics, bench)
        }
    
    return comparisons

def calculate_performance_score(metrics, dora_metrics, benchmark):
    """Calculate overall performance score vs benchmark (0-100)."""
    scores = []
    
    # Commits frequency score
    if metrics["commits_per_week"] >= benchmark["commits_wk"]:
        scores.append(min(100, (metrics["commits_per_week"] / benchmark["commits_wk"]) * 100))
    else:
        scores.append((metrics["commits_per_week"] / benchmark["commits_wk"]) * 100)
    
    # Lead time score (lower is better)
    if metrics["avg_gap_hours"] and benchmark["time_between_h"]:
        lead_score = max(0, 200 - (metrics["avg_gap_hours"] / benchmark["time_between_h"]) * 100)
        scores.append(min(100, lead_score))
    
    # Deployment frequency score
    deploy_freq = dora_metrics.get("deployment_frequency_weekly", 0)
    if deploy_freq >= benchmark["deploy_freq_wk"]:
        scores.append(min(100, (deploy_freq / benchmark["deploy_freq_wk"]) * 100))
    else:
        scores.append((deploy_freq / benchmark["deploy_freq_wk"]) * 100)
    
    return round(sum(scores) / len(scores), 1) if scores else 0

def get_quality_assessment(score):
    """Get quality assessment based on performance score."""
    if score >= 90:
        return "🚀 Elite (Top 10%)"
    elif score >= 80:
        return "🏆 High Performer (Top 25%)"
    elif score >= 70:
        return "📈 Good (Top 50%)"
    elif score >= 60:
        return "📊 Average (Top 75%)"
    else:
        return "📉 Needs Improvement"

def main():
    """Main execution function."""
    args = parse_args()
    
    print(f"📈 Analyzing Git metrics for the last {args.window_days} days...")
    
    # Get commit data
    commits = commits_since(args.window_days)
    timestamps = sorted(ts for _, ts, _, _, _ in commits)
    
    # Calculate time gaps
    gaps = [t2 - t1 for t1, t2 in zip(timestamps, timestamps[1:])]
    avg_gap_h = (sum(gaps) / len(gaps) / 3600.0) if gaps else None
    
    # Calculate weekly rate
    weeks = max(args.window_days / 7.0, 1.0)
    per_week = len(commits) / weeks
    
    # Analyze contributors and scopes
    authors = Counter(author for _, _, author, _, _ in commits).most_common(10)
    scopes = Counter(scope for _, _, _, _, scope in commits)
    
    # Get file changes
    added, deleted, hot_files = numstat_since(args.window_days)
    
    # Calculate DORA metrics
    dora_metrics = calculate_dora_metrics(commits, args.window_days)
    
    # Get benchmarks and comparisons
    benchmarks = get_regional_benchmarks()
    
    # Build main metrics
    metrics = {
        "window_days": args.window_days,
        "commits_total": len(commits),
        "commits_per_week": round(per_week, 2),
        "avg_gap_hours": round(avg_gap_h, 2) if avg_gap_h else None,
        "authors_top": authors,
        "scope_counts": dict(scopes),
        "added_lines": added,
        "deleted_lines": deleted,
        "hot_files": hot_files,
    }
    
    # Add comparisons
    comparisons = compare_with_benchmarks(metrics, dora_metrics, benchmarks)
    
    # Calculate overall assessment
    avg_scores = [comp["performance_vs_region"] for comp in comparisons.values()]
    overall_score = round(sum(avg_scores) / len(avg_scores), 1) if avg_scores else 0
    
    # Final data structure
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "analysis_window": args.window_days,
        "project_metrics": metrics,
        "dora_metrics": dora_metrics,
        "regional_benchmarks": benchmarks,
        "regional_comparisons": comparisons,
        "overall_performance": {
            "score": overall_score,
            "assessment": get_quality_assessment(overall_score),
            "global_ranking": f"Top {max(5, 100 - overall_score):.0f}%" if overall_score > 0 else "N/A"
        }
    }
    
    # Write output
    with open(args.out, "w") as f:
        json.dump(data, f, indent=2)
    
    # Print summary
    print(f"✅ Enhanced metrics generated: {args.out}")
    print(f"📊 Summary:")
    print(f"   • Commits: {len(commits)} ({per_week:.1f}/week)")
    print(f"   • Contributors: {len(authors)}")
    print(f"   • Lines: +{added:,} / -{deleted:,}")
    print(f"   • DORA Deploy Freq: {dora_metrics.get('deployment_frequency_weekly', 0):.1f}/week")
    print(f"   • Overall Score: {overall_score}/100 ({get_quality_assessment(overall_score)})")
    
    # Regional comparison summary
    print(f"\n🌍 Regional Performance:")
    for region, comp in comparisons.items():
        score = comp["performance_vs_region"]
        print(f"   • {region}: {score}/100 ({get_quality_assessment(score)})")

if __name__ == "__main__":
    main()

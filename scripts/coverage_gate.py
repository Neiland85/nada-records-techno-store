#!/usr/bin/env python3
"""
Enhanced Coverage Gate Script for Nada Records Techno Store
Validates coverage with industrial-grade benchmarking
"""

import sys
import xml.etree.ElementTree as ET

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 coverage_gate.py <coverage.xml> [threshold]")
        sys.exit(1)
    
    path = sys.argv[1]
    min_cov = float(sys.argv[2]) if len(sys.argv) > 2 else 85.0
    
    try:
        rate = float(ET.parse(path).getroot().attrib.get("line-rate", 0.0)) * 100
        
        # Industrial benchmarks
        benchmarks = {
            "🥉 Basic (60%)": 60,
            "🥈 Good (75%)": 75, 
            "🥇 Excellent (85%)": 85,
            "🏆 Elite (90%)": 90,
            "🚀 Unicorn (95%)": 95
        }
        
        level = "❌ Critical"
        for desc, threshold in benchmarks.items():
            if rate >= threshold:
                level = desc
        
        print(f"📊 Coverage: {rate:.2f}% (mínimo {min_cov}%) → {level}")
        
        if rate >= min_cov:
            print(f"✅ PASSED: Coverage gate successful")
            sys.exit(0)
        else:
            gap = min_cov - rate
            print(f"❌ FAILED: Need {gap:.2f}% more coverage")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error parsing coverage: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

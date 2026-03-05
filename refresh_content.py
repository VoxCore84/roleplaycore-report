#!/usr/bin/env python3
"""Refresh data files from local sources, then rebuild the site.

Usage:
    python refresh_content.py          # refresh data + rebuild
    python refresh_content.py --dry    # show what would change, don't write
"""

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data")

# Local source paths (Windows)
WAGO_DIR = r"C:\Users\atayl\source\wago"
RC_TOOLS = r"C:\Dev\RoleplayCore\tools"
RC_DOC = r"C:\Dev\RoleplayCore\doc"


def count_tools():
    """Count Python scripts across tool repositories."""
    count = 0
    for d in [WAGO_DIR, RC_TOOLS]:
        if os.path.isdir(d):
            count += len([f for f in os.listdir(d) if f.endswith('.py')])
    return count


def refresh_changelog():
    """Read changelog from local gist cache if available."""
    gist_path = os.path.join(RC_DOC, "gist_changelog.md")
    if not os.path.exists(gist_path):
        print(f"  [skip] {gist_path} not found")
        return None

    # Parse most recent entries (date + title + summary)
    entries = []
    with open(gist_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('|') and '**' in line:
                cols = [c.strip() for c in line.split('|')[1:-1]]
                if len(cols) >= 3:
                    date = cols[0].replace('**', '').strip()
                    title = cols[1].replace('**', '').strip()
                    summary = cols[2].strip()
                    if date and title:
                        entries.append({
                            "date": date,
                            "title": title,
                            "summary": summary
                        })

    return entries[:8] if entries else None


def main():
    dry = '--dry' in sys.argv

    print("Refreshing content from local sources...")

    # Tool count
    tc = count_tools()
    if tc > 0:
        print(f"  Tools found: {tc} Python scripts")

    # Changelog
    cl = refresh_changelog()
    if cl:
        print(f"  Changelog: {len(cl)} entries")
        if not dry:
            with open(os.path.join(DATA_DIR, "changelog.json"), 'w', encoding='utf-8') as f:
                json.dump(cl, f, indent=2, ensure_ascii=False)
            print("  -> wrote changelog.json")

    if dry:
        print("\nDry run — no files written.")
        return

    # Rebuild
    print("\nRebuilding site...")
    subprocess.run([sys.executable, os.path.join(ROOT, "build_site.py")], check=True)


if __name__ == '__main__':
    main()

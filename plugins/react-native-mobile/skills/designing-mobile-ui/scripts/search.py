#!/usr/bin/env python3
"""
Mobile Design Search Tool
Search for design recommendations across colors, styles, typography, UX guidelines, and products.

Usage:
    python3 search.py "<keywords>" --domain <domain> [-n <max_results>]

Domains:
    colors      - Color palettes for different app types
    styles      - Mobile UI styles (iOS, Material, etc.)
    typography  - Font pairings for mobile
    ux          - UX guidelines and best practices
    products    - Product type recommendations
    all         - Search all domains (default)

Examples:
    python3 search.py "social vibrant" --domain colors
    python3 search.py "ios minimal" --domain styles
    python3 search.py "banking luxury" --domain products
    python3 search.py "keyboard" --domain ux
"""

import argparse
import csv
import os
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

DOMAINS = {
    "colors": "colors.csv",
    "styles": "styles.csv",
    "typography": "typography.csv",
    "ux": "ux-guidelines.csv",
    "products": "products.csv",
}

def load_csv(filename):
    """Load CSV file and return list of dicts."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def search_records(records, keywords, search_fields=None):
    """Search records for matching keywords."""
    keywords_lower = keywords.lower().split()
    results = []

    for record in records:
        # Search in specified fields or all fields
        if search_fields:
            search_text = " ".join(str(record.get(f, "")) for f in search_fields).lower()
        else:
            search_text = " ".join(str(v) for v in record.values()).lower()

        # Count matching keywords
        matches = sum(1 for kw in keywords_lower if kw in search_text)
        if matches > 0:
            results.append((matches, record))

    # Sort by match count descending
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results]

def format_colors(record):
    """Format color palette result."""
    output = f"\n### {record['name'].replace('-', ' ').title()}\n"
    output += f"**Category:** {record['category']}\n"
    output += f"**Best for:** {record['best_for']}\n\n"
    output += "```javascript\n"
    output += "module.exports = {\n"
    output += f"  primary: '{record['primary']}',\n"
    output += f"  accent: '{record['accent']}',\n"
    output += "  background: {\n"
    output += f"    light: '{record['background_light']}',\n"
    output += f"    dark: '{record['background_dark']}',\n"
    output += "  },\n"
    output += "};\n"
    output += "```\n"
    return output

def format_styles(record):
    """Format style result."""
    output = f"\n### {record['name'].replace('-', ' ').title()}\n"
    output += f"**Description:** {record['description']}\n"
    output += f"**Characteristics:** {record['characteristics']}\n"
    output += f"**Border Radius:** {record['radius']}\n"
    output += f"**Shadows:** {record['shadows']}\n"
    output += f"**Animations:** {record['animations']}\n"
    output += f"**Best for:** {record['best_for']}\n"
    return output

def format_typography(record):
    """Format typography result."""
    output = f"\n### {record['name'].replace('-', ' ').title()}\n"
    output += f"**Display Font:** {record['display_font']}\n"
    output += f"**Body Font:** {record['body_font']}\n"
    output += f"**Category:** {record['category']}\n"
    output += f"**Best for:** {record['best_for']}\n\n"
    output += "```bash\n"
    output += f"# Expo installation\n"
    output += f"npx expo install {record['expo_install']}\n"
    output += "```\n"
    return output

def format_ux(record):
    """Format UX guideline result."""
    output = f"\n### {record['topic'].replace('-', ' ').title()}: {record['rule']}\n"
    output += f"**Priority:** {record['priority']}\n\n"
    output += f"| Do | Don't |\n"
    output += f"|---|---|\n"
    output += f"| {record['do']} | {record['dont']} |\n"
    return output

def format_products(record):
    """Format product result."""
    output = f"\n### {record['product_type'].replace('-', ' ').title()}\n"
    output += f"**Recommended Style:** {record['recommended_style']}\n"
    output += f"**Recommended Colors:** {record['recommended_colors']}\n"
    output += f"**Recommended Typography:** {record['recommended_typography']}\n"
    output += f"**Key Features:** {record['key_features']}\n"
    return output

FORMATTERS = {
    "colors": format_colors,
    "styles": format_styles,
    "typography": format_typography,
    "ux": format_ux,
    "products": format_products,
}

def search_domain(domain, keywords, max_results=5):
    """Search a specific domain."""
    if domain not in DOMAINS:
        return f"Unknown domain: {domain}"

    records = load_csv(DOMAINS[domain])
    if not records:
        return f"No data found for domain: {domain}"

    # Search with keyword field prioritization
    search_fields = ["keywords", "name", "best_for"] if domain != "ux" else ["keywords", "topic", "rule"]
    results = search_records(records, keywords, search_fields)[:max_results]

    if not results:
        return f"No results found for '{keywords}' in {domain}"

    formatter = FORMATTERS[domain]
    output = f"## {domain.title()} Results ({len(results)} matches)\n"
    for record in results:
        output += formatter(record)

    return output

def search_all(keywords, max_results=3):
    """Search all domains."""
    output = ""
    for domain in DOMAINS:
        domain_output = search_domain(domain, keywords, max_results)
        if "No results found" not in domain_output:
            output += domain_output + "\n"
    return output if output else f"No results found for '{keywords}' in any domain"

def main():
    parser = argparse.ArgumentParser(description="Search mobile design recommendations")
    parser.add_argument("keywords", help="Search keywords")
    parser.add_argument("--domain", "-d", default="all",
                       choices=list(DOMAINS.keys()) + ["all"],
                       help="Domain to search (default: all)")
    parser.add_argument("-n", "--max-results", type=int, default=5,
                       help="Maximum results per domain (default: 5)")

    args = parser.parse_args()

    if args.domain == "all":
        result = search_all(args.keywords, args.max_results)
    else:
        result = search_domain(args.domain, args.keywords, args.max_results)

    print(result)

if __name__ == "__main__":
    main()

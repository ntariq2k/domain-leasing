"""
Fetches Google News RSS for each lease domain and writes blog-data.json.
Run locally or via GitHub Actions daily.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timezone

DOMAINS = {
    'nycreagent.com':         {'query': 'NYC real estate agent market',        'niche': 'NYC Real Estate'},
    'webuyqueens.com':        {'query': 'Queens NY home sale real estate',      'niche': 'Queens Real Estate'},
    'webuynycbuilding.com':   {'query': 'NYC commercial building investment',   'niche': 'NYC Commercial RE'},
    'webuynycbuildings.com':  {'query': 'New York City building acquisition',   'niche': 'NYC Building Market'},
    'njsellersagent.com':     {'query': 'New Jersey home selling real estate',  'niche': 'NJ Real Estate'},
    'nycroofexperts.com':     {'query': 'NYC roofing contractor repair cost',   'niche': 'NYC Roofing'},
    'nycpaintexperts.com':    {'query': 'NYC painting contractor commercial',   'niche': 'NYC Painting'},
    'nycreconsultant.com':    {'query': 'NYC real estate market consulting',    'niche': 'NYC RE Consulting'},
    'nycreconsultants.com':   {'query': 'New York real estate market trends',   'niche': 'NYC RE Market'},
}

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; domain-news-bot/1.0)'}


def fetch_rss(query, count=6):
    encoded = urllib.parse.quote(query)
    url = f'https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read()
    except Exception as e:
        print(f'  RSS fetch error: {e}')
        return None


def parse_date(pub_date):
    for fmt in ('%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S GMT'):
        try:
            return datetime.strptime(pub_date.strip(), fmt).strftime('%b %d, %Y')
        except Exception:
            pass
    return pub_date[:10] if pub_date else ''


def parse_rss(xml_bytes, count=6):
    if not xml_bytes:
        return []
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        print(f'  XML parse error: {e}')
        return []

    articles = []
    for item in root.findall('.//item')[:count]:
        raw_title = item.findtext('title', '').strip()
        link      = item.findtext('link', '').strip()
        pub_date  = item.findtext('pubDate', '').strip()
        source_el = item.find('source')
        source    = source_el.text.strip() if source_el is not None and source_el.text else ''

        # Google News appends " - Source Name" to titles
        if ' - ' in raw_title:
            parts = raw_title.rsplit(' - ', 1)
            title = parts[0].strip()
            if not source:
                source = parts[1].strip()
        else:
            title = raw_title

        if not title or not link:
            continue

        articles.append({
            'title':  title,
            'link':   link,
            'source': source,
            'date':   parse_date(pub_date),
        })

    return articles


def main():
    result = {'updated': datetime.now(timezone.utc).strftime('%Y-%m-%d')}

    for domain, cfg in DOMAINS.items():
        print(f'Fetching: {domain} — "{cfg["query"]}"')
        xml_bytes = fetch_rss(cfg['query'])
        articles  = parse_rss(xml_bytes)
        result[domain] = {'niche': cfg['niche'], 'articles': articles}
        print(f'  {len(articles)} articles')

    out_path = 'blog-data.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    total = sum(len(v.get('articles', [])) for v in result.values() if isinstance(v, dict))
    print(f'\nDone. {total} total articles written to {out_path}')


if __name__ == '__main__':
    main()

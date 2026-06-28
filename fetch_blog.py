"""
fetch_blog.py
Fetches Google News RSS and generates a fully static, SEO-optimised HTML page
for every lease domain. Run locally or via GitHub Actions (every 6 hours).

Output:
  sites/<domain>/index.html  — static page per domain (all SEO hardcoded)
  blog-data.json             — kept for index.html fallback / Netlify preview
  sitemap.xml                — updated daily
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import os
import re
from html import escape
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Domain catalogue — all SEO data lives here
# ---------------------------------------------------------------------------
DOMAINS = {
    'nycreagent.com': {
        'query':       'NYC real estate agent when:30d',
        'niche':       'NYC Real Estate',
        'tagline':     'Short, clean, powerful — the ultimate digital identity for a NYC real estate agent.',
        'features': [
            'Ultra-brandable: NYC + RE + Agent in 12 characters — the kind of name top producers pay for',
            'One closed NYC deal covers years of lease fees — avg commission is $25,000+',
            'Ideal for solo agents, top-producing teams, and boutique brokerages scaling in NYC',
        ],
        'about': (
            'nycreagent.com is a keyword-exact domain built for NYC real estate agents, Manhattan brokers, '
            'and Brooklyn realtors looking to own their market online. Established professionals and '
            'fast-growing teams lease premium geo+trade domains to claim immediate digital authority '
            'in the New York City real estate market. A single commission from one closed deal more '
            'than covers a full year of lease fees.'
        ),
        'monthly': '$450', 'annual': '$383', 'biennial': '$338',
        'keywords':    'NYC real estate agent, New York City realtor, Manhattan real estate agent, Brooklyn real estate broker, NYC property agent, New York real estate',
        'geo_region':  'US-NY', 'geo_place': 'New York City', 'schema_type': 'RealEstateAgent',
    },
    'webuyqueens.com': {
        'query':       'Queens NY home sale real estate when:30d',
        'niche':       'Queens Real Estate',
        'tagline':     "Own the cash home buying market in Queens — one of NYC's most active boroughs.",
        'features': [
            'Queens processes thousands of off-market home sales annually — this domain owns that search',
            'A single wholesale deal in Queens nets $10,000–$40,000 — this domain pays for itself in hours',
            'Clean, memorable brand investors and sellers trust immediately',
        ],
        'about': (
            'webuyqueens.com is the definitive brand for cash home buyers, real estate investors, and '
            'wholesalers operating in Queens, NY. The borough\'s high volume of off-market transactions '
            'makes a keyword-exact domain like this one a critical tool for capturing motivated seller '
            'traffic before competitors do. Investors who flip or wholesale in Jamaica, Flushing, '
            'Astoria, and Forest Hills use authoritative domain brands to convert sellers faster.'
        ),
        'monthly': '$300', 'annual': '$255', 'biennial': '$225',
        'keywords':    'we buy houses Queens NY, cash home buyer Queens, sell house fast Queens, off-market Queens real estate, buy homes Queens NY, Queens home investors',
        'geo_region':  'US-NY', 'geo_place': 'Queens, New York', 'schema_type': 'RealEstateAgent',
    },
    'webuynycbuilding.com': {
        'query':       'NYC commercial building investment when:30d',
        'niche':       'NYC Commercial Real Estate',
        'tagline':     'The definitive brand for NYC commercial and multi-family building acquisition.',
        'features': [
            'NYC multi-family and commercial deals routinely close at $1M–$50M+ — one deal justifies years of lease',
            'Perfect for syndicates, private equity firms, and commercial real estate investors',
            'Bundle with webuynycbuildings.com for complete brand dominance',
        ],
        'about': (
            'webuynycbuilding.com positions its lessee as the go-to buyer for New York City commercial '
            'real estate, multi-family apartment buildings, and mixed-use properties. Syndicators, '
            'private equity firms, and institutional investors in the NYC market lease premium domain '
            'brands to build instant credibility with building owners, brokers, and off-market deal '
            'sources. In a market where cap rates are compressing and competition for quality assets '
            'is fierce, a commanding digital brand is a meaningful competitive edge.'
        ),
        'monthly': '$350', 'annual': '$298', 'biennial': '$263',
        'keywords':    'buy NYC building, New York commercial real estate acquisition, NYC multi-family building investor, commercial property NYC, NYC building buyer',
        'geo_region':  'US-NY', 'geo_place': 'New York City', 'schema_type': 'RealEstateAgent',
    },
    'webuynycbuildings.com': {
        'query':       'New York City building sale investment when:30d',
        'niche':       'NYC Building Market',
        'tagline':     'The plural companion to webuynycbuilding.com — capture every search variation.',
        'features': [
            'Covers both singular and plural search traffic for NYC building buyers',
            'Best leased as a bundle with webuynycbuilding.com for total brand coverage',
            'Commercial real estate in NYC is among the highest-value markets on the planet',
        ],
        'about': (
            'webuynycbuildings.com captures the plural-form search traffic that webuynycbuilding.com '
            'does not — sellers and brokers who search "we buy NYC buildings" (plural) versus '
            '"we buy NYC building" (singular) represent different searcher habits. Together the two '
            'domains provide complete brand coverage across every variation a motivated commercial '
            'property owner might type, with zero gaps for competitors to exploit.'
        ),
        'monthly': '$200', 'annual': '$170', 'biennial': '$150',
        'keywords':    'buy NYC buildings, New York City building buyers, NYC investment buildings, commercial buildings NYC, NYC multi-family buyers',
        'geo_region':  'US-NY', 'geo_place': 'New York City', 'schema_type': 'RealEstateAgent',
    },
    'njsellersagent.com': {
        'query':       'New Jersey home selling real estate when:30d',
        'niche':       'NJ Real Estate',
        'tagline':     'The go-to brand for New Jersey listing agents who dominate their market.',
        'features': [
            'NJ median home price is $550,000+ — seller-side agents earning 2.5–3% commissions need this brand',
            'Keyword-perfect: motivated sellers searching for NJ listing representation land here',
            'Build a multi-million dollar listing operation on a name that already tells the story',
        ],
        'about': (
            'njsellersagent.com is purpose-built for New Jersey real estate agents who specialise in '
            'seller-side representation and listing services. With New Jersey median home values above '
            '$550,000, a single listing commission typically exceeds $13,000 — making this domain\'s '
            'lease cost an easily justified business expense for any serious listing agent in Bergen, '
            'Essex, Monmouth, Morris, or Middlesex county markets.'
        ),
        'monthly': '$250', 'annual': '$213', 'biennial': '$188',
        'keywords':    'NJ sellers agent, New Jersey listing agent, sell home New Jersey, NJ real estate agent for sellers, New Jersey realtor, NJ listing specialist',
        'geo_region':  'US-NJ', 'geo_place': 'New Jersey', 'schema_type': 'RealEstateAgent',
    },
    'nycroofexperts.com': {
        'query':       'NYC roofing contractor repair cost when:90d',
        'niche':       'NYC Roofing',
        'tagline':     'Become the most recognised roofing brand in the most expensive city in America.',
        'features': [
            'NYC roofing contracts average $15,000–$80,000 — this domain generates ROI on the first call',
            'Geo + trade + "experts" = instant local SEO authority in a fiercely competitive contractor market',
            'Ideal for established roofing companies looking to scale their NYC presence fast',
        ],
        'about': (
            'nycroofexperts.com gives roofing contractors in New York City an immediate SEO and brand '
            'advantage. The combination of the city name, trade category, and "experts" signals authority '
            'to both search engines and prospective clients seeking commercial flat roof work, residential '
            'shingle replacement, or emergency leak repair. In a market where a single roof replacement '
            'contract routinely exceeds $50,000, this domain earns its lease cost on the very first job.'
        ),
        'monthly': '$200', 'annual': '$170', 'biennial': '$150',
        'keywords':    'NYC roofing contractor, New York City roofer, roof repair NYC, commercial roofing New York, flat roof NYC, NYC roof replacement',
        'geo_region':  'US-NY', 'geo_place': 'New York City', 'schema_type': 'HomeAndConstructionBusiness',
    },
    'nycpaintexperts.com': {
        'query':       'NYC painting contractor commercial when:90d',
        'niche':       'NYC Painting',
        'tagline':     'The authority brand for painting contractors ready to own the NYC market.',
        'features': [
            'NYC commercial painting contracts routinely run $20,000–$200,000+ per project',
            'Instantly positions your company as the expert choice in a city of 8 million people',
            'One commercial building contract from this domain covers years of lease costs',
        ],
        'about': (
            'nycpaintexperts.com is the premium digital brand for painting contractors serving New York '
            'City\'s residential and commercial markets. From luxury Manhattan apartment interiors to '
            'large-scale commercial building exteriors in the Bronx and Brooklyn, the NYC painting '
            'industry is one of the highest-revenue trade markets in the country. This domain '
            'communicates expertise and scale to the clients who can afford to pay for quality.'
        ),
        'monthly': '$150', 'annual': '$128', 'biennial': '$113',
        'keywords':    'NYC painting contractor, New York City painter, commercial painting NYC, interior painting contractor New York, building painting NYC, NYC house painter',
        'geo_region':  'US-NY', 'geo_place': 'New York City', 'schema_type': 'HomeAndConstructionBusiness',
    },
    'nycreconsultant.com': {
        'query':       'NYC real estate consulting market when:30d',
        'niche':       'NYC RE Consulting',
        'tagline':     'The authority brand for NYC real estate consultants commanding premium fees.',
        'features': [
            'NYC RE consulting engagements regularly command $500–$5,000/hour — this domain matches that caliber',
            'Bundle with nycreconsultants.com for complete singular + plural brand coverage',
            'Clean, professional, authoritative — the name serious consultants build empires on',
        ],
        'about': (
            'nycreconsultant.com is the singular-form authority domain for New York City real estate '
            'consulting professionals. Whether advising institutional investors on portfolio strategy, '
            'guiding high-net-worth individuals through market entry decisions, or supporting '
            'development groups with acquisition due diligence, this domain signals the depth of '
            'expertise and local market knowledge that clients in NYC\'s multi-billion-dollar '
            'consulting sector are paying premium fees to access.'
        ),
        'monthly': '$225', 'annual': '$191', 'biennial': '$169',
        'keywords':    'NYC real estate consultant, New York property consultant, real estate advisory NYC, Manhattan RE consultant, NYC property advisor, real estate consulting New York',
        'geo_region':  'US-NY', 'geo_place': 'New York City', 'schema_type': 'ProfessionalService',
    },
    'nycreconsultants.com': {
        'query':       'New York real estate market trends when:30d',
        'niche':       'NYC RE Market',
        'tagline':     'The plural powerhouse brand for NYC real estate consulting firms.',
        'features': [
            'Ideal for multi-advisor practices, RE advisory firms, and consulting groups in New York City',
            'Bundle with nycreconsultant.com to own both singular and plural — no competitor can touch you',
            "NYC's high-end RE consulting market is worth billions — this name puts you at the front of it",
        ],
        'about': (
            'nycreconsultants.com is the plural-form companion domain for New York City real estate '
            'advisory firms and multi-consultant practices. Groups of advisors, boutique consultancies, '
            'and full-service RE advisory firms use this domain to communicate scale, depth, and '
            'institutional credibility to high-value clients seeking comprehensive market expertise '
            'across the NYC metro area.'
        ),
        'monthly': '$200', 'annual': '$170', 'biennial': '$150',
        'keywords':    'NYC real estate consultants, New York property consulting firm, real estate advisory firm NYC, Manhattan RE consultants, NYC consulting group',
        'geo_region':  'US-NY', 'geo_place': 'New York City', 'schema_type': 'ProfessionalService',
    },
}

HEADERS       = {'User-Agent': 'Mozilla/5.0 (compatible; domain-news-bot/1.0)'}
FORMSPREE_ID  = 'mykqjzoq'

# ---------------------------------------------------------------------------
# RSS fetching / parsing
# ---------------------------------------------------------------------------

def fetch_rss(query):
    encoded = urllib.parse.quote(query)
    url = f'https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read()
    except Exception as e:
        print(f'  RSS fetch error: {e}')
        return None


def fetch_rss_with_fallback(query, min_count=10):
    """Fetch RSS; if results are thin, retry with a broader time window."""
    xml_bytes = fetch_rss(query)
    articles  = parse_rss(xml_bytes)
    if len(articles) < min_count:
        # Strip any when: filter and retry without date restriction
        broad_query = re.sub(r'\s+when:\S+', '', query).strip()
        if broad_query != query:
            print(f'  Only {len(articles)} articles — retrying without time filter')
            xml_bytes = fetch_rss(broad_query)
            articles  = parse_rss(xml_bytes)
    return articles


def parse_date(pub_date):
    for fmt in ('%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S GMT'):
        try:
            return datetime.strptime(pub_date.strip(), fmt).strftime('%b %d, %Y')
        except Exception:
            pass
    return pub_date[:10] if pub_date else ''


def parse_rss(xml_bytes, count=20):
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

        if ' - ' in raw_title:
            parts  = raw_title.rsplit(' - ', 1)
            title  = parts[0].strip()
            if not source:
                source = parts[1].strip()
        else:
            title = raw_title

        if not title or not link:
            continue
        articles.append({'title': title, 'link': link, 'source': source, 'date': parse_date(pub_date)})

    return articles

# ---------------------------------------------------------------------------
# CSS extraction (single source of truth stays in index.html)
# ---------------------------------------------------------------------------

def read_css():
    try:
        with open('index.html', encoding='utf-8') as f:
            html = f.read()
        m = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
        return m.group(1) if m else ''
    except Exception:
        return ''

# ---------------------------------------------------------------------------
# Static HTML generation
# ---------------------------------------------------------------------------

def build_schema(domain, cfg, date_str):
    canonical  = f'https://{domain}/'
    price_num  = cfg['monthly'].replace('$', '')
    addr_region = cfg['geo_region'].split('-')[1]
    title      = f"{domain} — Premium Domain for Lease | {cfg['niche']}"
    meta_desc  = f"{domain} is available for lease. {cfg['tagline']} Starting at {cfg['monthly']}/mo."

    webpage = {
        '@type': 'WebPage',
        '@id': canonical,
        'url': canonical,
        'name': title,
        'description': meta_desc,
        'inLanguage': 'en-US',
        'dateModified': date_str,
    }
    business = {
        '@type': cfg['schema_type'],
        'name': domain,
        'url': canonical,
        'description': cfg['tagline'],
        'areaServed': cfg['geo_place'],
        'address': {
            '@type': 'PostalAddress',
            'addressRegion': addr_region,
            'addressCountry': 'US',
        },
        'offers': {
            '@type': 'Offer',
            'priceCurrency': 'USD',
            'price': price_num,
            'availability': 'https://schema.org/InStock',
            'description': f'Exclusive domain lease — {domain}. Month-to-month or multi-year terms available.',
        },
    }
    return json.dumps({'@context': 'https://schema.org', '@graph': [webpage, business]}, ensure_ascii=False)


def build_faq(domain, cfg):
    m = cfg['monthly']
    a = cfg['annual']
    b = cfg['biennial']
    faq = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': f'How much does it cost to lease {domain}?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'{domain} leases for {m}/month on a month-to-month basis, '
                        f'{a}/month billed annually (save 15%), or '
                        f'{b}/month on a 2-year plan (save 25%).'
                    ),
                },
            },
            {
                '@type': 'Question',
                'name': f'What is included when I lease {domain}?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'You receive exclusive use of {domain} for the full lease term. '
                        'All traffic, leads, and brand authority belong to you. '
                        'The domain is pointed to your website or landing page of choice.'
                    ),
                },
            },
            {
                '@type': 'Question',
                'name': f'Can I cancel my {domain} lease?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        'Month-to-month leases can be cancelled anytime with no penalty. '
                        'Annual and 2-year plans are prepaid at a discount. '
                        'Use the inquiry form below to discuss terms.'
                    ),
                },
            },
        ],
    }
    return json.dumps(faq, ensure_ascii=False)


def generate_html(domain, cfg, articles, date_str, css):
    canonical = f'https://{domain}/'
    title     = f"{domain} — Premium Domain for Lease | {cfg['niche']}"
    meta_desc = f"{domain} is available for lease. {cfg['tagline']} Starting at {cfg['monthly']}/mo."

    features_html = '\n'.join(
        f'        <li><span class="check">&#10003;</span><span>{escape(f)}</span></li>'
        for f in cfg['features']
    )

    if articles:
        items_html = '\n'.join(
            f'      <article class="news-item">\n'
            f'        <a class="news-title" href="{escape(a["link"])}" target="_blank" rel="noopener noreferrer">{escape(a["title"])}</a>\n'
            f'        <span class="news-meta">{escape(a["source"])} &middot; {escape(a["date"])}</span>\n'
            f'      </article>'
            for a in articles
        )
        news_section = (
            f'  <section class="card" aria-label="{escape(cfg["niche"])} news">\n'
            f'    <h2 class="card-title">{escape(cfg["niche"])} News '
            f'<span class="news-badge">Updated Daily</span></h2>\n'
            f'    <div class="news-list">\n{items_html}\n    </div>\n  </section>\n'
        )
    else:
        news_section = ''

    m, a, b = cfg['monthly'], cfg['annual'], cfg['biennial']

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(meta_desc)}">
  <meta name="keywords" content="{escape(cfg['keywords'])}">
  <meta name="geo.region" content="{cfg['geo_region']}">
  <meta name="geo.placename" content="{escape(cfg['geo_place'])}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(meta_desc)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(meta_desc)}">
  <link rel="canonical" href="{canonical}">
  <link rel="sitemap" type="application/xml" href="/sitemap.xml">
  <meta name="robots" content="index, follow">
  <script type="application/ld+json">{build_schema(domain, cfg, date_str)}</script>
  <script type="application/ld+json">{build_faq(domain, cfg)}</script>
  <style>{css}
    .about-text {{ margin-top:14px; font-size:14px; color:var(--muted); line-height:1.75; }}
  </style>
</head>
<body>

<header>
  <div class="pill"><span class="dot"></span> Available Now</div>
  <h1>{domain}</h1>
  <p class="tagline">{escape(cfg['tagline'])}</p>
</header>

<main>
  <section class="card" aria-label="Why this domain">
    <h2 class="card-title">Why this domain</h2>
    <ul class="features">
{features_html}
    </ul>
    <p class="about-text">{escape(cfg['about'])}</p>
  </section>

  <section class="card" aria-label="Lease pricing">
    <h2 class="card-title">Lease pricing</h2>
    <div class="pricing-grid">
      <div class="tier">
        <div class="tier-term">Monthly</div>
        <div class="tier-price">{m}/mo</div>
        <div class="tier-per">per month</div>
        <span class="tier-save none">-</span>
      </div>
      <div class="tier tier-featured">
        <div class="tier-badge">Most popular</div>
        <div class="tier-term">Annual</div>
        <div class="tier-price">{a}/mo</div>
        <div class="tier-per">per month, billed yearly</div>
        <span class="tier-save">Save 15%</span>
      </div>
      <div class="tier">
        <div class="tier-term">2-Year</div>
        <div class="tier-price">{b}/mo</div>
        <div class="tier-per">per month, billed 2yr</div>
        <span class="tier-save">Save 25%</span>
      </div>
    </div>
  </section>

  <section class="card" aria-label="Domain inquiry form">
    <h2 class="card-title">Inquire about {domain}</h2>
    <div class="success" id="success">
      <div class="success-icon">&#9989;</div>
      <h3>Message received!</h3>
      <p>We&#39;ll follow up within 24 hours at the email you provided.</p>
    </div>
    <form id="inquiry-form" action="https://formspree.io/f/{FORMSPREE_ID}" method="POST">
      <input type="hidden" name="_subject" value="Domain lease inquiry: {domain}">
      <input type="hidden" name="domain" value="{domain}">
      <div class="grid2">
        <div class="field">
          <label for="fname">Full name *</label>
          <input id="fname" type="text" name="name" required placeholder="Jane Smith">
        </div>
        <div class="field">
          <label for="business">Business name</label>
          <input id="business" type="text" name="business" placeholder="Acme LLC">
        </div>
      </div>
      <div class="grid2">
        <div class="field">
          <label for="email">Email *</label>
          <input id="email" type="email" name="email" required placeholder="you@company.com">
        </div>
        <div class="field">
          <label for="phone">Phone</label>
          <input id="phone" type="tel" name="phone" placeholder="(212) 555-0100">
        </div>
      </div>
      <div class="field">
        <label for="term">Preferred lease term</label>
        <select id="term" name="term">
          <option value="monthly">Month-to-month</option>
          <option value="annual">Annual &#8212; save 15%</option>
          <option value="biennial">2-Year &#8212; save 25%</option>
        </select>
      </div>
      <div class="field">
        <label for="message">Tell us about your business</label>
        <textarea id="message" name="message" placeholder="How would you use this domain? What market are you serving?"></textarea>
      </div>
      <button type="submit" class="btn" id="submit-btn">Send Inquiry &#8594;</button>
    </form>
  </section>

{news_section}
</main>

<footer>
  <p>Premium domain lease listing &middot; Last updated {date_str} &middot;
  <a href="mailto:omegaincomeclub@gmail.com">Contact owner</a></p>
  <p class="visitor-count" id="visitor-count" aria-live="polite"></p>
</footer>

<script>
(function () {{
  var form = document.getElementById('inquiry-form');
  var btn  = document.getElementById('submit-btn');
  var ok   = document.getElementById('success');
  form.addEventListener('submit', function (e) {{
    e.preventDefault();
    btn.textContent = 'Sending…';
    btn.disabled = true;
    fetch(form.action, {{
      method: 'POST',
      body: new FormData(form),
      headers: {{ Accept: 'application/json' }},
    }}).then(function (res) {{
      if (res.ok) {{ form.style.display = 'none'; ok.style.display = 'block'; }}
      else {{ btn.textContent = 'Something went wrong — try again'; btn.disabled = false; }}
    }}).catch(function () {{
      btn.textContent = 'Something went wrong — try again';
      btn.disabled = false;
    }});
  }});

  // Visitor counter — CounterAPI.dev (free, no signup). Fails silently.
  (function () {{
    var el = document.getElementById('visitor-count');
    if (!el) return;
    var slug = window.location.hostname.replace(/^www\./, '').replace(/\./g, '-') || 'local';
    fetch('https://api.counterapi.dev/v1/omegaincomeclub/' + slug + '/up')
      .then(function (r) {{ return r.ok ? r.json() : null; }})
      .then(function (d) {{
        if (!d || typeof d.count !== 'number') return;
        el.innerHTML = '<span class="vc-num">' + d.count.toLocaleString() + '</span> visits';
      }})
      .catch(function () {{}});
  }})();
}})();
</script>
</body>
</html>
'''

# ---------------------------------------------------------------------------
# Sitemap
# ---------------------------------------------------------------------------

def write_sitemap(domain_list, date_str):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for domain in domain_list:
        lines += [
            '  <url>',
            f'    <loc>https://{domain}/</loc>',
            f'    <lastmod>{date_str}</lastmod>',
            '    <changefreq>daily</changefreq>',
            '    <priority>1.0</priority>',
            '  </url>',
        ]
    lines.append('</urlset>')
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'sitemap.xml updated — {len(domain_list)} URLs')

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    now      = datetime.now(timezone.utc)
    date_str = now.strftime('%Y-%m-%d')
    result   = {'updated': date_str}
    css      = read_css()

    for domain, cfg in DOMAINS.items():
        print(f'\nFetching: {domain} — "{cfg["query"]}"')
        articles = fetch_rss_with_fallback(cfg['query'])
        result[domain] = {'niche': cfg['niche'], 'articles': articles}
        print(f'  {len(articles)} articles fetched')

        # Write static HTML
        out_dir = os.path.join('sites', domain)
        os.makedirs(out_dir, exist_ok=True)
        html = generate_html(domain, cfg, articles, date_str, css)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  Generated sites/{domain}/index.html')

    # blog-data.json for index.html fallback (Netlify preview URL)
    with open('blog-data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    total = sum(len(v.get('articles', [])) for v in result.values() if isinstance(v, dict))
    print(f'\nblog-data.json written — {total} total articles')

    write_sitemap(list(DOMAINS.keys()), date_str)
    print('\nAll done.')


if __name__ == '__main__':
    main()

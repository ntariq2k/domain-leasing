"""
email_builder.py — generates personalized cold emails for each lead.
Usage: python outreach/email_builder.py
Input:  outreach/leads.json
Output: outreach/email_queue.json
"""
import json, os

SENDER_NAME  = "Noman"
SENDER_EMAIL = "omegaincomeclub@gmail.com"

# Domain → pitch details (niche, value prop, key benefit)
DOMAIN_PITCH = {
    "nycreagent.com": {
        "domain": "nycreagent.com",
        "niche": "NYC real estate agents",
        "pain": "competing for online visibility in a crowded NYC market",
        "benefit": "a professionally built, SEO-optimized website with your brand at nycreagent.com",
        "price": "$500/month (all-inclusive)",
    },
    "webuyqueens.com": {
        "domain": "webuyqueens.com",
        "niche": "Queens real estate investors",
        "pain": "finding motivated sellers online before the big cash-buyer networks do",
        "benefit": "an established cash-buyer brand website at webuyqueens.com targeting motivated Queens sellers",
        "price": "$500/month (all-inclusive)",
    },
    "webuynycbuilding.com": {
        "domain": "webuynycbuilding.com",
        "niche": "NYC commercial real estate buyers",
        "pain": "standing out to building owners looking to sell off-market",
        "benefit": "a professional commercial building acquisition site at webuynycbuilding.com",
        "price": "$500/month (all-inclusive)",
    },
    "webuynycbuildings.com": {
        "domain": "webuynycbuildings.com",
        "niche": "NYC property acquisition groups",
        "pain": "attracting high-value off-market building sellers at scale",
        "benefit": "an institutional-grade building acquisition brand at webuynycbuildings.com",
        "price": "$500/month (all-inclusive)",
    },
    "njsellersagent.com": {
        "domain": "njsellersagent.com",
        "niche": "New Jersey listing agents",
        "pain": "differentiating yourself as a dedicated sellers agent in a crowded NJ market",
        "benefit": "a niche sellers-agent brand site at njsellersagent.com built to attract NJ home sellers",
        "price": "$500/month (all-inclusive)",
    },
    "nycroofexperts.com": {
        "domain": "nycroofexperts.com",
        "niche": "NYC roofing contractors",
        "pain": "getting found online ahead of the big national roofing chains",
        "benefit": "a lead-generating expert roofing site at nycroofexperts.com with auto-updating industry content",
        "price": "$500/month (all-inclusive)",
    },
    "nycpaintexperts.com": {
        "domain": "nycpaintexperts.com",
        "niche": "NYC painting contractors",
        "pain": "winning commercial painting contracts online without spending on ads",
        "benefit": "a professional painting contractor site at nycpaintexperts.com targeting NYC commercial clients",
        "price": "$500/month (all-inclusive)",
    },
    "nycreconsultant.com": {
        "domain": "nycreconsultant.com",
        "niche": "NYC real estate consultants",
        "pain": "being discovered by institutional and investor clients searching for independent advisors",
        "benefit": "an independent consultancy brand at nycreconsultant.com with advisory credibility built in",
        "price": "$500/month (all-inclusive)",
    },
    "nycreconsultants.com": {
        "domain": "nycreconsultants.com",
        "niche": "NYC real estate consulting firms",
        "pain": "projecting the firm-level authority needed to win institutional consulting mandates",
        "benefit": "a full-service consulting firm brand at nycreconsultants.com backed by deep market content",
        "price": "$500/month (all-inclusive)",
    },
}

SUBJECT_TEMPLATES = [
    "Quick question about your online presence — {domain}",
    "{biz_name}: would a dedicated niche site help you?",
    "Idea for {biz_name} — {domain} lease opportunity",
    "{domain} — professional website available for {niche}",
]

BODY_TEMPLATE = """Hi {first_name},

I came across {biz_name} and wanted to reach out about something that might save you a lot of time and money.

I own the domain {domain} — a professionally built website targeted specifically at {niche} in the NYC/NY area.

Instead of spending $3,000–$10,000 building a custom site from scratch, you could lease this fully operational website for just {price}. That includes:

• A complete, SEO-optimized professional website
• Your business contact info and services prominently featured
• Auto-updating industry news and content (boosts Google rankings)
• Contact forms sending leads directly to you
• Ongoing technical management — zero work on your end

Given that you're in the business of {niche}, this site is built exactly for what your potential clients are searching for.

If this sounds interesting, I'd love to schedule a quick 15-minute call to show you the site live. No pressure — just a look.

Would this week work for you?

Best,
{sender_name}
{sender_email}

P.S. This is a single-tenant lease — once leased, the site operates exclusively under your brand.
"""


def build_first_name(business_name: str) -> str:
    words = business_name.split()
    if words:
        return words[0].title()
    return "there"


def build_emails(leads: list) -> list:
    queue = []
    subject_idx = {}

    for lead in leads:
        domain = lead.get("domain", "")
        pitch  = DOMAIN_PITCH.get(domain)
        if not pitch:
            continue

        biz_name   = lead.get("business_name", "Your Business")
        first_name = build_first_name(biz_name)

        # Rotate subjects per domain to avoid repetition
        idx = subject_idx.get(domain, 0)
        subject_tmpl = SUBJECT_TEMPLATES[idx % len(SUBJECT_TEMPLATES)]
        subject_idx[domain] = idx + 1

        subject = subject_tmpl.format(
            domain=pitch["domain"],
            biz_name=biz_name,
            niche=pitch["niche"],
        )

        body = BODY_TEMPLATE.format(
            first_name=first_name,
            biz_name=biz_name,
            domain=pitch["domain"],
            niche=pitch["niche"],
            pain=pitch["pain"],
            benefit=pitch["benefit"],
            price=pitch["price"],
            sender_name=SENDER_NAME,
            sender_email=SENDER_EMAIL,
        )

        queue.append({
            "to_name": biz_name,
            "to_email": None,  # Google Places doesn't return emails; placeholder for manual enrichment
            "to_phone": lead.get("phone", ""),
            "to_address": lead.get("address", ""),
            "to_website": lead.get("website", ""),
            "domain": domain,
            "subject": subject,
            "body": body,
            "sent": False,
            "sent_at": None,
        })

    return queue


def main():
    leads_path = os.path.join(os.path.dirname(__file__), "leads.json")
    if not os.path.exists(leads_path):
        print("ERROR: leads.json not found. Run lead_scraper.py first.")
        return

    with open(leads_path, encoding="utf-8") as f:
        leads = json.load(f)

    queue = build_emails(leads)

    out_path = os.path.join(os.path.dirname(__file__), "email_queue.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)

    print(f"Email queue built: {len(queue)} emails")
    print(f"Note: to_email is null — Google Places doesn't return emails.")
    print("Enrich with Apollo.io free tier (50/mo) or Hunter.io (25/mo) to fill emails.")
    print(f"Saved to: {out_path}")


if __name__ == "__main__":
    main()

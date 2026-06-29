# Cold Email Outreach — Setup Guide

## Step 1: Get Google Maps API Key (for lead scraping)

1. Go to https://console.cloud.google.com
2. Create a new project (or select existing)
3. APIs & Services → Library → Enable "Places API"
4. APIs & Services → Credentials → Create Credentials → API Key
5. Copy the key — you get $200/month free (~1,000 detail lookups)

## Step 2: Get Gmail OAuth Credentials (for email sending)

1. Same Google Cloud Console → APIs & Services → Library → Enable "Gmail API"
2. APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID
3. Application type: **Desktop app**
4. Download JSON → save as `outreach/credentials.json`

## Step 3: Install Python dependencies

```bash
pip install google-auth google-auth-oauthlib google-api-python-client
```

## Step 4: Scrape leads

```bash
set GOOGLE_MAPS_API_KEY=your_key_here
python outreach/lead_scraper.py
```

Outputs `outreach/leads.json` — 20 businesses per domain = ~180 leads total.

## Step 5: Enrich email addresses

Google Places doesn't return email addresses. Use one of:
- **Apollo.io free** — 50 email lookups/month (https://apollo.io)
- **Hunter.io free** — 25 searches/month (https://hunter.io)
- **Snov.io free** — 50 credits/month (https://snov.io)

Open `leads.json` and paste email addresses into the `to_email` field for each lead.

## Step 6: Build email queue

```bash
python outreach/email_builder.py
```

Outputs `outreach/email_queue.json` with personalized emails for every lead that has a `to_email`.

## Step 7: Send (dry run first)

```bash
# Preview what will be sent — nothing is sent
python outreach/sender.py --dry-run --limit 10

# Send 50 emails (Gmail free limit: 500/day)
python outreach/sender.py --limit 50
```

First real run opens a browser for Gmail OAuth — log in and allow. Token saved as `outreach/token.json`.

## Automation (optional)

Add a GitHub Actions job or Windows Task Scheduler entry to run sender.py daily:
```bash
python outreach/sender.py --limit 50
```

Tracks sent status in `outreach/send_log.json` — already-sent addresses are skipped automatically.

## Files

| File | Purpose |
|------|---------|
| `leads.json` | Raw business leads from Google Maps |
| `email_queue.json` | Personalized emails ready to send |
| `send_log.json` | Sent history (auto-created) |
| `credentials.json` | Gmail OAuth app credentials (you download) |
| `token.json` | Gmail access token (auto-created on first run) |

**Do not commit credentials.json or token.json to git.**

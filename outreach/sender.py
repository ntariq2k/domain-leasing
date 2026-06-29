"""
sender.py — sends cold emails via Gmail API (500 free/day).
Usage: python outreach/sender.py [--limit 50] [--dry-run]

Setup (one-time):
  1. Go to https://console.cloud.google.com → APIs & Services → Enable "Gmail API"
  2. Create OAuth 2.0 credentials (Desktop app) → download as outreach/credentials.json
  3. Run this script once — browser opens for authorization → token.json is saved

Requires: google-auth google-auth-oauthlib google-api-python-client
Install:  pip install google-auth google-auth-oauthlib google-api-python-client
"""
import argparse, base64, json, os, time
from datetime import datetime, timezone
from email.mime.text import MIMEText

SCOPES       = ["https://www.googleapis.com/auth/gmail.send"]
CREDS_FILE   = os.path.join(os.path.dirname(__file__), "credentials.json")
TOKEN_FILE   = os.path.join(os.path.dirname(__file__), "token.json")
QUEUE_FILE   = os.path.join(os.path.dirname(__file__), "email_queue.json")
LOG_FILE     = os.path.join(os.path.dirname(__file__), "send_log.json")
SENDER_EMAIL = "omegaincomeclub@gmail.com"
DAILY_LIMIT  = 500  # Gmail API free limit


def get_gmail_service():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDS_FILE):
                print(f"ERROR: {CREDS_FILE} not found.")
                print("Download OAuth credentials from Google Cloud Console → APIs & Services → Credentials.")
                raise SystemExit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def build_message(to_email: str, subject: str, body: str) -> dict:
    msg = MIMEText(body, "plain")
    msg["To"]      = to_email
    msg["From"]    = SENDER_EMAIL
    msg["Subject"] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {"raw": raw}


def load_send_log() -> dict:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"total_sent": 0, "today_sent": 0, "last_date": "", "sent_to": []}


def save_send_log(log: dict):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit",   type=int, default=50,    help="Max emails to send this run (default 50)")
    parser.add_argument("--dry-run", action="store_true",      help="Print emails without sending")
    args = parser.parse_args()

    if not os.path.exists(QUEUE_FILE):
        print("ERROR: email_queue.json not found. Run email_builder.py first.")
        return

    with open(QUEUE_FILE, encoding="utf-8") as f:
        queue = json.load(f)

    log  = load_send_log()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if log["last_date"] != today:
        log["today_sent"] = 0
        log["last_date"]  = today

    # Filter unsent with a real email address
    pending = [e for e in queue if not e["sent"] and e.get("to_email")]
    if not pending:
        print("No pending emails with valid addresses.")
        print("Run email_builder.py then enrich to_email fields (Apollo.io free / Hunter.io free).")
        return

    remaining_today = DAILY_LIMIT - log["today_sent"]
    to_send = pending[: min(args.limit, remaining_today)]

    if not to_send:
        print(f"Daily limit reached ({DAILY_LIMIT}/day). Try again tomorrow.")
        return

    if not args.dry_run:
        service = get_gmail_service()

    sent_count = 0
    for email in to_send:
        if args.dry_run:
            print(f"[DRY RUN] To: {email['to_email']} | Subject: {email['subject'][:60]}")
            sent_count += 1
            continue

        try:
            msg = build_message(email["to_email"], email["subject"], email["body"])
            service.users().messages().send(userId="me", body=msg).execute()
            email["sent"]    = True
            email["sent_at"] = datetime.now(timezone.utc).isoformat()
            log["today_sent"]  += 1
            log["total_sent"]  += 1
            log["sent_to"].append(email["to_email"])
            sent_count += 1
            print(f"  Sent → {email['to_email']} ({email['domain']})")
            time.sleep(0.5)  # gentle rate limit
        except Exception as e:
            print(f"  Failed → {email['to_email']}: {e}")

    # Save updated queue + log
    if not args.dry_run:
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
        save_send_log(log)

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Sent {sent_count} emails. Today total: {log['today_sent']}/{DAILY_LIMIT}")


if __name__ == "__main__":
    main()

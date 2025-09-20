# IG AI Agent Backend

FastAPI server for Instagram Messaging via the Messenger Send API.

## Prerequisites
- Instagram Professional account connected to a Facebook Page
- Meta Developer App in Live mode
- Permissions (request/approve as needed):
  - instagram_basic
  - instagram_manage_messages
  - pages_manage_metadata
  - pages_messaging
  - pages_manage_engagement

## Configure Webhooks
1. In Meta App > Webhooks, subscribe to `instagram` object with fields: `messages`, `mentions`, `comments` (at minimum `messages`).
2. Set callback URL to: `https://YOUR_DOMAIN/webhook`
3. Set Verify Token to your `VERIFY_TOKEN` value (must match env).

## Local Development
1. Create env file:
```
cp backend/.env.example backend/.env
# edit backend/.env
```
2. Install deps and run:
```
python3 -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
3. Expose via tunnel (e.g., Cloudflared/Ngrok) and set the callback URL in Meta to the public `https://.../webhook`.

## Sending Messages
The server uses the Messenger Send API endpoint:
- `POST https://graph.facebook.com/{GRAPH_API_VERSION}/me/messages?access_token=PAGE_ACCESS_TOKEN`
- Recipient ID is the IG user ID provided in webhook events.

## Notes
- Disclose affiliates in any links you send (FTC/ASA).
- Avoid medical or unsafe claims; escalate business inquiries to email.
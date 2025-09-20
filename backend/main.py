import os
import json
import secrets
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from .ig_api import InstagramAPI

# Load environment variables from .env if present
load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "change-me")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v20.0")

app = FastAPI(title="IG AI Agent Backend")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

ig_api = InstagramAPI(page_access_token=PAGE_ACCESS_TOKEN, graph_api_version=GRAPH_API_VERSION)


class HealthResponse(BaseModel):
	status: str
	version: str


class ConfigResponse(BaseModel):
	verify_token_set: bool
	page_access_token_set: bool
	graph_api_version: str


class ConfigRequest(BaseModel):
	verify_token: Optional[str] = None
	page_access_token: Optional[str] = None
	graph_api_version: Optional[str] = None


class SendTestRequest(BaseModel):
	recipient_id: str
	text: str


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
	return HealthResponse(status="ok", version=GRAPH_API_VERSION)


@app.get("/config", response_model=ConfigResponse)
async def get_config() -> ConfigResponse:
	return ConfigResponse(
		verify_token_set=bool(VERIFY_TOKEN and VERIFY_TOKEN != "change-me"),
		page_access_token_set=bool(PAGE_ACCESS_TOKEN),
		graph_api_version=GRAPH_API_VERSION,
	)


@app.post("/config", response_model=ConfigResponse)
async def set_config(cfg: ConfigRequest) -> ConfigResponse:
	global VERIFY_TOKEN, PAGE_ACCESS_TOKEN, GRAPH_API_VERSION, ig_api
	if cfg.verify_token:
		VERIFY_TOKEN = cfg.verify_token
	if cfg.page_access_token:
		PAGE_ACCESS_TOKEN = cfg.page_access_token
		ig_api.page_access_token = PAGE_ACCESS_TOKEN
	if cfg.graph_api_version:
		GRAPH_API_VERSION = cfg.graph_api_version
		# Recreate API client to apply version change
		ig_api = InstagramAPI(page_access_token=PAGE_ACCESS_TOKEN, graph_api_version=GRAPH_API_VERSION)
	return await get_config()


@app.get("/token/new")
async def new_token() -> Dict[str, str]:
	return {"verify_token": secrets.token_urlsafe(24)}


@app.post("/test/send")
async def test_send(body: SendTestRequest) -> Dict[str, Any]:
	try:
		await ig_api.send_text_message(recipient_id=body.recipient_id, text=body.text)
		return {"ok": True}
	except Exception as e:
		return {"ok": False, "error": str(e)}


@app.get("/webhook")
async def verify_webhook(request: Request) -> Response:
	"""Meta Webhook verification endpoint.
	Meta sends hub.mode, hub.verify_token, hub.challenge as query params.
	"""
	params = dict(request.query_params)
	mode = params.get("hub.mode")
	verify_token = params.get("hub.verify_token")
	challenge = params.get("hub.challenge")

	if mode == "subscribe" and verify_token == VERIFY_TOKEN and challenge is not None:
		return Response(content=challenge, media_type="text/plain", status_code=status.HTTP_200_OK)
	return Response(status_code=status.HTTP_403_FORBIDDEN)


def _extract_text_events(payload: Dict[str, Any]) -> List[Dict[str, str]]:
	"""Extract text message events from IG/Messenger-style webhook payloads.
	Supports both entry.messaging[] and entry.changes[].value.messages[].
	Returns list of {sender_id, recipient_id, text}.
	"""
	events: List[Dict[str, str]] = []
	object_type = payload.get("object")
	for entry in payload.get("entry", []):
		# Messenger/IG unified messaging style
		for msg_event in entry.get("messaging", []) or []:
			sender_id = msg_event.get("sender", {}).get("id")
			recipient_id = msg_event.get("recipient", {}).get("id")
			message = msg_event.get("message", {})
			text = message.get("text")
			if sender_id and text:
				events.append({"sender_id": sender_id, "recipient_id": recipient_id or "", "text": text})

		# Instagram-specific changes format
		for change in entry.get("changes", []) or []:
			value = change.get("value", {})
			if value.get("messaging_product") == "instagram":
				for message in value.get("messages", []) or []:
					sender_id = message.get("from")
					text = message.get("text")
					recipient_id = value.get("id") or ""
					if isinstance(text, dict):
						text = text.get("body")
					if sender_id and text:
						events.append({"sender_id": sender_id, "recipient_id": recipient_id, "text": text})
	return events


def _dm_agent_reply(user_text: str) -> str:
	"""Very simple rule-based reply using our persona guide.
	Later, replace with an LLM-backed agent with guardrails.
	"""
	lower = user_text.strip().lower()
	if any(k in lower for k in ["business", "collab", "press", "sponsor"]):
		return (
			"Thanks for reaching out about collaborations! Please email press@yourdomain.com with brief, deliverables, and budget."
		)
	if "routine" in lower:
		return (
			"I can build a quick routine for you. Reply with skin type (oily/dry/combo/sensitive) + budget ($/$$/$$$)."
		)
	if any(k in lower for k in ["list", "links", "shop", "buy"]):
		return (
			"Affiliate: I may earn a commission. See link in bio for today’s picks, or say your budget for tailored recs."
		)
	if any(k in lower for k in ["help", "hi", "hello", "hey"]):
		return (
			"Hey! I’m your AI recs-buddy. Tell me what you’re looking for (skin, hair, or everyday finds)."
		)
	# Default helpful reply
	return (
		"Got it! Do you want dupes, routines, or today’s top deals? Say ‘ROUTINE’, ‘DUPES’, or ‘DEALS’."
	)


@app.post("/webhook")
async def receive_webhook(request: Request) -> Response:
	payload = await request.json()
	# Basic logging for debug
	print("Incoming webhook:", json.dumps(payload)[:2000])

	# Acknowledge quickly to avoid retries
	events = _extract_text_events(payload)
	for evt in events:
		try:
			reply = _dm_agent_reply(evt["text"]) 
			await ig_api.send_text_message(recipient_id=evt["sender_id"], text=reply)
		except Exception as e:
			print("Error sending message:", e)

	return Response(status_code=status.HTTP_200_OK)


if __name__ == "__main__":
	import uvicorn
	uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
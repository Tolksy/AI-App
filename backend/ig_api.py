import os
from typing import Optional

import httpx


class InstagramAPI:
	def __init__(self, page_access_token: str, graph_api_version: str = "v20.0") -> None:
		self.page_access_token = page_access_token
		self.graph_api_version = graph_api_version
		self.base_url = f"https://graph.facebook.com/{self.graph_api_version}"

	async def send_text_message(self, recipient_id: str, text: str) -> None:
		if not self.page_access_token:
			raise RuntimeError("PAGE_ACCESS_TOKEN is not set")
		url = f"{self.base_url}/me/messages"
		params = {"access_token": self.page_access_token}
		payload = {
			"messaging_type": "RESPONSE",
			"recipient": {"id": recipient_id},
			"message": {"text": text[:2000]},
		}
		async with httpx.AsyncClient(timeout=15.0) as client:
			resp = await client.post(url, params=params, json=payload)
			if resp.status_code >= 400:
				raise RuntimeError(f"Send API error {resp.status_code}: {resp.text}")
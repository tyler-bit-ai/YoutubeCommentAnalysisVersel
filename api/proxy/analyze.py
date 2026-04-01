import json
from http.server import BaseHTTPRequestHandler
import urllib.error

from api._lib.env import get_required_env
from api._lib.responses import send_error_json, send_json, send_options
from api._lib.upstream import build_json_request, fetch_upstream_json, parse_http_error

A15T_API_URL = "https://api.platform.a15t.com/v1/chat/completions"


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length)
            client_req = json.loads(raw_body.decode("utf-8"))
            api_key = get_required_env("A15T_API_KEY")

            request = build_json_request(
                A15T_API_URL,
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                },
                payload={
                    "model": client_req.get("model", "openai/gpt-4o-mini-2024-07-18"),
                    "messages": client_req.get("messages", []),
                    "temperature": client_req.get("temperature", 0.7)
                }
            )
            payload, status_code = fetch_upstream_json(request)
            send_json(self, payload, status_code)
        except urllib.error.HTTPError as error:
            message, status_code = parse_http_error(error)
            send_error_json(self, message, status_code)
        except Exception as error:
            send_error_json(self, str(error), 500)

    def do_OPTIONS(self):
        send_options(self)

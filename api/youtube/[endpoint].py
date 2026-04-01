from http.server import BaseHTTPRequestHandler
import urllib.error
import urllib.parse

from api._lib.env import get_required_env
from api._lib.responses import send_error_json, send_json, send_options
from api._lib.upstream import build_json_request, fetch_upstream_json, parse_http_error

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"
ALLOWED_ENDPOINTS = {"search", "videos", "channels", "commentThreads", "comments"}


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            youtube_api_key = get_required_env("YOUTUBE_API_KEY")
            parsed_url = urllib.parse.urlparse(self.path)
            endpoint = parsed_url.path.rstrip("/").split("/")[-1]
            if endpoint not in ALLOWED_ENDPOINTS:
                send_error_json(self, "Not Found", 404)
                return

            query_params = urllib.parse.parse_qs(parsed_url.query, keep_blank_values=True)
            query_params["key"] = [youtube_api_key]
            upstream_query = urllib.parse.urlencode(query_params, doseq=True)
            upstream_url = f"{YOUTUBE_API_BASE}/{endpoint}?{upstream_query}"

            request = build_json_request(upstream_url, headers={})
            payload, status_code = fetch_upstream_json(request)
            send_json(self, payload, status_code)
        except urllib.error.HTTPError as error:
            message, status_code = parse_http_error(error)
            send_error_json(self, message, status_code)
        except Exception as error:
            send_error_json(self, str(error), 500)

    def do_OPTIONS(self):
        send_options(self)

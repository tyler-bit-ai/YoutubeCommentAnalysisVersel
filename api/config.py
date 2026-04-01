from http.server import BaseHTTPRequestHandler

from api._lib.env import is_configured
from api._lib.responses import send_json, send_options


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        send_json(self, {
            "youtubeConfigured": is_configured("YOUTUBE_API_KEY"),
            "a15tConfigured": is_configured("A15T_API_KEY")
        })

    def do_OPTIONS(self):
        send_options(self)

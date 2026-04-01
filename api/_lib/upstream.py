import json
import urllib.error
import urllib.request

def build_json_request(url, method="GET", headers=None, payload=None):
    request_headers = headers or {}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    return urllib.request.Request(url, data=data, headers=request_headers, method=method)


def fetch_upstream_json(request):
    with urllib.request.urlopen(request) as response:
        raw_body = response.read().decode("utf-8")
        return json.loads(raw_body), response.status


def parse_http_error(error):
    body = error.read().decode("utf-8")
    try:
        payload = json.loads(body)
        message = payload.get("error", {}).get("message", body)
        return message, error.code
    except json.JSONDecodeError:
        return body, error.code

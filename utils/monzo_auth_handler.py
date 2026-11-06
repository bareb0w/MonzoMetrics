import requests
import webbrowser
import urllib.parse
import http.server
import socketserver
import json
from dotenv import load_dotenv
from os import getenv
import secrets

csrf_token = secrets.token_urlsafe(32)

load_dotenv()
# ==== CONFIG ====
REDIRECT_URI = getenv("REDIRECT_URI")
TOKEN_FILE = "monzo_tokens.json"
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
# ================

AUTH_URL = "https://auth.monzo.com"
TOKEN_URL = "https://api.monzo.com/oauth2/token"


class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            code = params["code"][0]
            print(f"\n✅ Got auth code: {code}")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<h1>Monzo auth successful!</h1><p>You can close this window.</p>")

            # Exchange the code for tokens
            data = {
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code
            }
            r = requests.post(TOKEN_URL, data=data)
            r.raise_for_status()
            tokens = r.json()
            print("\n✅ Got tokens:", tokens)

            save_token(tokens)
            print(f"\n💾 Tokens saved to {TOKEN_FILE}")
        else:
            self.send_response(400)
            self.end_headers()


def get_token_from_json():
    with open(TOKEN_FILE, "r") as f:
        tokens = json.load(f)
    return tokens


def save_token(tokens):
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)


def get_access_token():
    return get_token_from_json().get("access_token")


def refresh_access():

    url = "https://api.monzo.com/oauth2/token"
    old_tokens = get_token_from_json()
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": old_tokens.get("refresh_token")
    }

    response = requests.post(url, data=data)

    response.raise_for_status()

    tokens = response.json()
    save_token(tokens)
    print("Access token refreshed successfully!")


def main():
    # Start local server to catch the redirect
    with socketserver.TCPServer(("localhost", 8081), OAuthHandler) as httpd:
        # Build URL
        url = (
            f"{AUTH_URL}/?"
            f"client_id={CLIENT_ID}"
            f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
            f"&response_type=code"
            f"&state={csrf_token}"
        )
        print(f"\n🌍 Opening browser for Monzo login: {url}\n")
        webbrowser.open(url)

        print("Waiting for redirect with auth code...")
        httpd.handle_request()  # handle ONE request then stop


if __name__ == "__main__":
    # main()
    refresh_access()

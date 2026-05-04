#!/usr/bin/env python3
"""Telegram delivery — send brand kit files via Telegram."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def send_message(token: str, chat_id: str, text: str) -> dict:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    body = json.dumps({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def send_document(token: str, chat_id: str, file_path: str, caption: str = "") -> dict:
    boundary = "----FormBoundary7MA4YWxkTrZu0gW"
    url = f"https://api.telegram.org/bot{token}/sendDocument"

    filename = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        file_data = f.read()

    body_lines = []
    body_lines.append(f"--{boundary}".encode())
    body_lines.append(f'Content-Disposition: form-data; name="chat_id"'.encode())
    body_lines.append(b"")
    body_lines.append(chat_id.encode())

    if caption:
        body_lines.append(f"--{boundary}".encode())
        body_lines.append(f'Content-Disposition: form-data; name="caption"'.encode())
        body_lines.append(b"")
        body_lines.append(caption.encode())

    body_lines.append(f"--{boundary}".encode())
    body_lines.append(
        f'Content-Disposition: form-data; name="document"; filename="{filename}"'.encode()
    )
    body_lines.append(b"Content-Type: application/octet-stream")
    body_lines.append(b"")
    body_lines.append(file_data)
    body_lines.append(f"--{boundary}--".encode())

    body = b"\r\n".join(body_lines) + b"\r\n"

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Telegram delivery — send brand kit files"
    )
    parser.add_argument(
        "--token",
        default=None,
        help="Telegram bot token (or set TELEGRAM_BOT_TOKEN env var)",
    )
    parser.add_argument("--chat-id", required=True, help="Telegram chat ID")
    parser.add_argument("--files", nargs="+", required=True, help="File paths to send")
    parser.add_argument(
        "--message", default=None, help="Optional text message to send first"
    )
    args = parser.parse_args()

    token = args.token or os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print(
            "ERROR: Telegram bot token required (--token or TELEGRAM_BOT_TOKEN env var)",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.message:
        try:
            send_message(token, args.chat_id, args.message)
            print(f"[+] Message sent")
        except urllib.error.URLError as e:
            print(f"ERROR: Message failed: {e}", file=sys.stderr)

    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"[-] File not found: {file_path}")
            continue
        try:
            result = send_document(token, args.chat_id, file_path)
            if result.get("ok"):
                print(f"[+] Sent: {file_path}")
            else:
                print(
                    f"[-] Failed: {file_path} — {result.get('description', 'unknown error')}",
                    file=sys.stderr,
                )
        except urllib.error.URLError as e:
            print(f"[-] Error sending {file_path}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"[-] Error sending {file_path}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()

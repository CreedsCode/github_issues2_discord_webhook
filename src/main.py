from flask import Flask, request
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)


@app.route('/github', methods=['POST'])
def idk():
    data = json.loads(request.data)
    issue_action = data["action"]

    if issue_action != "opened":
        return "Ok"

    issue_data = data["issue"]
    username = issue_data["user"]["login"]
    issue_title = issue_data["title"]
    user_picture = issue_data["user"]["avatar_url"]
    issue_url = issue_data["html_url"]
    user_url = issue_data["user"]["html_url"]
    repository = data["repository"]["full_name"]
    issue_id = issue_data["number"]
    created_at = issue_data["created_at"]

    data = {
        "content": "New Attackerthon submission!",
        "embeds": [
            {
                "title": issue_title,
                "url": issue_url,
                "color": 14483456,
                "author": {
                    "name": username,
                    "url": user_url,
                    "icon_url": user_picture
                },
                "footer": {
                    "text": f"Repository {repository}, issue: {issue_id}"
                },
                "timestamp": created_at
            }
        ],
        "username": "Attackerthon Issue Tracker",
        "attachments": []

    }
    push = requests.post(url=os.getenv("DISCORD_WEBHOOK"),
                         headers={"Content-Type": "application/json"},
                         json=data)
    print("send", push)
    return "OK"


if __name__ == '__main__':
    app.run(port=3000)

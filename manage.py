import json
import os
import pickle
import secrets
from functools import wraps
from threading import Timer

from bottle import redirect, request, response, route, run, template
# Gmail API utils
from google_auth_oauthlib.flow import Flow

import task
from logger import logger

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ["https://mail.google.com/"]

SECRET = secrets.token_urlsafe(16)


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def restricted(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.get_cookie("access", secret=SECRET):
            return func(*args, **kwargs)
        else:
            return redirect("/login")

    return wrapper


@route("/login", method=["GET", "POST"])
def login():
    if request.method == "GET":
        return template("login")
    elif request.method == "POST":
        if request.forms.get("pass") == os.environ["PASSWORD"]:
            response.set_cookie("access", "true", secret=SECRET)
        return redirect("/")


@route("/", method=["GET", "POST"])
@restricted
def index():
    global flow
    if request.method == "GET":
        if os.path.exists("token.pickle"):
            logger.info("token.pickle already exists, redirecting to dashboard")
            return redirect("/dashboard")
        logger.warn("token.pickle was not found, Oauth flow needed")
        return template("index")
    elif request.method == "POST":
        creds_config = json.load(request.files.get("creds").file)
        flow = Flow.from_client_config(
            creds_config, SCOPES, redirect_uri=creds_config["web"]["redirect_uris"][0]
        )
        auth_url, _ = flow.authorization_url()
        return redirect(auth_url)


@route("/callback")
@restricted
def callback():
    flow.fetch_token(code=request.query.code)
    logger.info("Fetched code successfully, creating token.pickle")
    creds = flow.credentials
    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)

    logger.info("Starting RepeatTimer to run main task every 3 minutes")
    RepeatTimer(3 * 60, task.main).start()
    return redirect("/dashboard")


@route("/dashboard")
@restricted
def dashboard():
    return template("dashboard")


@route("/logs")
@restricted
def logs():
    with open("app.log") as f:
        return f.read().replace("\n", "<br>")


@route("/force-task", method="POST")
@restricted
def force_task():
    logger.info("Forced task recieved")
    task.main()
    response.status = 200
    return response


if __name__ == "__main__":
    if os.path.exists("token.pickle"):
        logger.info("Starting RepeatTimer to run main task every 3 minutes")
        RepeatTimer(3 * 60, task.main).start()
    logger.info("Starting server")
    run(host="0.0.0.0", port=int(os.environ["PORT"]))

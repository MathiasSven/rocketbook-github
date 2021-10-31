import base64
import os
import pickle
from datetime import datetime

# for working with github
from github import Github
from github.InputGitTreeElement import InputGitTreeElement
from google.auth.transport.requests import Request
# Gmail API utils
from googleapiclient.discovery import build

from logger import logger


def gmail_authenticate():
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)

    if not creds.valid:
        logger.warning("creds no longer valid, refreshing...")
        creds.refresh(Request())

    return build("gmail", "v1", credentials=creds)


def search_messages(service, query):
    result = service.users().messages().list(userId="me", q=query).execute()
    messages = []
    if "messages" in result:
        messages.extend(result["messages"])
    while "nextPageToken" in result:
        page_token = result["nextPageToken"]
        result = (
            service.users()
            .messages()
            .list(userId="me", q=query, pageToken=page_token)
            .execute()
        )
        if "messages" in result:
            messages.extend(result["messages"])
    return messages


def commit_push(files):
    g = Github(os.environ["GITHUB_TOKEN"])
    repo = g.get_repo(os.environ["GITHUB_REPO"])
    ref = repo.get_git_ref(os.environ["GITHUB_BRANCH"])
    commit = repo.get_commit(ref.object.sha)
    blobs = []
    for file in files:
        blobs.append(
            {
                "name": file["filename"],
                "blob": repo.create_git_blob(file["rawdata"], "base64"),
            }
        )
    tree = commit.commit.tree
    new_tree = repo.create_git_tree(
        [
            InputGitTreeElement(
                f"{os.environ.get('GITHUB_DESTIONATION', '')}/{file['name']}",
                "100644",
                "blob",
                sha=file["blob"].sha,
            )
            for file in blobs
        ],
        tree,
    )
    new_commit = repo.create_git_commit(
        f"rocketbook upload: {str(datetime.utcnow()).split('.')[0]}",
        new_tree,
        [commit.commit],
    )
    ref.edit(new_commit.sha)


def main():
    logger.info("Starting main task")
    service = gmail_authenticate()
    logger.info("Authenticated")
    results = search_messages(service, "from:notes@email.getrocketbook.com")
    logger.info(f"Found {len(results)} new emails")
    files = []
    for message in results:
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=message["id"], format="full")
            .execute()
        )
        payload = msg["payload"]
        headers = payload.get("headers")
        relevant_headers = {"From", "To", "Subject", "Date"}
        headers = {
            header["name"].lower(): header["value"].lower()
            for header in headers
            if header["name"] in relevant_headers
        }

        logger.info(headers)

        parts = payload.get("parts")
        supported = {"image/jpeg", "application/pdf"}
        for part in filter(lambda part: part["mimeType"] in supported, parts):
            filename = part.get("filename")
            logger.info(f"Found supported file: {filename}")
            body = part.get("body")

            attachment_id = body.get("attachmentId")
            attachment = (
                service.users()
                .messages()
                .attachments()
                .get(id=attachment_id, userId="me", messageId=message["id"])
                .execute()
            )
            data = attachment.get("data")
            rawdata = base64.b64encode(base64.urlsafe_b64decode(data)).decode("utf-8")
            files.append({"filename": filename, "rawdata": rawdata})
    if files:
        logger.info("Pushing new items to repo")
        commit_push(files)
    if results:
        logger.info("Deleting pushed emails")
        service.users().messages().batchDelete(
            userId="me", body={"ids": [msg["id"] for msg in results]}
        ).execute()
    logger.info("Finished main task")

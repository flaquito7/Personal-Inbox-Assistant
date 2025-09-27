from msal import PublicClientApplication
import requests
import os

CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
SCOPES = ["Mail.Read"]

def get_emails():
    app = PublicClientApplication(CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}")

    accounts = app.get_accounts()
    result = app.acquire_token_silent(SCOPES, account=accounts[0]) if accounts else None

    if not result:
        flow = app.initiate_device_flow(scopes=SCOPES)
        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)

    headers = {"Authorization": "Bearer " + result["access_token"]}
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages?$top=10",
        headers=headers
    )
    return response.json()["value"]

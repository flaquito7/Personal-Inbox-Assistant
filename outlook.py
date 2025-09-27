from msal import PublicClientApplication, SerializableTokenCache
import requests
import os
import atexit

CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
SCOPES = ["Mail.Read"]

def get_emails():
    # Create persistent token cache
    cache = SerializableTokenCache()
    if os.path.exists("msal_token_cache.json"):
        cache.deserialize(open("msal_token_cache.json", "r").read())
    
    atexit.register(lambda: open("msal_token_cache.json", "w").write(cache.serialize()) if cache.has_state_changed else None)
    
    # Try using consumers endpoint specifically for personal accounts
    app = PublicClientApplication(
        CLIENT_ID, 
        authority="https://login.microsoftonline.com/consumers",
        token_cache=cache
    )

    # Try to get token silently first (using refresh token)
    accounts = app.get_accounts()
    result = app.acquire_token_silent(SCOPES, account=accounts[0]) if accounts else None

    if not result:
        print("🔐 Authentication required - this should only happen once!")
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "error" in flow:
            print("Device flow failed:")
            print(flow)
            return []
        print(flow["message"])
        print("⏳ Waiting for you to complete authentication...")
        print("🔄 This will automatically continue once you authenticate")
        
        # Give more time for user to authenticate
        result = app.acquire_token_by_device_flow(flow)
        
        if result and "access_token" in result:
            print("✅ Authentication successful! Token will be saved for future use.")
        else:
            print("❌ Authentication failed or timed out. Please try again.")

    if not result or "access_token" not in result:
        print("❌ Authentication failed!")
        if result:
            error_desc = result.get('error_description', 'Unknown error')
            if 'authorization_pending' in error_desc:
                print("⏳ Still waiting for authentication - please complete it in your browser")
            else:
                print("Error details:", result)
        return []

    print("Authentication successful!")
    print(f"Token type: {result.get('token_type', 'Unknown')}")
    print(f"Scopes: {result.get('scope', 'Unknown')}")
    id_token_claims = result.get('id_token_claims', {})
    if isinstance(id_token_claims, dict):
        account_info = id_token_claims.get('preferred_username', 'Unknown')
    else:
        account_info = 'Unknown'
    print(f"Account info: {account_info}")

    headers = {"Authorization": "Bearer " + result["access_token"]}
    
    # Get emails from both Inbox and Junk folders
    all_emails = []
    folders = [
        ("Inbox", "Inbox"),
        ("Junk", "JunkEmail")  # Microsoft Graph uses "JunkEmail" for junk folder
    ]
    
    for folder_name, folder_id in folders:
        print(f"📂 Checking {folder_name} folder...")
        response = requests.get(
            f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}/messages?$top=10&$filter=isRead eq false",
            headers=headers
        )
        
        print(f"{folder_name} response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                folder_emails = response.json()["value"]
                print(f"Found {len(folder_emails)} unread emails in {folder_name}")
                # Add folder info to each email for identification
                for email in folder_emails:
                    email['_folder'] = folder_name
                all_emails.extend(folder_emails)
            except Exception as e:
                print(f"Failed to parse {folder_name} JSON: {e}")
        else:
            print(f"{folder_name} API call failed with status {response.status_code}")
    
    print(f"📧 Total unread emails found: {len(all_emails)}")
    return all_emails

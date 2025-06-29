import os.path
import base64
import re
import html
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_email_body(payload):
    """
    Recursively search for the email body, prioritizing plain text,
    but falling back to a cleaned HTML version if necessary.
    """
    # Use a stack for an iterative DFS search to avoid recursion depth issues
    parts_to_search = [payload]
    plain_text_body = None
    html_body = None

    while parts_to_search:
        part = parts_to_search.pop(0)
        mime_type = part.get('mimeType', '')
        body = part.get('body', {})
        data = body.get('data')

        if not data:
            # If the part is a container for other parts, add them to the search list
            if 'parts' in part:
                parts_to_search.extend(part['parts'])
            continue

        # Prioritize finding the plain text version
        if mime_type == 'text/plain':
            plain_text_body = base64.urlsafe_b64decode(data).decode('utf-8')
            # Once we find plain text, we can stop searching.
            break
        # If no plain text, keep the first HTML version we find as a fallback
        elif mime_type == 'text/html' and not html_body:
            html_body = base64.urlsafe_b64decode(data).decode('utf-8')

    if plain_text_body:
        return plain_text_body
    
    if html_body:
        # If we only found an HTML body, clean it for readability.
        # 1. Decode HTML entities (e.g., &amp; -> &)
        text = html.unescape(html_body)
        # 2. Remove all HTML tags
        clean_text = re.sub(r'<[^>]+>', '', text)
        return clean_text.strip()

    return None

def main():
    """
    Connects to the Gmail API, fetches emails from a specific sender and date range,
    and saves their content to a text file.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        # Updated query as per your request.
        query = 'from:newsletter@aisecret.us after:2025/06/21 before:2025/06/29'
        result = service.users().messages().list(userId='me', q=query).execute()
        messages = result.get('messages', [])

        if not messages:
            print("No messages found for the specified query.")
            return

        print(f"Found {len(messages)} messages. Saving content to email_content.txt...")

        with open('email_content_ai_secret.txt', 'w', encoding='utf-8') as output_file:
            for msg_info in messages:
                msg = service.users().messages().get(userId='me', id=msg_info['id']).execute()
                payload = msg.get('payload', {})
                headers = payload.get('headers', [])
                
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')

                output_file.write(f"--- Email from: {sender} | Subject: {subject} ---\n\n")

                # --- MODIFICATION START ---
                # Use the new robust function to get the email body
                email_text = get_email_body(payload)
                if email_text:
                    output_file.write(email_text)
                    output_file.write("\n\n")
                else:
                    output_file.write("Could not find a readable body for this email.\n\n")
                # --- MODIFICATION END ---

        print("Successfully saved email content to email_content_agent_ai.txt")

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()

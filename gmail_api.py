import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """
    Connects to the Gmail API, fetches emails from a specific sender and date range,
    and saves their content to a text file.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Build the Gmail API service
        service = build('gmail', 'v1', credentials=creds)

        # Define the search query.
        # Emails from a specific address, after Jan 1, 2024, and before Jan 31, 2024.
        # You can change 'user@example.com', and the dates.
        query = 'from:hi@mail.theresanaiforthat.com after:2025/06/22 before:2025/06/24'
        
        # Call the Gmail API to list the messages
        result = service.users().messages().list(userId='me', q=query).execute()
        messages = result.get('messages', [])

        if not messages:
            print("No messages found.")
            return

        print(f"Found {len(messages)} messages. Saving content to email_content.txt...")

        with open('email_content.txt', 'w', encoding='utf-8') as output_file:
            for msg_info in messages:
                msg = service.users().messages().get(userId='me', id=msg_info['id']).execute()
                
                # Get the message payload and headers
                payload = msg.get('payload', {})
                headers = payload.get('headers', [])
                
                # Extract subject and sender for context
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')

                output_file.write(f"--- Email from: {sender} | Subject: {subject} ---\n\n")

                # Find the plain text part of the email body
                if 'parts' in payload:
                    for part in payload['parts']:
                        if part['mimeType'] == 'text/plain':
                            data = part['body'].get('data')
                            if data:
                                text = base64.urlsafe_b64decode(data).decode('utf-8')
                                output_file.write(text)
                                output_file.write("\n\n")
                                break
                # Handle emails with no parts (simple text body)
                else:
                    data = payload.get('body', {}).get('data')
                    if data:
                        text = base64.urlsafe_b64decode(data).decode('utf-8')
                        output_file.write(text)
                        output_file.write("\n\n")

        print("Successfully saved email content to email_content.txt")

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()


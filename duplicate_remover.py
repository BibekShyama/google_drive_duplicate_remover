import webbrowser
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle

# Define the scope for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google_drive():
    """Authenticate the user and create a Google Drive service instance using Brave Browser."""
    creds = None

    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # executable browser path
    webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))

    # Authenticate every time, without saving credentials to pickle
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    # Open Brave Browser for authentication
    flow.run_local_server(open_browser=True, browser='brave')
    creds = flow.credentials

    return build('drive', 'v3', credentials=creds)


def get_all_files(service, folder_id):
    """Retrieve all files from a specific Google Drive folder."""
    files = []
    page_token = None
    while True:
        response = service.files().list(
            q=f"('{folder_id}' in parents) and (mimeType contains 'image/' or mimeType contains 'video/')",
            spaces='drive',
            fields="nextPageToken, files(id, name, md5Checksum, mimeType)",
            pageToken=page_token
        ).execute()
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files


def delete_file(service, file_id):
    """Delete a file from Google Drive."""
    try:
        service.files().delete(fileId=file_id).execute()
        print(f"Deleted file with ID: {file_id}")
    except Exception as e:
        print(f"Failed to delete file {file_id}: {e}")

def find_and_delete_duplicates(service, folder_id):
    """Find and delete duplicate photos/videos based on MD5 checksum in a specific folder."""
    files = get_all_files(service, folder_id)
    print(f"Total files retrieved: {len(files)}")

    checksum_map = {}
    failed_deletions = set()

    for file in files:
        checksum = file.get('md5Checksum')
        file_id = file.get('id')
        file_name = file.get('name')

        if checksum:
            if checksum in checksum_map:
                if file_id in failed_deletions:
                    print(f"Skipping previously failed file: {file_name} ({file_id})")
                    continue
                print(f"Duplicate found: {file_name} ({file_id})")
                try:
                    delete_file(service, file_id)
                except Exception as e:
                    print(f"Failed to delete file {file_id}: {e}")
                    failed_deletions.add(file_id)
            else:
                checksum_map[checksum] = file_id
        else:
            print(f"File {file_name} does not have an MD5 checksum. Skipping.")




    checksum_map = {}
    for file in files:
        checksum = file.get('md5Checksum')
        if checksum:
            if checksum in checksum_map:
                print(f"Duplicate found: {file['name']} ({file['id']})")
                delete_file(service, file['id'])
            else:
                checksum_map[checksum] = file['id']
        else:
            print(f"File {file['name']} does not have an MD5 checksum. Skipping.")

def main():
    """Main function to execute the script."""
    service = authenticate_google_drive()
    folder_id = "<folder_id>"  # Replace with your Google Drive folder ID
    find_and_delete_duplicates(service, folder_id)


if __name__ == '__main__':
    main()


from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_drive(title,file_path,service_account_file,parent_folder_id):

    # Authenticate and create a Google Drive API service instance
    creds = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    drive_service = build('drive', 'v3', credentials=creds)

    # File metadata with the fixed parent folder ID
    file_metadata = {
        'name': title,
        'mimeType': 'video/mp4',  # Adjust according to your file type
        'parents': [parent_folder_id]
    }

    # Media file upload
    media = MediaFileUpload(file_path, mimetype='video/mp4')

    # Upload file
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'  # Request webViewLink field for the file
    ).execute()

    # Get the webViewLink (full link) of the uploaded file
    file_link = file.get('webViewLink')

    # Return the full link to the uploaded file
    return file_link


if __name__ == '__main__':

    title = 'SampleVideo'  # your file title
    file_path='sample.mp4' # your file path
    parent_folder_id = 'your-google-drive-folder-id' # the drive folder where video has to be uploaded
    service_account_file = 'service_account_file.json'  # path of your google service account's json file

    video_link = upload_to_drive(title,file_path,service_account_file,parent_folder_id)
    print(video_link)
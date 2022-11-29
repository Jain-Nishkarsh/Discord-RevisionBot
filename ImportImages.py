def As_Function():
    from googleapiclient.http import MediaIoBaseDownload
    from Google import Create_Service
    import os
    import io
    import pandas as pd

    CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo_File.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    RevisionThings_folder_id = '1OUAsmg2xMmAIpyZEJiICsa7xUvoDM4uo'
    Questions_folder_id = '1xZFnXvri0LCn64QxR4Goe33l58SYYlD5'

    query = f"parents = '{RevisionThings_folder_id}'"
    response = service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')
    while nextPageToken:
        response = service.files().list(q=query).execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')
    df = pd.DataFrame(files)

    query1 = f"parents = '{Questions_folder_id}'"
    response1 = service.files().list(q=query1).execute()
    files1 = response1.get('files')
    nextPageToken1 = response1.get('nextPageToken')
    while nextPageToken1:
        response1 = service.files().list(q=query1).execute()
        files.extend(response1.get('files'))
        nextPageToken1 = response1.get('nextPageToken')
    df1 = pd.DataFrame(files1)

    RevisionThings_file_ids = df['id'].to_list()
    RevisionThings_file_names = df['name'].to_list()

    Questions_file_ids = df1['id'].to_list()
    Questions_file_names = df1['name'].to_list()

    Questions_Folder_names = os.listdir('Questions')
    RevisionThings_Folder_names = os.listdir('RevisionThings')

    for file_id, file_name in zip(RevisionThings_file_ids,
                                  RevisionThings_file_names):
        if file_name not in RevisionThings_Folder_names:
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fd=fh, request=request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print('Donwload progress {0}'.format(status.progress() * 100))

            fh.seek(0)
            with open(os.path.join('./RevisionThings', file_name), 'wb') as f:
                f.write(fh.read())
                f.close()

    for file_id, file_name in zip(Questions_file_ids, Questions_file_names):
        if file_name not in Questions_Folder_names:
            request1 = service.files().get_media(fileId=file_id)
            fh1 = io.BytesIO()
            downloader1 = MediaIoBaseDownload(fd=fh1, request=request1)
            done1 = False
            while not done1:
                status1, done1 = downloader1.next_chunk()
                print('Donwload progress {0}'.format(status1.progress() * 100))

            fh1.seek(0)
            with open(os.path.join('./Questions', file_name), 'wb') as f:
                f.write(fh1.read())
                f.close()

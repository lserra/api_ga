# -*- encoding: UTF-8 -*-

"""
Downloading unsampled reports created in Google Analytics, using the Google Drive API.
Created by: Laercio Serra (laercio.serra@gmail.com)
Created on: 06/06/2017
"""

import io
import webbrowser
import httplib2 as http
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from oauth2client import file, client, tools


def list_files(drive_service):
    # List all files found
    files = drive_service.files().list().execute()
    print "List of files"
    print "-" * 50
    for f in files['files']:
        print f['name']

    return files


def download_file(files, drive_service):
    # Download all files found
    print "\n<-- Downloading all files found -->"
    print "-" * 50
    for f in files['files']:
        if "google-apps" in f['mimeType']:
            pass  # skip google files
        else:
            file_id = f['id']
            file_name = f['name']
            request = drive_service.files().get_media(fileId=file_id)
            fh = io.FileIO(file_name, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            print "\n>> File     => %s" % (file_name)
            while done is False:
                status, done = downloader.next_chunk()
                print ">> Download => %d%%." % int(status.progress() * 100)


def main():
    # Define the auth scopes to request.
    # You can copy your credentials from the console
    # https://console.developers.google.com
    client_secret = '/home/df/Documents/api-ga/client_secret.json'
    flow = client.flow_from_clientsecrets(
      client_secret,
      scope='https://www.googleapis.com/auth/drive.readonly',
      redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    auth_uri = flow.step1_get_authorize_url()
    webbrowser.open(auth_uri)

    print auth_uri

    auth_code = raw_input('Enter the auth code: ')

    credentials = flow.step2_exchange(auth_code)
    http_auth = credentials.authorize(http.Http())

    drive_service = build('drive', 'v3', http_auth)

    # List all files found
    files = list_files(drive_service)

    # Download all files found
    download_file(files, drive_service)


if __name__ == '__main__':
    main()

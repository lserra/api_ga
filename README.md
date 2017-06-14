# api_ga
Using API's from Google Analytics/Drive to extracting data unsampled
(unsampled reports).

### How work
-------------
The unsampled reports created are available to download on Google Drive.
An unsampled report is submitted to Google Analytics by APIs.
So, this report is processed by Google and then is available to download
on Google Drive.
To download this report from Google Drive also is used the APIs.
In both cases, I'm using the [google-api-client](https://github.com/google/google-api-python-client) (for python).

### Requirements
----------------
- python==2.7
- google-api-python-client==1.6.2
- httplib2==0.10.3
- oauth2client==4.1.0
- pyOpenSSL==16.2.0

_You can use the following command:_ pip install -r requirements.txt

### Authentication
------------------
To submit an unsampled report to Google Analytics the API is
authenticated using a service account.
To download an unsampled report from Google Drive the API is
authenticated using an user account.

For both cases, is necessary the JSON file (_client_secret.json_).
This file you can generate in Google API Console.

__These files were created for this specific project, but I can't share/
public them here because contains confidential data.__

### The project
---------------
- __get_profile_tvg.py__

_Returns Analytics data for a view (profile) in GA, using the API.
The authentication method used by this script is service account._

- __ins_unsampled_reports_tvg.py__

_Create a new unsampled report data in GA, using the API.
The authentication method used by this script is service account._

- __del_unsampled_reports_tvg.py__

_Delete an unsampled report data in GA, using the API.
The authentication method used by this script is service account._

- __list_unsampled_reports_tvg.py__

_List all unsampled reports to which the user has access in GA, using the API.
The authentication method used by this script is service account._

- __get_unsampled_reports.py__

_Returns a single unsampled report in GA, using the API.
The authentication method used by this script is service account._

- __download_unsampled_reports_tvg.py__

_Download unsampled reports created in GA, using the API.
The authentication method used by this script is user account._

### More information
--------------------
For more details about how to use this APIs:
- [Google Analytics](https://developers.google.com/analytics/)
- [Google Drive](https://developers.google.com/drive/v3/web/about-sdk)
- [OAuth](https://developers.google.com/api-client-library/python/guide/aaa_oauth)
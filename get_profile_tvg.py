# -*- encoding: UTF-8 -*-

"""
Returns Analytics data for a view (profile) in Google Analytics, using the Google Analytics API.
The authentication method used by this script is service account
Created by: Laercio Serra (laercio.serra@gmail.com)
Created on: 06/06/2017
"""


import apiclient as api
from oauth2client.service_account import ServiceAccountCredentials
import httplib2


def get_service(api_name, api_version, scope, key_file_location, service_account_email):
    """
    Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scope: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account p12 key file.
        service_account_email: The service account email address.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_p12_keyfile(service_account_email, key_file_location, scopes=scope)

    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    service = api.discovery.build(api_name, api_version, http=http)

    return service


def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(accountId=account).execute()

        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')

            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(accountId=account, webPropertyId=property).execute()

            if profiles.get('items'):
                # return the first view (profile) id.
                return profiles.get('items')[0].get('id')

    return None


def get_results(service, profile_id):
    # Use the Analytics Service Object to query the Core Reporting API
    # for the number of sessions within the past seven days.
    # Source1: https://developers.google.com/analytics/devguides/reporting/core/v3/reference#q_details
    # Source2: https://developers.google.com/analytics/devguides/config/mgmt/v3/unsampled-reports#use_cases
    return service.data().ga().get(ids='ga:' + profile_id,
                                   start_date='1daysAgo',
                                   end_date='today',
                                   metrics='ga:sessions').execute()


def print_results(results):
    # Print data nicely for the user.
    if results:
        print 'View (Profile): %s' % results.get('profileInfo').get('profileName')
        print 'Total Sessions: %s' % results.get('rows')[0][0]

    else:
        print 'No results found'


def get_list_unsampled_reports(service):
    # Note: This code assumes you have an authorized Analytics service object.
    # See the Unsampled Reports Developers Guide for details.

    # Requests a list of all Unsampled Reports for the authorized user.
    try:
        return service.management().unsampledReports().list(accountId='296593',
                                                            webPropertyId='UA-296593-56',
                                                            profileId='107283129').execute()

    except TypeError, error:
        # Handle errors in constructing a query.
        print 'There was an error in constructing your query : %s' % error

    except httplib2.HttpLib2Error, error:
        # Handle API errors.
        print ('There was an API error : %s' % error.message)


def print_list_unsampled_reports(reports):
    # Print data nicely for the user.
    if reports:
        reps = reports['items']
        print '\nTotal Unsampled Reports: %s' % len(reps)
        for rep in reps:
            r = rep
            print '>> [ %s ] => %s / %s / %s / %s' % (r['id'], r['title'], r['status'], r['created'], r['updated'])

        # The results of the list method are stored in the reports object.
        # The following code shows how to iterate through them.
        # for report in reports.get('items', []):
        #     driveDownloadDetails = report.get('driveDownloadDetails', {})
        #     cloudStorageDownloadDetails = report.get('cloudStorageDownloadDetails', {})
        #
        #     print 'Account Id            = %s' % report.get('accountId')
        #     print 'Property Id           = %s' % report.get('webPropertyId')
        #     print 'Report Id             = %s' % report.get('id')
        #     print 'Report Title          = %s' % report.get('title')
        #     print 'Report Kind           = %s' % report.get('kind')
        #     print 'Report start-date = %s' % report.get('start-date')
        #     print 'Report end-date = %s' % report.get('end-date')
        #     print 'Report metrics        = %s' % report.get('metrics')
        #     print 'Report dimensions = %s' % report.get('dimensions')
        #     print 'Report filters = %s' % report.get('filters')
        #     print 'Report Status         = %s\n' % report.get('status')
        #     print 'Report downloadType = %s' % report.get('downloadType')
        #     print 'Drive Document Id = %s' % driveDownloadDetails.get('document Id')
        #     print 'Cloud Bucket Id = %s' % cloudStorageDownloadDetails.get('bucketId')
        #     print 'Cloud Object Id = %s' % cloudStorageDownloadDetails.get('objectId')
        #     print 'Report Created = %s' % report.get('created')
        #     print 'Report Updated = %s' % report.get('updated')

    else:
        print 'No reports found'


def get_data_unsampled_reports(service):
    # Note: This code assumes you have an authorized Analytics service object.
    # See the Unsampled Reports Developer Guide for details.

    # Example #1:
    # This request gets an existing unsampled report.
    try:
        return service.management().unsampledReports().get(accountId='296593',
                                                           webPropertyId='UA-296593-56',
                                                           profileId='107283129',
                                                           unsampledReportId='9AWCqoS4T9iLA2Dy1hc0Ng').execute()

    except TypeError, error:
        # Handle errors in constructing a query.
        print 'There was an error in constructing your query : %s' % error

    except httplib2.HttpLib2Error, error:
        # Handle API errors.
        print ('There was an API error : %s : %s' % error.message)


def print_data_unsampled_reports(report):
    # Print data nicely for the user.
    if report:
        drive_download_details = report.get('driveDownloadDetails', {})
        print '\n>> Report Id             => %s' % report.get('id')
        print '>> Report Title          => %s' % report.get('title')
        print '>> Report Status         => %s' % report.get('status')
        print '>> Report Download Type  => %s' % report.get('downloadType')
        print '>> Drive Document Id     => %s' % drive_download_details.get('document Id')

    else:
        print 'No reports found'


def main():
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics.readonly']

    # Use the developer console and replace the values with your
    # service account email and relative location of your key file.
    key_file_location = '/home/df/Documents/api-ga/DFPGloboProducao-237b0668bdbf.p12'
    service_account_email = 'teste-api-ga@dfpgloboproducao.iam.gserviceaccount.com'

    # Authenticate and construct service.
    service = get_service('analytics', 'v3', scope, key_file_location, service_account_email)
    profile = get_first_profile_id(service)
    print_results(get_results(service, profile))
    print_list_unsampled_reports(get_list_unsampled_reports(service))
    # print_data_unsampled_reports(get_data_unsampled_reports(service))


if __name__ == '__main__':
    main()

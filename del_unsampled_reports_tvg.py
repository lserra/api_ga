# -*- encoding: UTF-8 -*-

"""
Deleting a unsampled report data (in Google Analytics), using the Google Analytics API.
The authentication method used by this script is service account
Source: https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/management/unsampledReports
Created by: Laercio Serra (laercio.serra@gmail.com)
Created on: 06/06/2017
"""


import sys
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

    # delegate_credentials = credentials.create_delegated('cgti.globobi@gmail.com')

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


def del_reports(service, account_id, web_property_id, profile_id, ur_id):
    # Note: This code assumes you have an authorized Analytics service object.
    # See the Unsampled Reports Developer Guide for details.
    # Source: https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/management/
    # unsampledReports/delete

    # This request deletes an unsampled report.
    try:
        print "-" * 50
        answer = raw_input(">> Do you really want to delete this unsampled report [ Y/N ] : ")

        if str.upper(answer) == "Y":
            service.management().unsampledReports().delete(
                accountId=account_id,
                webPropertyId=web_property_id,
                profileId=profile_id,
                unsampledReportId=ur_id
            ).execute()

            print "Unsampled Report has been deleted with successful!"
        else:
            sys.exit(0)

    except TypeError, error:
        # Handle errors in constructing a query.
        print 'There was an error in constructing your query : %s' % error

    except httplib2.HttpLib2Error, error:
        # Handle API errors.
        print ('There was an API error : %s : %s' % error.message)


def print_results(results):
    # Print data nicely for the user.
    if results:
        print '\nUnsampled Report Details'
        print '-' * 50
        print '>> Report Id     => %s' % results.get('id')
        print '>> Report Title  => %s' % results.get('title')
        print '>> Report Status => %s' % results.get('status')
        print '>> Report Link   => %s' % results.get('selfLink')

        return results.get('id')
    else:
        print '\nUnsampled Report Details'
        print '-' * 50
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
    reps = reports['items']
    if reps:
        print '\nTotal Unsampled Reports: %s' % len(reps)
        print '-' * 50
        for rep in reps:
            r = rep
            print '>> [ %s ] => %s / %s / %s / %s' % (r['id'], r['title'], r['status'], r['created'], r['updated'])

    else:
        print '\nTotal Unsampled Reports: %s' % len(reps)
        print '-' * 50
        print 'No reports found'


def get_data_unsampled_reports(service, ur_id):
    # Note: This code assumes you have an authorized Analytics service object.
    # See the Unsampled Reports Developer Guide for details.

    # Example #1:
    # This request gets an existing unsampled report.
    try:
        return service.management().unsampledReports().get(accountId='296593',
                                                           webPropertyId='UA-296593-56',
                                                           profileId='107283129',
                                                           unsampledReportId=ur_id).execute()

    except TypeError, error:
        # Handle errors in constructing a query.
        print 'There was an error in constructing your query : %s' % error

    except httplib2.HttpLib2Error, error:
        # Handle API errors.
        print ('There was an API error : %s : %s' % error.message)


def print_data_unsampled_reports(report):
    # Print data nicely for the user.
    if report:
        print '\nUnsampled Report Details'
        print '-' * 50
        print '>> Report Id             => %s' % report.get('id')
        print '>> Report Title          => %s' % report.get('title')
        print '>> Report Status         => %s' % report.get('status')
        print '>> Report Download Type  => %s' % report.get('downloadType')

        drive_download_details = report.get('driveDownloadDetails', {})

        if drive_download_details:
            print '>> Drive Document Id     => %s' % drive_download_details.get('document Id')

    else:
        print '\nUnsampled Report Details'
        print '-' * 50
        print 'No reports found'


def main():
    # Define the auth scopes to request.
    # https://www.googleapis.com/auth/analytics - View and manage your Google Analytics data
    # https://www.googleapis.com/auth/analytics.edit - Edit Google Analytics management entities
    scope = ['https://www.googleapis.com/auth/analytics.edit']

    # Use the developer console and replace the values with your
    # service account email and relative location of your key file.
    key_file_location = '/home/df/Documents/api-ga/DFPGloboProducao-237b0668bdbf.p12'
    service_account_email = 'teste-api-ga@dfpgloboproducao.iam.gserviceaccount.com'

    # Parameters definition
    account_id = '296593'
    web_property_id = 'UA-296593-56'

    # Authenticate and construct service.
    service = get_service('analytics', 'v3', scope, key_file_location, service_account_email)
    profile = get_first_profile_id(service)
    ur_id = '41ir6z5OSOuRDotwkh8wQg'
    print_data_unsampled_reports(get_data_unsampled_reports(service, ur_id))
    del_reports(service, account_id, web_property_id, profile, ur_id)
    # print_results(del_reports(service, account_id, web_property_id, profile, ur_id))
    # print_list_unsampled_reports(get_list_unsampled_reports(service))


if __name__ == '__main__':
    main()

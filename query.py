from helloanalytics import initialize_analyticsreporting
import json 
#view_id_variable
view_ids = {}
#view_ids["www.321webmarketing.com”] = "some_number_from_google_analytics"
view_ids['www.bbgbroker.com'] = '119560347'
#view_ids["www.beyondexteriors.com”] = "some_number_from_google_analytics"

#user types in domain name for Google Analytics information
org_name = input('What is the domain name?')
view_id = view_ids['{}'.format(org_name)]

#report_variables
report_month_year = input('report month? (mm/yyyy)')
ga_months_back = input('how many months? (integer; 1-7)')
what_kindof_traffic = input('What kind of traffic? Organic,Social, Other, Direct, or Referrel')


#query function
def get_query(analytics):
    return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': view_id,
          'dateRanges': [{'startDate': '2017-12-01', 'endDate': '2018-07-01'}],
          'metrics': [{'expression':'ga:newUsers'}],
          'dimensions' : [{ 'name' : 'ga:medium', 'name' : 'ga:yearMonth'}],
        }]
      }
      ).execute()


def export_to_json(queryset):
    with open('query.json', 'w') as outfile:
        json.dump(queryset, outfile)

    
#create list of months you are going to loop through
months = ['201712', '201801', '201802', '201803','201804','201805','201806']

def trial():
    analytics = initialize_analyticsreporting()
    queryset = get_query(analytics)
    export_to_json(queryset)

trial()
from helloanalytics import initialize_analyticsreporting
import json 
import pandas 
headers_list = []
dimensions_list = []
listtest = []
months = ['2017-12', '2018-01', '2018-02', '2018-03','2018-04','2018-05','2018-06', '2018-07']
df = pandas.DataFrame([range(7), range(7), range(7), range(7), range(7)])   
#view_id_variable
view_ids = {}
#view_ids["www.321webmarketing.com”] = "some_number_from_google_analytics"
view_ids['www.321webmarketing.com'] = '89636352'
#view_ids["www.beyondexteriors.com”] = "some_number_from_google_analytics"

#user types in domain name for Google Analytics information
org_name = input('What is the domain name?')
view_id = view_ids['{}'.format(org_name)]

#report_variables
report_month_year = input('report month? (mm/yyyy)')
ga_months_back = input('how many months? (integer; 1-7)')
what_kindof_traffic = input('What kind of traffic? Organic,Social, Other, Direct, or Referrel')


#query function
def get_query(analytics, startdate, enddate):
    return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': view_id,
          'dateRanges': [{'startDate': startdate, 'endDate': enddate}],
          'metrics': [{'expression':'ga:newUsers'}],
          'dimensions' : [{ 'name' : 'ga:channelGrouping'}],
        }]
      }
      ).execute()

def get_metric(response):
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        #dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        for row in report.get('data', {}).get('rows', []):
            #dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])
            #for header, dimension in zip(dimensionHeaders, dimensions):
                #print(dimension)
            for i, values in enumerate(dateRangeValues):
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    listtest.append(value)
                    
def get_dimension(response):
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            for header, dimension in zip(dimensionHeaders, dimensions):
                    #for i in range(5):
                        #data_array[i,0] = dimension
                    dimensions_list.append(dimension)
    df.index = dimensions_list


def monthloops(months):
    analytics = initialize_analyticsreporting()
    x = get_query(analytics, months[0] + '-01', months[len(months)-1]+ '-31')
    get_dimension(x)
    for i in range(len(months)-1):
        headers_list.append(months[i])
        x = get_query(analytics,months[i]+ '-01', months[i+1]+ '-01')
        get_metric(x)
    df.columns = headers_list

monthloops(months)



print(df)
print(listtest)



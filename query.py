from helloanalytics import initialize_analyticsreporting
import json 
import pandas 
months = ['2017-12', '2018-01', '2018-02', '2018-03','2018-04','2018-05','2018-06', '2018-07']
headers_list = []
dimensions_list = []
month_values = []
view_ids = {}
view_ids['www.321webmarketing.com'] = '89636352'


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
    dict = {}
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])
            for header, dimension in zip(dimensionHeaders, dimensions):
                dict[dimension] = 0
            for i, values in enumerate(dateRangeValues):
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    dict[dimension] =value
    month_values.append(dict)
                    
def get_dimension(response):
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            for header, dimension in zip(dimensionHeaders, dimensions):
                    dimensions_list.append(dimension)


def month_loops_for_new_users(months):
    analytics = initialize_analyticsreporting()
    x = get_query(analytics, months[0] + '-01', months[len(months)-1]+ '-31')
    get_dimension(x)
    for i in range(len(months)-1):
        headers_list.append(months[i])
        x = get_query(analytics,months[i]+ '-01', months[i+1]+ '-01')
        get_metric(x)
    
def make_table(months):
    Other = []
    Direct = []
    Organic_Search = []
    Referrel = []
    Social = []
    df = pandas.DataFrame([range(7), range(7), range(7), range(7), range(7)]) 
    month_loops_for_new_users(months)
    df.columns = headers_list
    df.index = dimensions_list
    for month_value in month_values:
        try:
            if month_value['(Other)']:
                Other.append(month_value['(Other)'])
            else:
                Other.append(0)
        except:
            Other.append(0)
        if month_value['Direct']:
            Direct.append(month_value['Direct'])
        else:
            Direct.append(0)
        if month_value['Organic Search']:
            Organic_Search.append(month_value['Organic Search'])
        else:
            Orangic_Search.append(0)
        if month_value['Referral']:
            Referrel.append(month_value['Referral'])
        else:
            Referrel.append(0)
        if month_value['Social']:
            Social.append(month_value['Social'])
        else:
            Social.append(0)
    df.loc['(Other)', :] = Other
    df.loc['Direct', : ] = Direct
    df.loc['Organic Search'] = Organic_Search
    df.loc['Referral', :] = Referrel
    df.loc['Social', : ] = Social
    print(df)



make_table(months)
             
             







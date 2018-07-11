from flask import Flask
app = Flask(__name__)
from flask import Markup
from flask import render_template
import json 
import time
from datetime import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from initialize_apis import get_google_analytics_api

#At the beginning you should define the organization name (domain name) to get the View ID so 
#the API call can be made
view_ids = {}
view_ids['www.321webmarketing.com'] = '89636352'
# org_name = input('What is the domain name? ')
org_name = 'www.321webmarketing.com'
view_id = view_ids['{}'.format(org_name)]

#It is just as important to know the reporting month

# reporting_month = input('What is the month of report? YYYY/MM ')
 #reporting_month = datetime.strptime(reporting_month, '%Y/%m')
reporting_month = '2018/02'
#Converting reporting month into YYYY/MM format
reporting_month = datetime.strptime(reporting_month, '%Y/%m')
# ga_months_back = input('How many months back? ')
#And as important to know how many months you're going back in the records
ga_months_back = '10'

#These lists will be used later on to hoard data of sorts
list_of_months = []
unique_channel_groups =[]


#A function to get a list of all of the months we will be examining for channel groupings
def get_months(reporting_month,ga_months_back):
    for i in range(int(ga_months_back)):
        month_behind = reporting_month - relativedelta(months = i)
        month_behind = datetime.strftime(month_behind, '%Y/%m')
        list_of_months.append(month_behind)
    return list_of_months

#A function to return a dictionary of new users, per month, by channel grouping
def get_new_users(month):
    analytics = get_google_analytics_api.initialize_analyticsreporting()
    analytics = analytics
    dict = {}
    startdate = datetime.strptime(month, '%Y/%m')
    enddate = startdate + relativedelta(months = 1)
    startdate = datetime.strftime(startdate, '%Y-%m') + '-01'
    enddate = datetime.strftime(enddate, '%Y-%m') + '-01'
    response = analytics.reports().batchGet(
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
    new_users_by_channel_grouping = dict
    return new_users_by_channel_grouping

#This function makes table out of dictionary
def get_table(list_of_months,view_id):
    data = {}
    for month in list_of_months:
        data[month] = get_new_users(month)
    return data

    
#This function makes a list of all of the unique channel groupings
def get_unique_channel_groupings(data): 
    unique_channel_groupings = []
    months = data.keys()
    for month in months:
        channels = data[month]
        for channel in channels:
            if  channel not in unique_channel_groupings:
                unique_channel_groupings.append(channel)
    return unique_channel_groupings

#This function makes a table with all 0s so that no channel grouping gets left behind if a 
#channel grouping had a value of 0 that month
def make_zero_table(months, unique_channel_groupings):
    table = {}
    for month in months:
        table[month] = {}
        for cg in unique_channel_groupings:
            table[month][cg] = '0'
    return table
    
    
#This function fills in the 0 data table
def make_table(months, unique_channel_groupings,data, table):
    for month in months:
        for cg in unique_channel_groupings:
            if cg in data[month]:
                table[month][cg] = data[month][cg]
    return table
            

#This function makes an interestingly structured dictionary containing months, channels, and data
#from table
def get_data(reporting_month, ga_months_back, view_id):
    months = get_months(reporting_month, ga_months_back)
    data = get_table(months, view_id)
    unique_channel_groupings = get_unique_channel_groupings(data)
    table = make_zero_table(months, unique_channel_groupings)
    table = make_table(months, unique_channel_groupings,data, table)
    data = {}
    data["months"] = months
    data["channels"] = unique_channel_groupings
    data["data"] = table
    return data

#Unfortunately, I need this data to work on flask, and didn't feel like going back and changing everything
#so this function rearranges the dictionary so it can be looped through on the html (bootstrap) template

def rearrange_dict_for_flask(data):
    data_dict = {}
    months = data["months"]
    channels = data["channels"]
    data = data["data"]
    intermediate_list = []
    channel_list = []
    total = 0
    total_lst = [] 
    #The purpose of these loops is to change the structure of the data
    #so that it can be put into a flask html template
    for month in months:
        intermediate_list.append(data[month])
    for item in intermediate_list:
        for key in item.keys():
            channel_list.append(key + ":" + item[key])
    for i in range(len(months)):
        month = datetime.strptime(months[i], '%Y/%m')
        month = datetime.strftime(month, '%b')
        months[i] = month     
    data_dict["months"] = months[::-1]
    for channel in channels:
        lst = []
        for item in channel_list:
            if channel in item:
                item = item.replace(channel, "").replace(":", "")
                lst.append(item)
                data_dict[channel] = lst[::-1]
    return data_dict
#This kinda just does what I said above
def data_for_flask(reporting_month, ga_months_back, view_id):
    data = get_data(reporting_month, ga_months_back, view_id)
    data_dict = rearrange_dict_for_flask(data)
    return data_dict

data_dict = data_for_flask(reporting_month, ga_months_back, view_id)
#This function/app route gets the data for flask and plugs it into a Bootstrap template

@app.route('/data_table')
def data_for_template():
    data = data_dict
    return render_template('data_table_traffic.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
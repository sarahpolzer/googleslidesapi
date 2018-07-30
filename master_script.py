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
import requests
port = 5004


with open('client_information/client_information.json', 'r') as f:
     clients = json.load(f)
client = input('Who is the client? ')
view_id = clients[client]['google_analytics']

reporting_month = input('What is the reporting month? (YYYY/MM)? ')
reporting_month = datetime.strptime(reporting_month, '%Y/%m')
ga_months_back = input('How many months back? ')
#At the beginning you should define the organization name (domain name) to get the View ID so 
#the API call can be made to Google Analytics.
#view_ids = {}
#view_ids['www.321webmarketing.com'] = '89636352'
#org_name = input('What is the domain name? ')
#org_name = 'www.321webmarketing.com'
#view_id = view_ids['{}'.format(org_name)]

"""What
Converts
Data"""
#key and token
api_key = "273-f91b45f83365ec4b"
token = "26f9d7d7d282599f161076ad2e4eecfd"

#Account IDs
account_id = clients[client]['what_converts']


#First we've got a function to get the months that we will pull API data from

def get_months(reporting_month,ga_months_back):
    list_of_months = []
    for i in range(int(ga_months_back)):
        month_behind = reporting_month - relativedelta(months = i)
        month_behind = datetime.strftime(month_behind, '%Y/%m')
        list_of_months.append(month_behind)
    return list_of_months



""" API 
Calls
To
Google
Analytics"""

#A function to get a list of all of the months we will be examining for channel groupings

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
    first, organic = 0, unique_channel_groupings.index('Organic Search')
    unique_channel_groupings[organic], unique_channel_groupings[first] = unique_channel_groupings[first], unique_channel_groupings[organic]
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

def rearrange_traffic_data_for_flask(data):
    traffic_data = {}
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
    traffic_data["months"] = months[::-1]
    for channel in channels:
        lst = []
        for item in channel_list:
            if channel in item:
                item = item.replace(channel, "").replace(":", "")
                lst.append(item)
                traffic_data[channel] = lst[::-1]
    return traffic_data

#This kinda just does what I said above
def traffic_data_for_flask(reporting_month, ga_months_back, view_id):
    data = get_data(reporting_month, ga_months_back, view_id)
    traffic_data = rearrange_traffic_data_for_flask(data)
    return traffic_data

""" API 
Calls
To 
What
Converts"""


#This function pulls leads data based off of the list of months
def pull_lead_data(list_of_months):
    n = 0
    month_lead = {}
    lead_dict = {}
    lead_types = ['phone_call', 'web_form']
    lead_dict['months'] = list_of_months
    for month in list_of_months:  
        lead_dict = {} 
        startdate = datetime.strptime(month, '%Y/%m')
        enddate = startdate + relativedelta(months = 1)
        startdate = datetime.strftime(startdate, '%Y-%m') + '-01'
        enddate = datetime.strftime(enddate, '%Y-%m') + '-01'
        for lead in lead_types:
            params = {
                'lead_type': lead,
                'start_date': startdate,
                'end_date': enddate,
                'lead_status': 'unique',
                'account_id' : account_id
             }
            x = requests.get(
                'https://app.whatconverts.com/api/v1/leads',
                 auth = (api_key,token),
                 params = params
                  )
            json_data = json.loads(x.text)
            lead_dict[lead] = json_data[ "total_leads" ]
            month_lead[month] = lead_dict
    return month_lead

def rearrange_lead_data_for_flask(list_of_months, month_lead):
    lead_data = {}
    lead_types = ['phone_call', 'web_form']
    phone_call = []
    web_form = []
    for month in list_of_months:
        for lead_type in lead_types:
            if month_lead[month][lead_type] and lead_type=='phone_call':
                phone_call.append(month_lead[month][lead_type])
            else:
                web_form.append(month_lead[month][lead_type])
    for i in range(len(list_of_months)):
        month = datetime.strptime(list_of_months[i], '%Y/%m')
        month = datetime.strftime(month, '%B')
        list_of_months[i] = month
    list_of_months = list_of_months[::-1]
    phone_call = phone_call[::-1]
    web_form = web_form[::-1]
    lead_data['months'] = list_of_months
    lead_data['Phone Call'] = phone_call
    lead_data['Web Form'] = web_form
    return lead_data           
                     
            
       
        

def leads_data_for_flask(reporting_month, ga_months_back):
    mo_list = get_months(reporting_month, ga_months_back)
    month_lead = pull_lead_data(mo_list)
    lead_data = rearrange_lead_data_for_flask(mo_list, month_lead)
    return lead_data


"""
End 
of
API
call
to
WhatConverts
"""


""" 
Beginning 
to make
 Content Charts
 """

#Collecting data for content posted during reporting month
def content_posted_report_month():
    now = datetime.now()
    report_month = now.strftime('%B %Y')
    master_list = []
    report_month_data = {}
    print("Answer these questions to provide information about content being posted in {}".format(report_month))
    for article in range(3):
        article_list = []
        title = input("What is the content's title? ")
        content_type = input("What is the content's type? ")
        article_list.append(title)
        article_list.append(content_type)
        master_list.append(article_list)
    report_month_data['columns'] = ['Title', 'Type']
    report_month_data['data'] = master_list
    return report_month_data

#Collecting data for content that is going to be posted next month
def content_posted_next_month():
    now = datetime.now()
    next_month = now + relativedelta(months=1)
    next_month = next_month.strftime('%B %Y')
    master_list = []
    next_month_data = {}
    print("Answer these questions to provide information about content being posted in {}".format(next_month))
    for article in range(3):
        article_list = []
        title = input("What is the content title? ")
        content_type = input("What is the content type? ")
        article_list.append(title)
        article_list.append(content_type)
        master_list.append(article_list)
    next_month_data['columns'] = ['Title', 'Type']
    next_month_data['data'] = master_list
    return next_month_data




"""
consolidating
data
"""

traffic_data = traffic_data_for_flask(reporting_month, ga_months_back, view_id)
leads_data = leads_data_for_flask(reporting_month,ga_months_back)
report_month_data = content_posted_report_month()
next_month_data = content_posted_next_month()

"""
Now rendering 
Flask templates
for data
"""


@app.route('/traffic')
def traffic_data_for_template():
    data = traffic_data
    return render_template('traffic.html', data=data)


@app.route('/leads')
def leads_data_for_template():
    data = leads_data
    return render_template('leads.html', data=data)


@app.route('/content_report_month')
def content_data_for_report_month_template():
    data = report_month_data
    return render_template('content_overview.html', data=data)

@app.route('/content_next_month')
def content_data_for_next_month_template():
    data = next_month_data
    return render_template('content_overview.html', data=data)

if __name__ == "__main__":
    app.run(port=port)





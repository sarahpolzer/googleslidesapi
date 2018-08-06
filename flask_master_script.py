#importing required packages"
from flask import Flask
app = Flask(__name__)
from flask import Markup
from flask import render_template
import json
import time
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from initialize_apis import get_google_analytics_api
import requests
from __main__ import *
from multiprocessing import Process
from flask import request
from find_client_options import find_clients_options
from find_client_options import convert_number_to_client




#The port where the server will run
port = 5005

#reading JSON client data as to get the stored google analytics and What Converts data
with open('client_information/client_information.json', 'r') as f:
     clients = json.load(f)
#find clients options is an imported function that finds all valid clients and makes 
#a big string that the User will see telling them which input buttons to press for each client
clients_option = find_clients_options(clients)

#asking the User who the client is- clients_option string will appear in terminal
client = input(clients_option)

#converting number that was inputted into the client that the User meant to select
client = convert_number_to_client(clients, client)



#Getting the report month in the correct format
def flask_master(clients, client, port):
    now = datetime.datetime.now()
    reporting_month = now - relativedelta(months=1)
    reporting_month = datetime.datetime.strftime(reporting_month, '%Y/%m' )
    reporting_month = datetime.datetime.strptime(reporting_month, '%Y/%m')

    #Assigning the number of months back
    months_back = 6


    """Getting the Google Analytics View ID for the Traffic Charts"""
    view_id = clients[client]['google_analytics']


    """What
    Converts
    Data"""
    #key and token
    api_key = "273-f91b45f83365ec4b"
    token = "26f9d7d7d282599f161076ad2e4eecfd"
    #Account IDs based off of client dictionary
    account_id = clients[client]['what_converts']


    #First we've got a function to get the months that we will pull API data from for Google Analytics
    #and What Converts

    def get_months(reporting_month, months_back):
        list_of_months = []
        for i in range(int(months_back)):
            month_behind = reporting_month - relativedelta(months = i)
            month_behind = datetime.datetime.strftime(month_behind, '%Y/%m')
            list_of_months.append(month_behind)
        return list_of_months



    """ API 
    Calls
    To
    Google
    Analytics"""


    #A function to return a dictionary of new users, per month, by channel grouping
    def get_new_users(month, view_id):
        analytics = get_google_analytics_api.initialize_analyticsreporting()
        analytics = analytics
        dict = {}
        startdate = datetime.datetime.strptime(month, '%Y/%m')
        enddate = startdate + relativedelta(months = 1)
        startdate = datetime.datetime.strftime(startdate, '%Y-%m') + '-01'
        enddate = datetime.datetime.strftime(enddate, '%Y-%m') + '-01'
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
            data[month] = get_new_users(month, view_id)
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
    def get_data(reporting_month,months_back, view_id):
        months = get_months(reporting_month, months_back)
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
            month = datetime.datetime.strptime(months[i], '%Y/%m')
            month = datetime.datetime.strftime(month, '%b')
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
    def traffic_data_for_flask(reporting_month, months_back, view_id):
        data = get_data(reporting_month, months_back, view_id)
        traffic_data = rearrange_traffic_data_for_flask(data)
        return traffic_data

    """ API 
    Calls
    To 
    What
    Converts"""


    #This function pulls leads data based off of the list of months
    def pull_lead_data(list_of_months, account_id):
        n = 0
        month_lead = {}
        lead_dict = {}
        lead_types = ['phone_call', 'web_form']
        lead_dict['months'] = list_of_months
        for month in list_of_months:  
            lead_dict = {} 
            startdate = datetime.datetime.strptime(month, '%Y/%m')
            enddate = startdate + relativedelta(months = 1)
            startdate = datetime.datetime.strftime(startdate, '%Y-%m') + '-01'
            enddate = datetime.datetime.strftime(enddate, '%Y-%m') + '-01'
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
    #This function rearranges the data we just got so that it is suitable for the Flask template
    def rearrange_lead_data_for_flask(list_of_months, month_lead):
        lead_data = {}
        lead_types = ['phone_call', 'web_form']
        phone_call = []
        web_form = []
        for month in list_of_months:
            for lead_type in lead_types:
                if month_lead[month][lead_type] >= 0 and lead_type=='phone_call':
                    phone_call.append(month_lead[month][lead_type])
                else:
                    web_form.append(month_lead[month][lead_type])
        for i in range(len(list_of_months)):
            month = datetime.datetime.strptime(list_of_months[i], '%Y/%m')
            month = datetime.datetime.strftime(month, '%B')
            list_of_months[i] = month
        list_of_months = list_of_months[::-1]
        phone_call = phone_call[::-1]
        web_form = web_form[::-1]
        lead_data['months'] = list_of_months
        lead_data['Phone Call'] = phone_call
        lead_data['Web Form'] = web_form
        return lead_data           
                        
                
        
            
    #This is kindof like the master function, it returns the dictionary of leads data that will
    #later be used in the Flask template.
    def leads_data_for_flask(reporting_month, months_back, account_id):
        mo_list = get_months(reporting_month, months_back)
        month_lead = pull_lead_data(mo_list, account_id)
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


    #Collecting data for content posted during reporting month




    """
    consolidating data so that the Analytics data, WhatConverts data, and Content charts are all in 
    proper html templates with specific urls
    """
    traffic_data = traffic_data_for_flask(reporting_month, months_back, view_id)
    leads_data = leads_data_for_flask(reporting_month, months_back, account_id)


    @app.route('/traffic')
    def traffic_data_for_template():
        data = traffic_data
        return render_template('traffic.html', data=data)

                #The app route for WhatConverts data
    @app.route('/leads')
    def leads_data_for_template():
        data = leads_data
        return render_template('leads.html', data=data)


    if __name__ == "__main__":
        app.run(port=port, debug=False)
     

flask_master(clients, client, port)





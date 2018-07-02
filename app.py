from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
app = Flask(__name__)
import json 
from helloanalytics import initialize_analyticsreporting 
from quickstart import *
import json 
import time
from datetime import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


view_ids = {}
view_ids['www.321webmarketing.com'] = '89636352'
# org_name = input('What is the domain name? ')
org_name = 'www.321webmarketing.com'
view_id = view_ids['{}'.format(org_name)]

# reporting_month = input('What is the month of report? YYYY/MM ')
 #reporting_month = datetime.strptime(reporting_month, '%Y/%m')
reporting_month = '2018/02'
reporting_month = datetime.strptime(reporting_month, '%Y/%m')
# ga_months_back = input('How many months back? ')
ga_months_back = '7'
list_of_months = []
unique_channel_groups =[]



def get_months(reporting_month,ga_months_back):
    for i in range(int(ga_months_back)):
        month_behind = reporting_month - relativedelta(months = i)
        month_behind = datetime.strftime(month_behind, '%Y/%m')
        list_of_months.append(month_behind)
    return list_of_months


def get_new_users(month):
    analytics = initialize_analyticsreporting()
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

def get_table(list_of_months,view_id):
    data = {}
    for month in list_of_months:
        data[month] = get_new_users(month)
    return data

    

def get_unique_channel_groupings(data): 
    unique_channel_groupings = []
    months = data.keys()
    for month in months:
        channels = data[month]
        for channel in channels:
            if  channel not in unique_channel_groupings:
                unique_channel_groupings.append(channel)
    return unique_channel_groupings


def make_zero_table(months, unique_channel_groupings):
    table = {}
    for month in months:
        table[month] = {}
        for cg in unique_channel_groupings:
            table[month][cg] = '0'
    return table
    
    

def make_table(months, unique_channel_groupings,data, table):
    for month in months:
        for cg in unique_channel_groupings:
            if cg in data[month]:
                table[month][cg] = data[month][cg]
    return table
            


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

def rearrange_dict_for_flask(data):
    data_dict = {}
    Direct = []
    Organic_search = []
    Referral = []
    Social = []
    Other = []
    months = data["months"]
    channels = data["channels"]
    data = data["data"]
    data_dict["months"] = months
    for month in months:
        for channel in channels:
            if channel == 'Direct':
                Direct.append(data[month][channel])
            if channel == 'Organic Search':
                Organic_search.append(data[month][channel])
            if channel=='Referral':
                Referral.append(data[month][channel])
            if channel=='Social':
                Social.append(data[month][channel])
            if channel == '(Other)':
                Other.append(data[month][channel])
    data_dict["Direct"] = Direct
    data_dict["Organic Search"] = Organic_search
    data_dict["Referral"] = Referral
    data_dict["Social"] = Social
    data_dict["(Other)"] = Other
    return data_dict

def data_for_flask(reporting_month, ga_months_back, view_id):
    data = get_data(reporting_month, ga_months_back, view_id)
    data_dict = rearrange_dict_for_flask(data)
    return data_dict



@app.route('/data_table')
def data_for_template():
    view_id = '89636352'
    reporting_month = '2018/02'
    reporting_month = datetime.strptime(reporting_month, '%Y/%m')
    ga_months_back = '4'
    data = data_for_flask(reporting_month, ga_months_back, view_id)
    return render_template('datatable.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
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
reporting_month = '2018/01'
reporting_month = datetime.strptime(reporting_month, '%Y/%m')
# ga_months_back = input('How many months back? ')
ga_months_back = '5'
list_of_months = []
unique_channel_groups = []



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
            


def master(reporting_month, ga_months_back, view_id):
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
    


def create_google_slides_data_table(data, slides_id, page_Id, table_Id):
    num_rows = len(data["months"]) + 1
    num_cols = len(data["channels"]) + 1
    service = setup_googleslides_api()
    body = {
            "requests": [
        {
            "createTable": {
            "objectId": table_Id,
            "elementProperties": {
                "pageObjectId": page_Id,
            },
            "rows": num_rows,
             "columns": num_cols
            }
        }
    ]
    }
    response = service.presentations().batchUpdate(presentationId = slides_id, body = body).execute()




def edit_google_slides_row_data(data, slides_id, table_Id):
    service = setup_googleslides_api()
    cg_rows = data["channels"]
    for row in range(len(cg_rows)):
        body = {
            "requests": [     
                {
                    "insertText": {
                        "objectId": table_Id,
                        "cellLocation": {
                            "rowIndex": row + 1,
                            "columnIndex": 0
                            },
                            "text": cg_rows[row],
                            "insertionIndex": 0
                            }
                        }
                    ]
                }
        response = service.presentations().batchUpdate(presentationId = slides_id, body = body).execute()

def edit_google_slides_col_data(data,slides_id, table_Id):
    service = setup_googleslides_api()
    mo_cols = data["months"]
    for col in range(len(mo_cols)):
        body = {
            "requests": [     
                {
                    "insertText": {
                        "objectId": table_Id,
                        "cellLocation": {
                            "rowIndex": 0,
                            "columnIndex": col + 1
                            },
                            "text": mo_cols[col],
                            "insertionIndex": 0
                            }
                        }
                    ]
                }
        response = service.presentations().batchUpdate(presentationId = slides_id, body = body).execute()

def insert_google_slides_cell_data(data, slides_id, table_Id):
    service = setup_googleslides_api()
    data_cells = data["data"]
    mo_cols = data["months"]
    cg_rows = data["channels"]
    for col in range(len(mo_cols)):
        for row in range(len(cg_rows)):
            body = {
                "requests": [     
                {
                    "insertText": {
                        "objectId": table_Id,
                        "cellLocation": {
                            "rowIndex": row+1,
                            "columnIndex": col + 1
                            },
                            "text": data_cells[mo_cols[col]][cg_rows[row]],
                            "insertionIndex": 0
                            }
                        }
                    ]
                }
            response = service.presentations().batchUpdate(presentationId = slides_id, body = body).execute()
        

    
data = master(reporting_month, ga_months_back, view_id)
slides_id = '17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8'
page_id = 'g1edf554207_0_7'
table_Id = '123456'
create_google_slides_data_table(data, slides_id, page_id, table_Id)
edit_google_slides_row_data(data,slides_id, table_Id)
edit_google_slides_col_data(data, slides_id, table_Id)
insert_google_slides_cell_data(data, slides_id, table_Id)


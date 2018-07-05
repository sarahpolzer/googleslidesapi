import requests
import json 
import json 
import time
from datetime import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
api_key = "273-f91b45f83365ec4b"
token = "26f9d7d7d282599f161076ad2e4eecfd"
account_ids = {"321webmarketing.com": '29202'}
account_id = account_ids["321webmarketing.com"]
reporting_month = '2018/04'
reporting_month = datetime.strptime(reporting_month, '%Y/%m')
ga_months_back = '5'


list_of_months = []

def get_months(reporting_month,ga_months_back):
    for i in range(int(ga_months_back)):
        month_behind = reporting_month - relativedelta(months = i)
        month_behind = datetime.strftime(month_behind, '%Y/%m')
        list_of_months.append(month_behind)
    return list_of_months

def pull_lead_data(list_of_months):
    lead_types = ['phone_call', 'web_form']
    dict_two = {}
    for month in list_of_months:   
        startdate = datetime.strptime(month, '%Y/%m')
        enddate = startdate + relativedelta(months = 1)
        startdate = datetime.strftime(startdate, '%Y-%m') + '-01'
        enddate = datetime.strftime(enddate, '%Y-%m') + '-01'
        for lead in lead_types:
            params = {
                'lead_type': lead,
                'start_date': startdate,
                'end_date': enddate,
                'lead_status': 'unique'
             }
            x = requests.get(
                'https://app.whatconverts.com/api/v1/leads',
                 auth = (api_key,token),
                 params = params
                  )
            json_data = json.loads(x.text)
            dict_two[month] = lead
            dict_two[month][lead] = json_data["total_leads"]
            
        """x = x.json()
        with open("what_converts.json", "a") as outfile:
            json_dump(x, outfile)"""
    print(dict_two)
    return dict_two






def master(reporting_month, ga_months_back):
    mo_list = get_months(reporting_month, ga_months_back)
    dict_two = pull_lead_data(mo_list)
    return dict_two




master(reporting_month,ga_months_back)

   
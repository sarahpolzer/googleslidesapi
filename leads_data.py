
from flask import Flask
app = Flask(__name__)
from flask import Markup
from flask import render_template
import requests
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
reporting_month = '2018/06'
reporting_month = datetime.strptime(reporting_month, '%Y/%m')
ga_months_back = '9'
list_of_months = []

def get_months(reporting_month,ga_months_back):
    for i in range(int(ga_months_back)):
        month_behind = reporting_month - relativedelta(months = i)
        month_behind = datetime.strftime(month_behind, '%Y/%m')
        list_of_months.append(month_behind)
    return list_of_months

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
                'lead_status': 'unique'
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

def rearrange_data_for_flask(list_of_months, month_lead):
    rearranged_dict = {}
    lead_types = ['phone_call', 'web_form']
    phone_call = []
    web_form = []
    for month in list_of_months:
        for lead_type in lead_types:
            if month_lead[month][lead_type] and lead_type=='phone_call':
                phone_call.append(month_lead[month][lead_type])
            else:
                web_form.append(month_lead[month][lead_type])
    #for month in list_of_months:
           # month = datetime.strptime(month, '%Y/%m')
          # month = datetime.strftime(month, '%B')
    for i in range(len(list_of_months)):
        month = datetime.strptime(list_of_months[i], '%Y/%m')
        month = datetime.strftime(month, '%B')
        list_of_months[i] = month
    list_of_months = list_of_months[::-1]
    phone_call = phone_call[::-1]
    web_form = web_form[::-1]
    rearranged_dict['months'] = list_of_months
    rearranged_dict['Phone Call'] = phone_call
    rearranged_dict['Web Form'] = web_form
    return rearranged_dict            
                     
            
       
        

def master(reporting_month, ga_months_back):
    mo_list = get_months(reporting_month, ga_months_back)
    month_lead = pull_lead_data(mo_list)
    rearranged_dict = rearrange_data_for_flask(mo_list, month_lead)
    return rearranged_dict



rearranged_dict = master(reporting_month,ga_months_back)

@app.route('/leads')
def data_for_template():
    data = rearranged_dict
    return render_template('leads.html', data=data)


if __name__ == "__main__":
     app.run(port=5002)






   

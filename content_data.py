from flask import Flask
app = Flask(__name__)
from flask import Markup
from flask import render_template


#import time packages
import time
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

#slides_service = get_slides_and_drive_apis.setup_googleslides_api()
slides_id = '17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8'
page_Id = 'g1eca1050f0_0_62'

def content_posted_report_month():
    now = datetime.datetime.now()
    report_month = now.strftime('%B %Y')
    master_list = []
    report_month_table_dict = {}
    print("Answer these questions to provide information about content being posted in {}".format(report_month))
    for article in range(3):
        article_list = []
        title = input("What is the content's title? ")
        content_type = input("What is the content's type? ")
        article_list.append(title)
        article_list.append(content_type)
        master_list.append(article_list)
    report_month_table_dict['columns'] = ['Title', 'Type']
    report_month_table_dict['data'] = master_list
    return report_month_table_dict

def content_posted_next_month():
    now = datetime.datetime.now()
    next_month = now + relativedelta(months=1)
    next_month = next_month.strftime('%B %Y')
    master_list = []
    next_month_table_dict = {}
    print("Answer these questions to provide information about content being posted in {}".format(next_month))
    for article in range(3):
        article_list = []
        title = input("What is the content title? ")
        content_type = input("What is the content type? ")
        article_list.append(title)
        article_list.append(content_type)
        master_list.append(article_list)
    next_month_table_dict['columns'] = ['Title', 'Type']
    next_month_table_dict['data'] = master_list
    return next_month_table_dict

report_month_table_dict = content_posted_report_month()
next_month_table_dict = content_posted_next_month()

@app.route('/content_report_month')
def data_for_report_month_template():
    data = report_month_table_dict
    return render_template('content_overview.html', data=data)

@app.route('/content_next_month')
def data_for_next_month_template():
    data = next_month_table_dict
    return render_template('content_overview.html', data=data)

if __name__ == "__main__":
     app.run(port=5005)

from quickstart import *
#import time packages
import time
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

def content_posted_report_month():
    now = datetime.datetime.now()
    report_month = now.strftime('%Y/%m')
    master_list = []
    table_dict = {}
    print("Answer these questions to provide information about content being posted in {}".format(report_month))
    for article in range(3):
        article_list = []
        content_name = input("What is the content name")
        content_type = input("What is the content type")
        post_date = input("On what date YYYY/MM")
        article_list.append(content_name)
        article_list.append(content_type)
        article_list.append(post_date)
        master_list.append(article_list)
    table_dict['columns'] = ['content_name', 'content_type', 'postdate']
    table_dict['data'] = master_list
    print(table_dict)
    return table_dict



def content_posted_next_month():
    now = datetime.datetime.now()
    next_month = now + relativedelta(months=1)
    next_month = next_month.strftime('%Y/%m')
    master_list = []
    table_dict = {}
    print("Answer these questions to provide information about content being posted in {}".format(next_month))
    for article in range(3):
        article_list = []
        title = input("What is the content title? ")
        content = input("What is the content type? ")
        article_list.append(title)
        article_list.append(content)
        master_list.append(article_list)
    table_dict['columns'] = ['Title', 'Content']
    table_dict['data'] = master_list
    return table_dict


def create_google_slides_data_table(table_dict, slides_id, page_Id, table_Id):
    num_rows = len(table_dict['data']) + 1
    num_cols = len(table_dict['columns'])
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




def edit_google_slides_col_data(table_dict,slides_id, table_Id):
    service = setup_googleslides_api()
    cols = table_dict["columns"]
    for col in range(len(cols)):
        body = {
            "requests": [     
                {
                    "insertText": {
                        "objectId": table_Id,
                        "cellLocation": {
                            "rowIndex": 0,
                            "columnIndex": col 
                            },
                            "text": cols[col],
                            "insertionIndex": 0
                            }
                        }
                    ]
                }
        response = service.presentations().batchUpdate(presentationId = slides_id, body = body).execute()

def edit_google_slides_data(table_dict, slides_Id, table_Id):
    service = setup_googleslides_api()
    data_cells = table_dict['data']
    cols = table_dict['columns']
    for col in range(len(mo_cols)):
        for row in range(len(data_cells)+1):
            body = {
                "requests": [     
                {
                    "insertText": {
                        "objectId": table_Id,
                        "cellLocation": {
                            "rowIndex": row+1,
                            "columnIndex": col 
                            },
                            "text": data_cells,
                            "insertionIndex": 0
                            }
                        }
                    ]
                }
            response = service.presentations().batchUpdate(presentationId = slides_id, body = body).execute()
    

def master(slides_id, page_Id, table_Id):
    table_dict = content_posted_next_month()
    create_google_slides_data_table(table_dict, slides_id, page_Id, table_Id)
    edit_google_slides_col_data(table_dict, slides_id, table_Id)
    



slides_id = '17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8'
page_Id = 'g1edf554207_0_7'
table_Id = '123456'

master(slides_id, page_Id, table_Id)
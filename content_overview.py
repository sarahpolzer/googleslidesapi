
import initialize_apis
from initialize_apis import get_slides_and_drive_apis

#import time packages
import time
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

slides_service = get_slides_and_drive_apis.setup_googleslides_api()

def content_posted_report_month():
    now = datetime.datetime.now()
    report_month = now.strftime('%Y/%m')
    master_list = []
    table_dict = {}
    print("Answer these questions to provide information about content being posted in {}".format(report_month))
    for article in range(3):
        article_list = []
        title = input("What is the content title")
        content_type = input("What is the content type")
        article_list.append(title)
        article_list.append(content_type)
        master_list.append(article_list)
    table_dict['columns'] = ['Title', 'Type']
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
        content_type = input("What is the content type? ")
        article_list.append(title)
        article_list.append(content_type)
        master_list.append(article_list)
    table_dict['columns'] = ['Title', 'Type']
    table_dict['data'] = master_list
    return table_dict


def create_google_slides_data_table(table_dict, slides_id, page_Id, table_Id):
    num_rows = len(table_dict['data']) + 1
    num_cols = len(table_dict['columns'])
    service = slides_service
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
    service = slides_service
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
    service = slides_service
    rows = table_dict['data']
    cols = table_dict['columns']
    for row in range(len(rows)):
        for col in range(len(cols)):
            body = {
                "requests": [     
                {
                    "insertText": {
                        "objectId": table_Id,
                        "cellLocation": {
                            "rowIndex": row+1,
                            "columnIndex": col 
                            },
                            "text": rows[row][col],
                            "insertionIndex": 0
                            }
                        }
                    ]
                }
            response = service.presentations().batchUpdate(presentationId = slides_id, body = body).execute()

def format_header_row(table_dict, slides_Id, table_Id):
    service = slides_service
    cols = table_dict['columns']
    body = { 
            "requests": [
                    {
                    "updateTableCellProperties": {
                        "objectId": table_Id,
                        "tableRange": {
                        "location": {
                            "rowIndex": 0,
                            "columnIndex": 0
                        },
                        "rowSpan": 1,
                        "columnSpan": len(cols)
                        },
                        "tableCellProperties": {
                        "tableCellBackgroundFill": {
                            "solidFill": {
                            "color": {
                                "rgbColor": {
                                "red": 0.7,
                                "green": 0.7,
                                "blue": 0.7
                                }
                            }
                            }
                        }
                        },
                        "fields": "tableCellBackgroundFill.solidFill.color"
                    }
                    },
                ]
                }

        
    response = service.presentations().batchUpdate(presentationId = slides_id, body = body).execute()

def format_header_text(table_dict, slides_Id, table_Id):
    service = slides_service
    cols = table_dict['columns']
    for col in range(len(cols)):
        body = { 
            "requests": [
                 {
                    "updateTextStyle": {
                        "objectId": table_Id,
                        "cellLocation": {
                        "rowIndex": 0,
                        "columnIndex": col
                        },
                        "style": {
                        "foregroundColor": {
                            "opaqueColor": {
                            "rgbColor": {
                                "red": 0.0,
                                "green": 0.0,
                                "blue": 0.0
                            }
                            }
                        },
                        "bold": True,
                        "fontFamily": "Cambria",
                        "fontSize": {
                            "magnitude": 18,
                            "unit": "PT"
                        }
                        },
                        "textRange": {
                        "type": "ALL"
                        },
                        "fields": "foregroundColor,bold,fontFamily,fontSize"
                    }
                    }, 
                ]
            }
        response = service.presentations().batchUpdate(presentationId = slides_id, body = body).execute()



def master(slides_id, page_Id, table_Id):
    table_dict = content_posted_next_month()
    create_google_slides_data_table(table_dict, slides_id, page_Id, table_Id)
    edit_google_slides_col_data(table_dict, slides_id, table_Id)
    edit_google_slides_data(table_dict, slides_id, table_Id)
    format_header_row(table_dict, slides_id, table_Id)
    format_header_text(table_dict, slides_id, table_Id)

slides_id = '17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8'
page_Id = 'g1edf554207_0_7'
table_Id = '123456'

master(slides_id, page_Id, table_Id)
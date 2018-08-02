
from __main__ import *

def find_clients_options(clients):
    client_lst = []
    client_options = 'Who is the client? \n'
    for client in clients.keys():
        if  "google_analytics" in clients[client].keys() and "what_converts" in clients[client].keys():
            client_lst.append(client)  
    for i in range(len(client_lst)):
        if i < (len(client_lst)-1):
            client_select = 'For ' + client_lst[i] + ' press ' + str(i+1) + '\n '
        else:
            client_select =  'For ' + client_lst[i] + ' press ' + str(i+1) + '\n '
        client_options = client_options + client_select
    return client_options

def convert_number_to_client(clients, client_input):
    client_lst = []
    for client in clients.keys():
        if  "google_analytics" in clients[client].keys() and "what_converts" in clients[client].keys():
            client_lst.append(client)  
    index = int(client_input) - 1
    client = client_lst[index]
    return client





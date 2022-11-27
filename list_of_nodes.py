#!/usr/bin/env python3

import requests
import json,time,urllib
from tabulate import tabulate
from pnetlab_lib import *

url = "http://192.168.80.133"
Login = 'admin'
Pass = 'pnet'
Cookie1, xsrf = login(url, Login, Pass)


# ----------------- Now create a list of running sessions summary info ----------------------------

print ("\n---------------------------- Running Labs -------------------------------\n")

users = filter_user(url, Cookie1, xsrf).json()

r = get_sessions_count(url, Cookie1).json()
count_labs = r["data"]
print("\nFound", count_labs,"running labs\n")

response_json = filter_session(url, Cookie1, xsrf, 1, count_labs)

response_json = response_json.json()

lab_list = set()
for item in response_json["data"]["data_table"]:
    lab_list.add(item["lab_session_path"])

lab_list = sorted(list(lab_list))
i = 0
labs = []
for item in lab_list:
    i += 1
    labs.append([i, item])
table_header = [
                "num", 
                "lab_session_path"
               ]
print( tabulate(labs, table_header) )

lab_num = int(input("\nChoose the lab number: ")) - 1 

print ("\n------------------------ List of Lab Sessions ---------------------------\n")

session_list = []
for item in response_json["data"]["data_table"]:
    if item["lab_session_path"] == labs[lab_num][1]:
        username = ""
        for user in users["data"]["data_table"]:
            if user["pod"] == item["lab_session_pod"] :
                username = user["username"]   
        session = [
                    item["lab_session_id"], 
                    username, 
                    item["lab_session_path"] 
                ]
        session_list.append( session )

table_header = [
                "lab_session_id", 
                "username",
                "lab_session_path"
               ]
print( tabulate(session_list, table_header) )

sess_id = input("\nInput lab session ID: ") 

print ("\n--------------------------- List of Nodes -------------------------------\n")

join_session(url, sess_id, Cookie1)

r = get_nodes(url, Cookie1).json()

node_list = []
for item in r['data']['nodes']:
    node = [
        r['data']['nodes'][str(item)]['name'],
        r['data']['nodes'][str(item)]['id'],
        r['data']['nodes'][str(item)]['url']
    ]

    node_list.append( node )
#print (session_list)
table_header = [
                "name", 
                "id", 
                "url"
               ]
print( tabulate(node_list, table_header) )

logout(url)
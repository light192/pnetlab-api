import requests
import json,time,urllib
from urllib.parse import unquote

def login(url, name, password):
    url2 = url + '/store/public/auth/login/login'
    header1 = {
       'Content-Type': 'application/json;charset=UTF-8'
    }
    r1 = requests.get(url, headers = header1, verify = False)
    header2 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'X-XSRF-TOKEN': unquote(r1.cookies["XSRF-TOKEN"]), 
        'Cookie': '_session='+unquote(r1.cookies["_session"])+';XSRF-TOKEN='+unquote(r1.cookies["XSRF-TOKEN"])
    }
    payload2 = json.dumps(
        {
            'username':''+name+'',
            'password':''+password+'',
            'html':'0','captcha':''
        }
    )
    r2 = requests.post(url2, headers = header2, data = payload2, verify = False)
    print(r2)
    return(r2.cookies, unquote(r1.cookies['XSRF-TOKEN']))

def logout(url):
    header = {
       'content-type': 'application/json'
    }
    r = requests.get(url + '/api/auth/logout', headers = header, verify = False)
    return(r)

def create_session(url, Lab, cookie):
    Lab = '{ "path": "/'+Lab+'.unl" }'
    r = requests.post( \
       url+'/api/labs/session/factory/create', \
       data = Lab, \
       headers = {'content-type': 'application/json'}, \
       cookies=cookie, verify=False \
    )
    return(r)

def get_session(url, cookie):
    r = requests.get(
       url + '/store/public/admin/lab_sessions/getSession', 
       headers = {'content-type': 'application/json'}, 
       cookies = cookie, 
       verify = False
    )
    session_id = r.json()['data']
    return(session_id)

def destroy_session(url, lab_session_id, cookie):
    lab_session_id = '{"lab_session":"' + str(lab_session_id) + '"}'
    r = requests.post( \
       url + '/api/labs/session/factory/destroy',  \
       data = lab_session_id, \
       headers = {'content-type': 'application/json'}, \
       cookies = cookie, verify=False
    )
    return(r)

def join_session( url, lab_session_id, cookie ):
    lab_session_id = '{"lab_session":"' + str(lab_session_id) + '"}'
    r = requests.post( \
       url + '/api/labs/session/factory/join',  \
       data = lab_session_id,  \
       headers = {'content-type': 'application/json'},  \
       cookies = cookie, \
       verify = False \
    )
    return(r)

def read_session(url, lab_session_id, cookie):
    lab_session_id='{"lab_session":"' + str(lab_session_id) + '"}'
    r = requests.post( \
       url + '/store/public/admin/lab_sessions/read',  \
       data = lab_session_id, \
       headers = {'content-type': 'application/json'},  \
       cookies = cookie, \
       verify = False \
    )
    return(r)

def leave_session(url, Lab, cookie):
    Lab='{"path": "/'+Lab+'.unl"}'
    r = requests.post( \
       url + '/api/labs/session/factory/leave',  \
       data = Lab,  \
       headers = {'content-type': 'application/json'},  \
       cookies = cookie,  \
       verify = False \
    )
    return(r)

def get_sessions_count(url, cookie):
    r = requests.get( \
        url + '/store/public/admin/lab_sessions/count', \
        headers = {'content-type': 'application/json'}, \
        cookies = cookie,    \
        verify=False \
    )
    return(r)


def filter_session(url, cookie, xsrf, page_number = 1, page_quantity = 25):
    header = {
        "Content-Type": "application/json;charset=UTF-8",
        "X-XSRF-TOKEN":xsrf
    }
    payload = json.dumps( \
        {   \
            "data": {   \
                "page_number": page_number,    \
                "page_quantity": page_quantity, \
                "page_total": 0,     \
                "flag_filter_change": True,  \
                "flag_filter_logic": "and",  \
                "data_sort": {              \
                    "lab_session_id": "desc" \
                },  \
                "data_filter": {}   \
            }   \
        }   \
    )
    r = requests.post( \
       url + '/store/public/admin/lab_sessions/filter',  \
       headers = header, \
       data = payload, \
       cookies = cookie, verify = False \
    )
    return(r)

def filter_user(url, cookie, xsrf):
    header = {
       "Content-Type": "application/json;charset=UTF-8",
       "X-XSRF-TOKEN":xsrf
    }
    payload = json.dumps(
        {
            "data": {
                "page_number": 1,
                "page_quantity": 25,
                "page_total": 0,
                "flag_filter_change": True,
                "flag_filter_logic": "and",
                "data_sort": {
                    "online_time": "desc"
                },
                "data_filter": {}
            }
        }
    )
    r = requests.post(  \
        url + '/store/public/admin/users/filter',   \
        headers = header,   \
        data = payload,     \
        cookies = cookie,   \
        verify = False      \
    )
    return(r)


def get_nodes(url, cookie):
    # ids=[]
    r = requests.get( \
       url + '/api/labs/session/topology',  \
       headers = {'content-type': 'application/json'},  \
       cookies = cookie,  \
       verify = False  \
    )
    return(r)

def start_node(url, cookie, node):
    node_id='{"id":"' + str(node) + '"}'
    r = requests.post( \
        url + '/api/labs/session/nodes/start',  \
        headers = {'content-type': 'application/json'},  \
        data = node_id, \
        cookies = cookie,  \
        verify = False  \
    )
    return r

def stop_node(url, cookie, node):
    node_id='{"id":"' + str(node) + '"}'
    r = requests.post( \
        url + '/api/labs/session/nodes/stop',  \
        headers = {'content-type': 'application/json'},  \
        data = node_id, \
        cookies = cookie,  \
        verify = False  \
    )
    return r

def nodes_status(url, cookie):
    
    r = requests.post( \
        url + '/api/labs/session/nodestatus',  \
        headers = {'content-type': 'application/json'},  \
        cookies = cookie,  \
        verify = False  \
    )
    return r.json()
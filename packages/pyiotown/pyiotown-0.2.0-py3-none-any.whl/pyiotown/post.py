import requests
import threading
from urllib.parse import urlparse
import paho.mqtt.client as mqtt
import json

def uploadImage(url, token, payload):
    '''
    url : IoT.own Server Address
    token : IoT.own API Token
    payload : Image + Annotation Json Data (check format in README.md)
    '''
    apiaddr = url + "/api/v1.0/nn/image"
    header = {'Content-Type': 'application/json', 'Token': token}
    try:
        r = requests.post(apiaddr, data=payload, headers=header, verify=False, timeout=10)
        if r.status_code == 200:
            return True
        else:
            print(r.content)
            return False
    except Exception as e:
        print(e)
        return False
def data(url, token, nid, data, upload=""):
    '''
    url : IoT.own Server Address
    token : IoT.own API Token
    type: Message Type
    nid: Node ID
    data: data to send (JSON object)
    '''
    typenum = "2" # 2 static 
    apiaddr = url + "/api/v1.0/data"
    if upload == "":
        header = {'Accept':'application/json', 'token':token } 
        payload = { "type" : typenum, "nid" : nid, "data": data }
        try:
            r = requests.post(apiaddr, json=payload, headers=header, verify=False, timeout=10)
            if r.status_code == 200:
                return True
            else:
                print(r.content)
                return False
        except Exception as e:
            print(e)
            return False
    else:
        header = {'Accept':'application/json', 'token':token } 
        payload = { "type" : typenum, "nid" : nid, "meta": json.dumps(data) }
        try:
            r = requests.post(apiaddr, data=payload, headers=header, verify=False, timeout=10, files=upload)
            if r.status_code == 200:
                return True
            else:
                print(r.content)
                return False
        except Exception as e:
            print(e)
            return False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connect OK! Subscribe Start")
    else:
        print("Bad connection Reason",rc)

def post_files(result, url, token):
    if 'data' not in result.keys():
        return result
    
    for key in result['data'].keys():
        if type(result['data'][key]) is dict:
            resultkey = result['data'][key].keys()
            if ('raw' in resultkey) and ( 'file_type' in resultkey) :
                header = {'Accept':'application/json', 'token':token }
                upload = { key + "file": result['data'][key]['raw'] }
                try:
                    r = requests.post( url + "/api/v1.0/file", headers=header, verify=False, timeout=10, files=upload )
                    if r.status_code == 200:
                        del result['data'][key]['raw']
                        result['data'][key]['file_id'] = r.json()["files"][0]["file_id"]
                        result['data'][key]['file_ext'] = r.json()["files"][0]["file_ext"]
                        result['data'][key]['file_size'] = r.json()["files"][0]["file_size"]
                    else:
                        print("[ Error ] while send Files to IoT.own. check file format ['raw, file_type]")
                        print(r.content)
                except Exception as e:
                    print(e)
            # post post process apply.
    return result
def on_message(client, userdata, msg):
    data = json.loads((msg.payload).decode('utf-8'))
    result = userdata['func'](data)
    if type(result) is dict:
        post_result = post_files(result, userdata['url'], userdata['token'])
        # result = json.dumps(result).encode('utf-8')
        # print("post process done. publish result")
        print("post process Done. publish results")
        client.publish('iotown/proc-done', json.dumps(post_result), 1)
    else:
        print("CALLBACK FUNCTION TYPE ERROR [", type(result) ,"]must [ dict ]")
        client.publish('iotown/proc-done', msg.payload, 1)

    
def updateExpire(url, token, name):
    apiaddr = url + "/api/v1.0/pp/proc"
    header = {'Accept':'application/json', 'token':token}
    payload = { 'name' : name}
    try:
        r = requests.post(apiaddr, json=payload, headers=header, verify=False, timeout=10)
        if r.status_code == 200 or r.status_code == 403:
            print("update Expire Success")
        else:
            print("update Expire Fail! reason:",r)
    except Exception as e:
        print("update Expire Fail! reason:", e)
    timer = threading.Timer(60, updateExpire,[url,token,name])
    timer.start()
def getTopic(url, token, name):
    apiaddr = url + "/api/v1.0/pp/proc"
    header = {'Accept':'application/json', 'token':token}
    payload = {'name':name}    
    try:
        r = requests.post(apiaddr, json=payload, headers=header, verify=False, timeout=10)
        if r.status_code == 200:
            print("Get Topic From IoT.own Success")
            return json.loads((r.content).decode('utf-8'))['topic']
        elif r.status_code == 403:
            print("process already in use. please restart after 1 minute later.")
            return json.loads((r.content).decode('utf-8'))['topic']
        else:
            print(r)
            return None
    except Exception as e:
        print(e)
        return None
def postprocess(url, token, name, func, username, pw):
    # get Topic From IoTown
    topic = getTopic(url,token,name)
    if topic == None:
        raise Exception("Fatal Error")
    else:
        updateExpire(url, token, name)
    # if return typical topic, then updateExpire 60 seconds
    # if return 403 error, that means postprocess already in use at the other 
    #2  func등록 및 ID, PASSWORD 등록하기
    client = mqtt.Client() #client config
    client.on_connect = on_connect # callback function config (on_connect)
    client.on_message = on_message # callback function config (on_message)
    client.username_pw_set(username,pw)

    server_info = { "url":url,"token":token,"func":func}

    client.user_data_set(server_info)
    #3 토픽정보를 가지고 subscribe를 시작한다.
    mqtt_server = urlparse(url).netloc
    print("connect to",mqtt_server)
    client.connect(mqtt_server) # server address
    client.subscribe(topic,1) # subscribe all 'topic#'
    client.loop_forever() # loop forever

def postprocess_common(url, topic, func, username, pw):
    client = mqtt.Client() #client config
    client.on_connect = on_connect # callback function config (on_connect)
    client.on_message = on_message # callback function config (on_message)
    client.username_pw_set(username,pw)
    client.user_data_set(func)
    #3 토픽정보를 가지고 subscribe를 시작한다.
    mqtt_server = urlparse(url).netloc
    print("connect to",mqtt_server)
    client.connect(mqtt_server) # server address
    # topic = 'iotown/proc/common/yolox-x'
    client.subscribe(topic,1) # subscribe all 'topic#'
    client.loop_forever() # loop forever

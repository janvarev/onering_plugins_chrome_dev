# Deepl dev Translate plugin
# author: Vladislav Janvarev

# Solution are HEAVILY inspired by https://github.com/HIllya51/LunaTranslator

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "Deepl Translator through Chrome dev", # name
        "version": "1.0", # version

        "default_options": {
            "port": "9222",  # port
        },

        "translate": {
            "deepl_dev": (init,translate) # 1 function - init, 2 - translate
        }
    }
    return manifest


from traceback import print_exc
import requests, os
from urllib.parse import quote
import re

from urllib.parse import quote
#import websocket as websockets2
from websocket import create_connection
import json
import json
import time

_id = 1


def SendRequest(websocket, method, params):
    global _id
    _id += 1
    websocket.send(json.dumps({'id': _id, 'method': method, 'params': params}))
    res = websocket.recv()
    return json.loads(res)['result']


def waitload(websocket):
    for i in range(10000):
        state = (SendRequest(websocket, 'Runtime.evaluate', {"expression": "document.readyState"}))
        if state['result']['value'] == 'complete':
            break
        time.sleep(0.1)


def waittransok(websocket):
    for i in range(10000):
        state = (SendRequest(websocket, 'Runtime.evaluate', {
            "expression": "document.querySelector('.lmt__side_container--target [data-testid=translator-target-input]').textContent",
            "returnByValue": True}))
        if state['result']['value'] != '':
            return state['result']['value']
        time.sleep(0.1)
    return ''


def translate_websocket(websocketurl, content, src, tgt):
    if 1:
        websocket = create_connection(websocketurl)
        SendRequest(websocket, 'Page.navigate',
                    {'url': 'https://www.deepl.com/en/translator#{}/{}/{}'.format(src, tgt, quote(content))})
        waitload(websocket)
        res = waittransok(websocket)
        return (res)


def createtarget(port):
    url = 'https://www.deepl.com/en/translator'
    infos = requests.get('http://127.0.0.1:{}/json/list'.format(port)).json()
    use = None
    for info in infos:
        if info['url'][:len(url)] == url:
            use = info['webSocketDebuggerUrl']
            break
    if use is None:
        if 1:
            websocket = create_connection(infos[0]['webSocketDebuggerUrl'])
            a = SendRequest(websocket, 'Target.createTarget', {'url': url})
            use = 'ws://127.0.0.1:{}/devtools/page/'.format(port) + a['targetId']

    print("deb url: ", use)
    return use


def start_with_options(core:OneRingCore, manifest:dict):
    pass

def init(core:OneRingCore):
    core.websocketurl = createtarget(core.plugin_options(modname).get("port"))
    pass

def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    res = translate_websocket(core.websocketurl, text, from_lang, to_lang)


    return res

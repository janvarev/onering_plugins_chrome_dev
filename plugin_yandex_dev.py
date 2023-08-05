# Yandex dev Translate plugin
# author: Vladislav Janvarev

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "Yandex Translator through Chrome dev", # name
        "version": "1.0", # version

        "default_options": {
            "port": "9222",  # port
            "lang_pairs": "ru->en,en->ru"
        },

        "translate": {
            "yandex_dev": (init,translate) # 1 function - init, 2 - translate
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
        state = (SendRequest(websocket, 'Runtime.evaluate',
                             {"expression": 'document.querySelector("#translation > span").innerText',
                              "returnByValue": True}))
        if state['result'].get('value') is not None:
            if state['result'].get('value') != "":
                return state['result'].get('value')
        time.sleep(0.1)
    return ''


def tranlate_old(websocketurl, content, src, tgt):
    if 1:
        websocket = create_connection(websocketurl)
        SendRequest(websocket, 'Runtime.evaluate',
                    {"expression": 'document.querySelector("#translation > span").innerText=""'})
        SendRequest(websocket, 'Runtime.evaluate', {
            "expression": 'i=document.querySelector("#fakeArea");i.innerText=`{}`;event = new Event("input", {{bubbles: true, cancelable: true }});i.dispatchEvent(event);'.format(
                content)})

        waitload(websocket)
        res = waittransok(websocket)

        return (res)

def tranlate(websocketurl, content, src, tgt):
    if 1:
        # websocket = create_connection(websocketurl)
        # SendRequest(websocket, 'Page.navigate',
        #             {'url': 'https://translate.yandex.com/?source_lang={}&target_lang={}'.format(src, tgt)})
        # waitload(websocket)
        # res2 = waittransok(websocket)
        #time.sleep(0.2)

        websocket = create_connection(websocketurl)
        # SendRequest(websocket, 'Page.navigate',
        #             {'url': 'https://translate.yandex.com/?source_lang={}&target_lang={}'.format(src, tgt)})
        # time.sleep(0.3)
        SendRequest(websocket, 'Runtime.evaluate',
                    {"expression": 'document.querySelector("#translation > span").innerText=""'})
        SendRequest(websocket, 'Runtime.evaluate', {
            "expression": 'i=document.querySelector("#fakeArea");i.innerText=`{}`;event = new Event("input", {{bubbles: true, cancelable: true }});i.dispatchEvent(event);'.format(
                content)})

        waitload(websocket)
        res = waittransok(websocket)

        return (res)

def createtarget(port,fr_lang,to_lang):
    url = 'https://translate.yandex.com/?source_lang={}&target_lang={}'.format(fr_lang, to_lang)
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


# class TS(basetrans):
#     def inittranslator(self):
#         self.websocketurl = (createtarget(globalconfig['debugport']))
#
#     def translate(self, content):
#         return ((tranlate(self.websocketurl, content, self.srclang, self.tgtlang)))


def start_with_options(core:OneRingCore, manifest:dict):
    pass

def init(core:OneRingCore):
    core.yandex_dev_dict_websocketurl = {}
    pairs = core.plugin_options(modname).get("lang_pairs").split(",")
    for pair in pairs:
        fr_lang, to_lang = pair.split("->")
        core.yandex_dev_dict_websocketurl[pair] = createtarget(core.plugin_options(modname).get("port"),fr_lang,to_lang)

    #core.websocketurl = createtarget(core.plugin_options(modname).get("port"))
    #pass

def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    res = tranlate(core.yandex_dev_dict_websocketurl.get(f"{from_lang}->{to_lang}"), text, from_lang, to_lang)


    return res

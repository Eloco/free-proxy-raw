#!/usr/bin/env python
# coding=utf-8

import base64
import traceback
import requests
import fire
import os
import json
import time
import httpx

def send_file_github(repo    : str,
                    filename : str,
                    token    : str,
                    content  : str,
                    ) -> bool:
    try:
        if token == "None":
            print(f"need gihtub repo <{repo}> token (at least gist write)")
            return(False)
        else:
            if os.path.exists(content):
                content = open(content,"r").read()
            content=base64.b64encode(content.encode("utf-8")).decode('utf-8')
            print(token)
            headers = {
                'User-Agent'    : 'HTTPie/1.0.3'            ,
                'Accept'        : 'application/json, */*'   ,
                'Connection'    : 'keep-alive'              ,
                'Content-Type'  : 'application/json'        ,
                'Authorization' : 'token '+token            ,
            }
            data    = {
                "message"       : "upload file or message"                                    ,
                "committer"     : { "name"  : "eloco"                          ,
                                    "email" : "eloco@users.noreply.github.com" , } ,
                "content"       : content
            }
            repo     = f"https://api.github.com/repos/{repo}/contents/"
            filename = f"{filename}"
            r        = httpx.put(repo+filename, headers = headers, data = json.dumps(data))

            if str(r.status_code)[:2] == "20":
                print(f"upload github <{repo}> success with {r.status_code}")
                return(True)
            else:
                print(f"[Upload] github-api PUT return: \n{r.text}")
                print(f"upload github <{repo}> failed with {r.status_code}")
                return(False)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return(False)

if __name__ == '__main__':
    while not fire.Fire(send_file_github):
        time.sleep(2)

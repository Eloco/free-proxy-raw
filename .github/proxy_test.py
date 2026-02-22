#!/usr/bin/env python
# coding=utf-8

from playwright.sync_api import sync_playwright
import os
import time

browserType=os.getenv('browserType', 'firefox')
proxy=os.getenv('proxy', 'null')
url=os.getenv('url', 'https://www.google.com/')
sleep=os.getenv('sleep', "30")



with sync_playwright() as playwright:
    if "http://" in proxy:
        launchBrowser = f"""browser = playwright.{browserType}.launch(headless=True,proxy={{"server": "<proxy>"}})"""
        launchBrowser = launchBrowser.replace("<proxy>",proxy)
        print(launchBrowser)
        exec(launchBrowser)
    else:
        launchBrowser = f"""browser = playwright.{browserType}.launch(headless=True)"""
        launchBrowser = launchBrowser.replace("<proxy>",proxy)
        print(launchBrowser)
        exec(launchBrowser)
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(60*3*1000)
    page.goto(url)
    time.sleep(int(sleep))
    content=page.content()

with open("page.html","w") as f:
    f.write(content)


#!/usr/bin/python3.6


from webapp import webappmain

def create_app(test_config = None):
    return webappmain.createapp(test_config)



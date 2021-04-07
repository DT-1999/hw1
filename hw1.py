# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 16:10:49 2021

@author: ustc
"""

# this is a programmon which searches restaurants in a city,and then note down and rank them

from flask import Flask, render_template
import requests
import json
import time
import random
import re
from bs4 import BeautifulSoup

from another_test import getjson, resturants_of_city

if __name__ == '__main__':    
    resturants_of_city('合肥市','蜀山区','瑶海区','包河区','庐阳区') #a city in China, with its four regions
    resturants_of_city('合肥市','蜀山区','瑶海区','包河区','庐阳区').search_and_show()

    
    

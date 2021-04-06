# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 16:10:49 2021

@author: ustc
"""
# anaconda do not support Chinese's utf-8
from flask import Flask, render_template
import requests
import json
import time
import random
import re
from bs4 import BeautifulSoup

from another_test import getjson, resturants_of_city

if __name__ == '__main__':    
    resturants_of_city('合肥市','蜀山区','瑶海区','包河区','庐阳区')
    resturants_of_city('合肥市','蜀山区','瑶海区','包河区','庐阳区').search_and_show()

    
    

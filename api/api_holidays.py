# -*- coding: utf-8 -*-


from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import requests_cache
import re
import urllib2

app = Flask(__name__)

requests_cache.install_cache()

@app.route("/results")

def doc():

	map_month = {
            	'जनवरी' : 'January',
            	'फरवरी' : 'February',
            	'मार्च' : 'March',
            	'अप्रैल' : 'April',
            	'मई' : 'May',
            	'जून' : 'June',
            	'जुलाई' : 'July',
            	'अगस्त' : 'August',
            	'सितंबर' : 'Spetember',
            	'अक्टूबर' : 'October',
            	'नवंबर' : 'Novemeber',
            	'दिसंबर' : 'December'
          	}

	map_day = {
           	'सोमवार' : 'Monday',
           	'मंगलवार' : 'Tuesday',
           	'बुधवार' : 'Wenesday',
           	'गुरुवार' : 'Thursday',
           	'शुक्रवार' : 'Friday',
           	'शनिवार' : 'Saturday',
           	'रविवार' : 'Sunday'
          	}

	url = 'https://www.timeanddate.com/holidays/india/2018'

	req = urllib2.urlopen(url)
	respData = req.read()

	date_with_month = re.findall(r'<th class="nw" >(.*?)</th>',str(respData))
	t_day = re.findall(r'<td class="nw" >(.*?)</td>',str(respData))
	festival = re.findall(r'<td><a href="\S+">(.*?)</a></td>',str(respData))
	h_type = re.findall(r'<td>(?!<)(.*?)</td>',str(respData))

	month = []
	date = []
	day = []

	for i in date_with_month:
    		i = i.split()
    		if i[1] in map_month:
        		month.append(map_month[i[1]])
        		date.append(i[0])

	for i in t_day:
    		if i in map_day:
        		day.append(map_day[i])

	res = []
	n = len(day)
	for i in range(0,n):
    		res.append({"date":date[i],"day":day[i],"month":month[i],"name":festival[i],"type":h_type[i]})

	return jsonify(res)


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)

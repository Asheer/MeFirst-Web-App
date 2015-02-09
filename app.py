from flask import Flask,render_template
from flask import request
from logging import DEBUG
from BeautifulSoup import BeautifulSoup
import urllib2,re,html
from mechanize import Browser
import HTMLParser
import itertools,os
app = Flask(__name__)
app.logger.setLevel(DEBUG)
import foursquare
import sys
import logging
loghandler = logging.StreamHandler(stream=sys.stdout)
foursquare.log.addHandler(loghandler)
foursquare.log.setLevel(logging.DEBUG)
classes = []
classDes = []
prof = []
rooms = []
times = []

classAndDes = []
timeStuff = []
app = Flask(__name__)

@app.route('/')
@app.route('/login')
def homepage():
    return render_template("login.html")

@app.route('/',methods=['POST'])
def my_form_post():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        app.logger.debug(username)
        scrape(username,password)
        return render_template("LOL.html",schedule = zip(classes,classDes,times,rooms,prof))

@app.route('/')
def scrape(username, password):
    home = "https://home.cunyfirst.cuny.edu/oam/Portal_Login1.html"
    br = Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent','Firefox')]
    br.open(home)
    br.select_form(nr=0)
    br.form['login'] = username
    br.form['password'] = password
    br.submit() # login
    response = br.open("https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES_2.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A")
    html = response.read()
    soup = BeautifulSoup(html)
    app.logger.debug(soup.title.string)
    if "Cart" in soup.title.string:
        app.logger.debug("HAHA")
    classIds=soup.findAll('div', {'id' : re.compile('win0divE_CLASS_NAME.*')})
    enrollids = soup.findAll('div', {'id' : re.compile('win0divDERIVED_REGFRM1_SSR_STATUS_LONG.*')})
    classAndEnroll = zip(classIds,enrollids)
    for span,eid in classAndEnroll:
        if "Enrolled" or "SUCCESS" in eid:
           # app.logger.debug(span.text)
            classes.append(span.text)

    classDesIds = soup.findAll('div', {'id' : re.compile('win0divE_CLASS_DESCR.*')})
    desAndEnroll = zip(classDesIds,enrollids)
    for span,eId in desAndEnroll:
        if "Enrolled" or "SUCCESS" in eid:
            span.text.replace("&amp;", "&")
 #           app.logger.debug(span.text)
            classDes.append(span.text)

    profIds = soup.findAll('div',{'id' : re.compile('DERIVED_REGFRM1_SSR_INSTR_LONG.*')})
    profAndEnroll = zip(profIds,enrollids)
    for span,eid in profAndEnroll:
        if "Enrolled" or "SUCCESS" in eid:
  #          app.logger.debug(span.text)
            prof.append(span.text)

    roomIds = soup.findAll('div',{'id' : re.compile('win0divDERIVED_REGFRM1_SSR_MTG_LOC_LONG.*')})
    roomAndEnroll = zip(roomIds,enrollids)
    for span,eid in roomAndEnroll:
        if "Enrolled" or "SUCCESS" in eid:
   #         app.logger.debug(span.text)
            rooms.append(span.text)

    timeIds = soup.findAll('div',{'id' : re.compile('win0divDERIVED_REGFRM1_SSR_MTG_SCHED_LONG.*')})
    timeAndEnroll = zip(timeIds,enrollids)
    for span,eid in timeAndEnroll:
        if "Enrolled" or "SUCCESS" in eid:
    #        app.logger.debug(span.text)
            times.append(span.text)

    classAndDes = classes + classDes
    timeStuff = rooms + times + prof
    app.logger.debug(classAndDes)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 33507))
    app.run(port=port)

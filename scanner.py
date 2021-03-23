# -*- coding: utf-8 -*-
__author__="Waleed & Hamza"
import argparse
import re
import requests
import whois
import utf
import urllib3



parser=argparse.ArgumentParser(description=utf.desc)

# 1.1st
parser.add_argument("action",help="Action:  whois xss sql e-mail credit-card  robots-txt")

parser.add_argument("web_URL",help="URL")
args = parser.parse_args()

url = ""

def whois1(url):
    query = whois.whois(url)
    print "-->Domain: ", query.domain
    print "-->Update time: ", query.get('updated_date')
    print "-->Expiration time: ", query.get('expiration_date')
    print "-->Name server: ", query.get('name_servers')
    print "-->Email: ", query.get('emails')

#1st

def robotstxtAvailable(url):
    url += "/robots.txt"
    try:
        robot = requests.get(url, verify=False)
        if int(robot.status_code) == 200:
            print "-->robots.txt available"
            print "robots.txt:", robot.content
        else:
            print "->robots.txt isn't available"
    except:
        pass


#2nd



def sql(url):
    sqlfile = open("sqlpayload.txt", "r")
    sqlPayload = sqlfile.readlines()
    sqlfile.close()
    if "=" in url:
        find1 = str(url).find('=')
        for i in sqlPayload:
            try:
                i = i.split("\n")[0]
                find2 = str(url[0:find1 + 1]) + str(i)
                find3 = requests.get(find2)
                if int(find3.status_code)==200:
                    print "-->Sqli paylaod: ", str(i)
                    print "-->Sqli URL: ", find2

                else:
                    print "->Sqli paylaod: ", str(i)
                    print "->Sqli URL: ", find2

            except:
                pass
    else:
        print "->Sqli isn't available"

def xss(url):
    xssfile = open("xsspayload.txt", "r")
    xssPayload = xssfile.readlines()
    xssfile.close()
    find4 = url.find("=")
    if "=" in url:
        for i in xssPayload:
            try:
                i = i.split("\n")[0]
                find5 = str(url[:find4 + 1]) + str(i)
                find6 = requests.get(find5)
                if i in find6.content:
                    print "-->XSS payload: ", str(i)
                    print "-->XSS URL: ", find5

                else:
                    print "->XSS payload: ", str(i)
                    print "->XSS URL: ", find5

            except:
                pass
    else:
        print "->XSS isn't available"


#3rd

def mail(url):
    mail1 = requests.get(url, verify=False)
    find7 = re.findall(r'[\w.-]+@[\w.-]+.\w+', mail1.content)
    for i in find7:
        print "-->E-mail: ", str(i)

        
def credit(url):
    credit1 = requests.get(url, verify=False)
    credit2 = str(credit1).split()
    credit3 = str("".join(credit2))
    VISA = re.match(r"^4[0-9]{12}(?:[0-9]{3})?$", credit3)
    MASTERCARD = re.match(r"^5[1-5][0-9]{14}$", credit3)

    try:
        if MASTERCARD.group():
            print "-->Website has a Master Card!"
            print MASTERCARD.group()


    except:
        print "->Website hasn't a Mastercard!"

    try:
        if VISA.group():
            print "-->Website has a VISA card!"
            print VISA.group()

    except:
        print "->Website hasn't a VISA card!"


#4th



if args:
    url = getattr(args, 'web_URL')
    urllib3.disable_warnings()

    print "-->URL:", url, "\n=========="
    if args.action=="sql":
        sql(url)

    elif args.action=="whois":
        whois1(url)

    elif args.action=="xss":
        xss(url)

    elif args.action=="e-mail":
        mail(url)

    elif args.action=="credit-card":
        credit(url)

    elif args.action=="robots-txt":
        robotstxtAvailable(url)

#6th

    else:
        print "Invalid Action"
        exit()

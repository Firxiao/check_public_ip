#!/bin/env python
#-*- coding: utf-8 -*-
"""
usage: when Public IP changed send a mail to you
author: Firxiao
blog: http://firxiao.com
"""

import urllib2
import smtplib  
from email.mime.text import MIMEText  
import ConfigParser
import string, os, sys
import ast



__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

filename = "public_ip.txt"
f = os.path.join(__location__, filename)


cf = ConfigParser.ConfigParser()
config_file = os.path.join(__location__,'conf.ini')
cf.read(config_file)

url = cf.get("url","url")
smtp_server = cf.get("mail_server","smtp_server")
mail_user = cf.get("mail_server","mail_user")
mail_pass = cf.get("mail_server","mail_pass")
mail_postfix = cf.get("mail_server","mail_postfix")


mailto_list = ast.literal_eval(cf.get("user","mailto_list"))

  
def send_mail(to_list,sub,content):
    me="Public_IP_Check"+"<"+mail_user+"@"+mail_postfix+">"   
    msg = MIMEText(content,_subtype='html',_charset='UTF-8')   

    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        s = smtplib.SMTP()  
        s.connect(smtp_server) 
        s.login(mail_user,mail_pass) 
        s.sendmail(me, to_list, msg.as_string())
        s.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  

def get_public_ip():
    res = urllib2.urlopen(url)
    Public_IP_Address = res.read()
    return Public_IP_Address

def record_ip(ip):
    output = open(f,'w')
    output.write(ip)
    print "record IP %s" % ip

def read_ip():
    ip_file =  open(f,'r')
    ip = ip_file.read()
    return ip
    

def main():
    try:
        old_ip = read_ip()
        new_ip = get_public_ip()
        print "old_ip: %s" %old_ip
        print "new_ip: %s" %new_ip
        if(new_ip != old_ip):
            mail_content = "Your Public IP has changed to %s" % new_ip
            if send_mail(mailto_list,"Public IP",mail_content):
                print "mail send success"
                record_ip(new_ip)
            else:
                print "mail send error, please check your [mail_server] config"

        else:
            print "public ip is unchanged; do nothing"

    finally:
        print ""




if __name__ == '__main__':  
    if os.path.exists(f):
        main()
    else:
        new_ip = get_public_ip()
        record_ip(new_ip)
        main()

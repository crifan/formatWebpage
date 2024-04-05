#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
#------------------------------------------------------------------------------
[Function]
this script is prettfy/format the input url/webpage then output it

[Usage]
formatWebpage.py -s http://hi.baidu.com/goodword/blog/item/7affc71996eecb77dbb4bdd7.html
formatWebpage.py -s http://b1.bst.126.net/newpage/r/j/m/m-3/pm.js?v=3422684529 -o 163_js_pm.js
formatWebpage.py -s http://againinput4.blog.163.com/blog/static/17279949120120824544142/ -e GB18030

[Info]
Version : v2012-01-10
Author  : crifan
Mail    : green-waste (at) 163.com

[Other Notes]
1. CSS formatter:
http://www.cleancss.com/
2. javascript formatter
http://www.gosu.pl/decoder/

#------------------------------------------------------------------------------
"""

#---------------------------------import---------------------------------------
import os
import re
import sys
#import math
import time
#import random
#import codecs
#import pickle
import logging
#import binascii
#import urllib
import urllib2
from BeautifulSoup import BeautifulSoup,Tag,CData
from datetime import datetime,timedelta
from optparse import OptionParser
from string import Template,replace
#import xml
#from xml.sax import saxutils

__VERSION__ = 'v2012-01-10'


#------------------------------------------------------------------------------
# just print whole line
def printDelimiterLine() :
    logging.info("%s", '-'*80)
    return 

#------------------------------------------------------------------------------
def main():

    # 0. main procedure begin
    parser = OptionParser()
    parser.add_option("-s","--srcURL",action="store", type="string",dest="srcURL",help="open the input url then output the prettfied version of html/js/... source code")
    parser.add_option("-e","--pageEncode",action="store", type="string",dest="pageEncode",help="Designate the source page encoding. If not set, default is 'utf-8'. If you got messy output page, then you can use this option to mannually designate the source page encoding")
    parser.add_option("-o","--outputName",action="store", type="string",dest="outputName",help="Set the output file name")

    logging.info("Version: %s", __VERSION__)
    logging.info("Note: The outputed page's encode is all 'charset=utf-8'")
    printDelimiterLine()
    
    (options, args) = parser.parse_args()
    # 1. export all options variables
    for i in dir(options):
        exec(i + " = options." + i)

    # 2. open url
    logging.info("Begin to connect to %s",srcURL)
    try :
        req = urllib2.Request(srcURL)
        # emulate web browser to access page
        req.add_header('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.5) Gecko/20070713 Firefox/2.0.0.5')
        page = urllib2.build_opener().open(req).read()
    except urllib2.URLError,reason :
        logging.error("URLError when open %s, reason=%s", srcURL, reason)
        sys.exit(2)
    except urllib2.HTTPError,code :
        logging.error("HTTPError when open %s, code=%s", srcURL, code)
        sys.exit(2)
    else :
        logging.info("Open %s successfully", srcURL)

    # 3. got soup
    if not pageEncode :
        # if open some website/javascript in Netease 163,
        # then should set encoding to GB18030 in most case, otherwise will get messy code !!!
        pageEncode = 'utf-8'
    logging.info("Using %s to encode the opened source page", pageEncode)
    soup = BeautifulSoup(page, fromEncoding=pageEncode)
    soup = soup.prettify()

    logging.debug("------prettified page for %s is:\n%s", srcURL, soup)

    # 4. generate new file name
    if not outputName : # if not set output file name
        slashSplited = srcURL.split('/')
        possibleName = slashSplited.pop(-1)
        while (not possibleName): # name is null
            possibleName = slashSplited.pop(-1)
        if possibleName.find('.') < 0 :
            # not normal name -> add html suffix
            possibleName += '.html'

        # 5. remove invalid char
        filteredName = ''
        pattern = re.compile(r"[\w_\.-=]")
        for c in possibleName :
            if pattern.match(c) :
                # retain this char if is a-z,A-Z,0-9,_,.,-,=
                filteredName += c
        if not filteredName :
            filteredName = datetime.now().strftime('%Y%m%d_%H%M') + '.html'
        outputName = filteredName
    
    # 6. create dir
    curPath = os.getcwd()
    dirToSave = curPath + '/' + 'output'
    fullName = dirToSave + '/' + outputName
    if (os.path.isdir(dirToSave) == False) :
        os.makedirs(dirToSave) # create dir recursively
        logging.info("Create dir %s for save output file %s", dirToSave, outputName)

    # 7. create output file
    # codecs.open -> following newFile.write(soup) will occur UnicodeDecodeError
    #newFile = codecs.open(fullName, 'w', 'utf-8') 
    newFile = open(fullName, 'w')
    if newFile:
        logging.info("Newly created output file: %s", fullName)
    else:
        logging.error("Can not create new output file: %s", fullName)
        sys.exit(2)

    # 8. output prettfied content
    newFile.write(soup)
    newFile.flush()
    newFile.close()
    logging.info("Saved prettified url %s into %s", srcURL, fullName)

#------------------------------------------------------------------------------
# got python script file name itsself
def getScriptSelfFilename() :
    # got script self's name
    # for : python xxx.py -s yyy    # -> sys.argv[0]=xxx.py
    # for : xxx.py -s yyy           # -> sys.argv[0]=D:\yyy\zzz\xxx.py
    argv0List = sys.argv[0].split("\\")
    scriptName = argv0List[len(argv0List) - 1] # get script file name self
    possibleSuf = scriptName[-3:]
    if possibleSuf == ".py" :
        scriptName = scriptName[0:-3] # remove ".py"
    return scriptName

###############################################################################
if __name__=="__main__":
    logging.basicConfig(
                    level    =logging.DEBUG,
                    format   = 'LINE %(lineno)-4d  %(levelname)-8s %(message)s',
                    datefmt  = '%m-%d %H:%M',
                    filename = getScriptSelfFilename() + '.log',
                    filemode = 'w');
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    try:
        main()
    except:
        logging.exception("Unknown Error !")
        raise

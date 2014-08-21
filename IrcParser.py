#! /usr/bin/python
"""
The MIT License (MIT)

Copyright (c) 2014 Kent Huang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import os
import re
import sys

def showUsage(argv):
    print "Usage: %s irclogfile" % argv[0]
    return

def isTargetFileExist(targetFile):
    return os.path.isfile(targetFile)

def filterLoginInfo(eventBody):
    return None,None

def filterMsg(eventBody):
    reObj = re.match(r"<\s?(.*)> (.*)",eventBody)
    if reObj:
        return reObj.group(1),reObj.group(2)
    else:
    	return None,None

def eventLogFilter(eventBody):
    if eventBody[0] == '-':
    	return filterLoginInfo(eventBody)
    elif eventBody[0] == '<':
        return filterMsg(eventBody)
    else:
    	return None,None

def eventLogAnalyzer(event):
    eventInfo = {}
    reObj = re.match(r"(\d\d)\:(\d\d) (.*)",event)
    if reObj:
    	hr = reObj.group(1)
    	min = reObj.group(2)
    	(name,msg) = eventLogFilter(reObj.group(3))
        if name and msg:
            eventInfo['type'] = "msg"
            eventInfo['name'] = name
            eventInfo['msg'] = msg
        else:
            eventInfo['type'] = "state"
        eventInfo['hr'] = hr
        eventInfo['min'] = min
        return eventInfo
    else:
    	return None

def ircParser(targetFile):
    eventList = []
    fd = open(targetFile,'r')

    for event in fd:
    	eventInfo = eventLogAnalyzer(event)
        if eventInfo:
            eventList.append(eventInfo)
    fd.close()
    return eventList

def showEvent(eventList):
    for eventInfo in eventList:
        if eventInfo['type'] == "msg":
            print "[%s:%s] %s: %s" % (eventInfo['hr'], eventInfo['min'], eventInfo['name'], eventInfo['msg'])

def main(argv):
    if len(argv) != 2:
    	showUsage(argv)
        return 0
    else:
    	targetFile = argv[1]
    
    if isTargetFileExist(targetFile):
        print "Start parsing %s..." % targetFile
        eventList = ircParser(targetFile)
        showEvent(eventList)
    else:
    	print "No such file..."

    return 1

if __name__ == '__main__':
    main(sys.argv)

import re
import pycurl
import cStringIO
import urllib
import ConfigParser
import smtplib
import getpass
#import traceback
import requests

Config = ConfigParser.ConfigParser()
Config.read('config.ini')

key = Config.get('personal data', 'key')
sender = Config.get('personal data', 'sender')
receipient = Config.get('personal data', 'receipient')

### Doesn't work in Pycharm-Terminal
#pw = getpass.getpass('Passord: \n')
#print 'Thank you'

###creates new Stringbuffer, cStringIO faster than StringIO
buff = cStringIO.StringIO()
###creates new Curl-Object
c = pycurl.Curl()
url = "https://tc-app.de/raffauf/tcraffauf.dll/sessionID/$/"
###set URL
c.setopt(pycurl.URL, url)
header = ['user-agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0', 'cache-control: max-age=0']
c.setopt(pycurl.HTTPHEADER, header)
###writes response to buffer when performed
c.setopt(c.WRITEFUNCTION, buff.write)
###easier debugging
#c.setopt(c.VERBOSE, True)
###executes a HTTP-Request
c.perform()
#print buff.getvalue()
response = buff.getvalue()
###regex response for new SessionID
front = "tcraffauf.dll/"
back = "/$/"
sessionID = response[(response.index(front)+len(front)):response.index(back)]
print "SessionID = " + sessionID

newURL = "https://tc-app.de/raffauf/tcraffauf.dll/" + sessionID + "/$/"
c.setopt(c.URL, newURL)

#TODO: send new request with sessionID + POSTparameters
newBuff = cStringIO.StringIO()
data = (('VSTATUS', '0'), ('ARZTWAHL', '0'), ('PATIENTSTATUS', '0'), ('IW_Action', 'IWGRADBUTTON1'),
        ('IW_ActionParam', ''), ('IW_FormName', 'IWForm1'), ('IW_FormClass', 'TIWForm1'), ('IW_LocationHash', ''),
        ('IW_TrackID', '2'), ('IW_width', '1280'), ('IW_height', '648'), ('IW_SessionID_', sessionID),
        ('IWGRADBUTTON1', ''))

c.setopt(c.POST, 1)
post = urllib.urlencode(data)
c.setopt(c.POSTFIELDS, post)
c.setopt(c.WRITEFUNCTION, newBuff.write)
c.perform()
print newBuff.getvalue()

#TODO: parse date
responseCal = newBuff.getvalue()
freedate = 'CS6' in responseCal
print len(responseCal.split('\n'))

#print type(responseCal)

#print re.search('CS5', responseCal)

#for free in re.finditer('CS5', responseCal):
#        print free.start(), free.end(), free.group()

#front1 = "SubmitClickConfirm('KALENDER'"
#back1 = "</a></td><td class=\"KALENDER_CS5\">"
#cs6 = response[(responseCal.index(front1)+len(front1)):responseCal.index(back1)]

#print cs6
#print '----------POST ' + ''.join(post)

#TODO: send mail
print freedate

if freedate:
        request_url = 'https://api.mailgun.net/v3/sandboxa394801553fc40438ad32d792bd8068c.mailgun.org/messages'.format(sandbox)
        request = requests.post(request_url, auth=('api', key), data={
        'from': 'postmaster@sandboxa394801553fc40438ad32d792bd8068c.mailgun.org',
        'to': 'v.koehring@gmail.com',
        'subject': 'Free appointment! :)',
        'text': 'Go, get it!'
        })
        print 'Status: {0}'.format(request.status_code)
        print 'Body:   {0}'.format(request.text)

###closes buffer
newBuff.close()
buff.close()
###ends curl-session
c.close()

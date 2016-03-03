import pycurl
import cStringIO
import urllib

#creates new Stringbuffer, cStringIO faster than StringIO
buff = cStringIO.StringIO()
#creates new Curl-Object
c = pycurl.Curl()
url = "https://tc-app.de/raffauf/tcraffauf.dll/sessionID/$/"
#set URL
c.setopt(pycurl.URL, url)
header = ['user-agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0', 'cache-control: max-age=0']
c.setopt(pycurl.HTTPHEADER, header)
#writes response to buffer when performed
c.setopt(c.WRITEFUNCTION, buff.write)
#easier debugging
c.setopt(c.VERBOSE, True)
#executes a HTTP-Request
c.perform()
print buff.getvalue()
response = buff.getvalue()
#regex response for new SessionID
front = "tcraffauf.dll/"
back = "/$/"
sessionID = response[(response.index(front)+len(front)):response.index(back)]
print "SessionID = " + sessionID

newURL = "https://tc-app.de/raffauf/tcraffauf.dll/" + sessionID + "/$/"
c.setopt(c.URL, newURL)

#TODO: send new request with sessionID + POSTparameters
#new Buffer needed?
newBuff = cStringIO.StringIO()
data = (('VSTATUS', '0'), ('ARZTWAHL', '0'), ('PATIENTENSTATUS', '0'), ('IW_Action', 'IWGRADBUTTON1'),
        ('IW_ActionParam', ''), ('IW_FormName', 'IWForm1'), ('IW_FormClass', 'TIWForm1'), ('IW_LocationHash', ''),
        ('IW_TrackID', '2'), ('IW_width', '1280'), ('IW_height', '648'), ('IW_SessionID_', sessionID),
        ('IWGRADBUTTON1', ''))
header.append('Referer: https://tc-app.de/raffauf/tcraffauf.dll/sessionID/$/')
#set new Header, expects list or tuple of strings
c.setopt(pycurl.HTTPHEADER, header)

print '----------' + ''.join(header)

c.setopt(c.POST, 1)
post = urllib.urlencode(data)
c.setopt(c.POSTFIELDS, post)
c.setopt(c.WRITEFUNCTION, newBuff.write)
c.perform()
print newBuff.getvalue()

#closes buffer
newBuff.close()
buff.close()
#ends curl-session
c.close()

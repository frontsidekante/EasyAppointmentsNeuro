import pycurl
import cStringIO
import re
import requests

#creates new Stringbuffer, cStringIO faster than StringIO
buff = cStringIO.StringIO()
#creates new Curl-Object
c = pycurl.Curl()
#url = "www.google.de"
#url = "http://tc-app.de"
url = "https://tc-app.de/raffauf/tcraffauf.dll/sessionID/$/"
#set URL
c.setopt(pycurl.URL, url)
c.setopt(pycurl.HTTPHEADER, ['user-agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0', 'cache-control: max-age=0'])
#writes response to buffer when performed
c.setopt(c.WRITEFUNCTION, buff.write)
#executes a HTTP-Request

#c.setopt(c.VERBOSE, True)
c.perform()
print buff.getvalue()

response = buff.getvalue()
#regex response for new SessionID
front = "tcraffauf.dll/"
back = "/$/"

sessionID = response[(response.index(front)+len(front)):response.index(back)]
print sessionID

buff.close()
#ends curl-session
c.close()

import urllib2
import time as t

url = "https://na.api.pvp.net/api/lol/na/v4.1/game/ids?beginDate=%s&api_key=915c95f3-f17c-494b-9b80-732bd34f44d9"
time = 1429075500

f = open('gameIds.txt', 'a+')
while True:
	print "Current time: " + str(time)
	req = urllib2.Request(url % str(time))
	req.add_header('Accept', 'application/json')
	try:
		res = urllib2.urlopen(req)
		results = res.read()
		result_list = eval(results)
		for r in result_list:
			f.write(str(r) + "\n")
		time += 300
	except IOError as e:
		print "Sleeping"
		f.close()
		t.sleep(900)
		f = open('gameIds.txt', 'a+')
f.close()
print 'done'

# up to but not including 1428098400 uploaded to dropbox

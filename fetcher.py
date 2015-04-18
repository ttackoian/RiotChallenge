import urllib2
import time as t
import json
import scipy.io
import glob


champListUrl = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?api_key=915c95f3-f17c-494b-9b80-732bd34f44d9"
res = urllib2.urlopen(champListUrl)
result = res.read()
result = json.loads(result)
champs = result["data"]

i = 0
champ2Feature = {}
id2Name = {}
nameToFeature = {}
for champ in champs.keys():
	currChamp = champs[champ]
	champ2Feature[currChamp["id"]] = i
	id2Name[currChamp["id"]] = currChamp["name"]
	nameToFeature[currChamp["name"]] = i
	i += 1

url = "https://na.api.pvp.net/api/lol/na/v2.2/match/%s?api_key=915c95f3-f17c-494b-9b80-732bd34f44d9"

req = None
trainingData = []
trainingLabels = []

zeros = []
for _ in range(len(champ2Feature.keys())):
	zeros.append(0)

numProcessed = 0
with open('testIds.txt', 'r') as f:
	for gameId in f:
		while True:
			try:
				req = urllib2.Request(url % gameId[:-1])
				req.add_header('Accept-Language', 'en-US')
				req.add_header('Accept-Charset', 'ISO-8859-1,utf-8')
				res = urllib2.urlopen(req)
				results = res.read()
				results = json.loads(results)

				winner, loser = None, None
				team1 = list(zeros)
				team2 = list(zeros)
				for participant in results["participants"]:
					if participant["teamId"] == 100:
						team1[champ2Feature[participant["championId"]]] = 1
					else:
						team2[champ2Feature[participant["championId"]]] = 1
				if results["teams"][0]["teamId"] == 100 and results["teams"][0]["winner"]:
					winner, loser = team1, team2
				elif results["teams"][0]["teamId"] == 200 and results["teams"][0]["winner"]:
					winner, loser = team2, team1
				elif results["teams"][1]["teamId"] == 100 and results["teams"][1]["winner"]:
					winner, loser = team1, team2
				else:
					winner, loser = team2, team1

				trainingData.append(winner)
				trainingLabels.append(1)

				trainingData.append(loser)
				trainingLabels.append(0)
				break
			except IOError as e:
				print "Sleeping...finished processing " + str(numProcessed) + " game IDs."
				t.sleep(9)
		numProcessed += 1


filedict = {"trainingData" : trainingData, "trainingLabels" : trainingLabels}
scipy.io.savemat('riotData.mat', filedict)

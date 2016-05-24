import requests
import time
import json
from datetime import datetime
KEY  = "8bf96ba6-e94d-43fc-a892-06eac23bae66"


def getSummonerId(summonerName):
	url = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/" + summonerName + "?api_key=" + KEY
	r = requests.get(url)
	return r.json()

def getMatchHistory(summonerId,season=None):
	url = "https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/"+ summonerId +"?rankedQueues=TEAM_BUILDER_DRAFT_RANKED_5x5&seasons=SEASON2016" + "&endTime=" + "1464058733754" "&api_key=" + KEY
	r = requests.get(url)
	return r.json()

def getMatchResults(matchId,summonerName="JimmyScene",duoName="Camel Jesus"):
	url = "https://na.api.pvp.net/api/lol/na/v2.2/match/"+ matchId + "?api_key=8bf96ba6-e94d-43fc-a892-06eac23bae66"
	r = requests.get(url)
	results = r.text
	results = json.loads(results)

	try:
		# print(datetime.fromtimestamp(results["matchCreation"] /1000).ctime())
		myId = None
		withDuo = False
		for x in results["participantIdentities"]:
			if(x["player"]["summonerName"] == summonerName):
				myId=x["participantId"]
			if(x["player"]["summonerName"] == duoName):
				withDuo = True
		
		if(myId==None):
			return -1
		else:
			result = results["teams"][0]["winner"]
			winner = result if myId<6 else not result 
			
			return {
			"won" : winner ,
			"withDuo": withDuo
			}
	except KeyError:
		if(results["status"]["status_code"]==429):
			time.sleep(8)
			return getMatchResults(matchId)
		elif(results["status"]["status_code"]==404):
			return {"error": 404, "url": url}



if __name__ == '__main__':
	summoner = "Jimmyscene".lower()	
	x= str(getSummonerId(summoner)[summoner]["id"])
	matchHistory = getMatchHistory(x)
	total = matchHistory["totalGames"]
	winsDuo = 0
	gamesDuo =0
	winsSolo = 0
	gamesSolo =0
	index=0
	for match in matchHistory["matches"]:
		print(str(index) + " /" + str(total))
		match=str(match["matchId"])
		result = getMatchResults(match)
		if(result !=None):
			if(result["withDuo"]):
				gamesDuo+=1
				if(result["won"]):
					winsDuo+=1
			else:
				gamesSolo+=1
				if(result["won"]):
					winsSolo+=1
			index+=1
	print("With Duo:")
	print("Won: " + str(winsDuo) + "Out of " + str(gamesDuo) )
	print("Solo: ")
	print("Won: " + str(winsSolo) + "Out of " + str(gamesSolo) )


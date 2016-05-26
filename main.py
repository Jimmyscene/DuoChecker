#!/usr/bin/env python3
import requests
import time
import json
import sys
import pdb
from datetime import datetime


KEY  = "8bf96ba6-e94d-43fc-a892-06eac23bae66"

class DuoChecker:
	def __init__(self):
		self.getSummoner()
		self.getDuo()
		self.getSummonerId()
		self.season = None
		self.calculate()

	def calculate(self):
		matchHistory = self.getMatchHistory()
		try:
			total = matchHistory["totalGames"]
		except Exception as e:
			sys.exit("Errored")
		winsDuo,gamesDuo, winsSolo, gamesSolo = 0,0,0,0
		for index,match in enumerate(matchHistory["matches"]):
			sys.stdout.flush()
			sys.stdout.write("\r%d%%" % (index*100/total))
			match=str(match["matchId"])
			try:
				result = self.getMatchResults(match)
			except Exception as e:
				print(e)
				print("Could not get Match Results for: %s" % match)
			if(result !=-1):
				if(result["withDuo"]):
					gamesDuo+=1
					if(result["won"]):
						winsDuo+=1
				else:
					gamesSolo+=1
					if(result["won"]):
						winsSolo+=1
			
		print()
		print("Duo Winrate: %d%%" % (winsDuo*100/gamesDuo) )
		print("Solo Winrate: %d%%" % (winsSolo*100/gamesSolo)  )
		print("With Duo:")
		print("Won: %s Out of %s " %(winsDuo,gamesDuo))
		print("Solo: ")
		print("Won: %s Out of %s " %(winsSolo,gamesSolo))
			

	def getSummonerId(self):
		url = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/%s,%s?api_key=%s"% (self.summonerName.lower(),self.duoName.lower(),KEY)
		response = requests.get(url)
		try: 
			summoner = response.json()[self.summonerName.replace(" ","").lower()]
			self.summonerName = summoner["name"] 
			self.summonerId = summoner["id"]
			duo = response.json()[self.duoName.replace(" ","").lower()]
			self.duoName = duo["name"]
			self.duoId = duo["id"]
		except Exception as e:
			if(response.status_code == 404):
				print("Neither Summoner nor Duo could be found.")
				self.getSummoner()
				self.getDuo()
				self.getSummonerId()
			else:
				e = str(e).replace('\'','')
				if(e == self.summonerName.lower()):
					print("%s Could Not Be Found" % self.summonerName)
					self.getSummoner()
					self.getSummonerId()
				elif(e == self.duoName.lower()):
					print("%s Could Not Be Found" % self.duoName)
					self.getDuo()
					self.getSummonerId()
				else:
					print( e == self.duoName.lower())
					print(e)
					print(self.duoName.lower())
					sys.exit()
			


	def getMatchHistory(self):
		now = 1464058733754 #int(round(time.time()*1000))
		url = "https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/%s?rankedQueues=TEAM_BUILDER_DRAFT_RANKED_5x5&seasons=SEASON2016&endTime=%d&api_key=%s" % (self.summonerId,now,KEY)
		response = requests.get(url)
		return response.json()

	def getMatchResults(self,matchId):
		url = "https://na.api.pvp.net/api/lol/na/v2.2/match/%s?api_key=%s" % (matchId,KEY)
		response = requests.get(url)
		results = response.text
		results = json.loads(results)
		try:
			myId = None
			withDuo = False
			for x in results["participantIdentities"]:
				if(x["player"]["summonerName"] == self.summonerName):
					myId=x["participantId"]
				if(x["player"]["summonerName"] == self.duoName):
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
		except KeyError as e:
			status_code = results["status"]["status_code"]
			if(status_code in {429,500} ):
				time.sleep(4)
				return self.getMatchResults(matchId)
			elif(status_code == 404):
				return {"error": 404, "url": url}
			else:
				print(results)
				sys.exit()
	def getSummoner(self):
		self.summonerName = input("Please Input Your Name:")
	def getDuo(self):
		self.duoName = input("Please Input Duo's Name:")



if __name__ == '__main__':
	DuoChecker()
	

	

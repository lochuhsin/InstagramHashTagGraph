from Core.Service.crawlInstagramService import crawlInstagramService


crawl = crawlInstagramService()


with open('dataBase/instagramAccountInfo.json','r') as f:
	import json
	file = json.load(f)


crawl.setupLoginAccount(username = file['account1']["account"],password = file['account1']["password"])
crawl.start()
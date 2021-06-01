from Dao.Repository.dataRepo import dataRepo
from Dao.Model.instagramPostModel import instagramPostModel
from collections import defaultdict
import copy

class dataProcessService(object):

	def __init__(self):
		self.instagramPostIdPath   = './dataBase/instagramPostIdList.json'
		self.instagramHashTagPath  = './dataBase/instagramHashTagList.json'
		self.instagramPostPath     = './dataBase/instagramPostList.json' 
		self.instagramHashTagGraphPath = './dataBase/instagramHashTagGraph.json' 
		self.instagramLoginAccountPath = './dataBase/instagramAccountInfo.json'


	def getInstagramPostIdList(self):
		return dataRepo(self.instagramPostIdPath).getDataFromJson()

	def getInstagramHashTagList(self):
		return dataRepo(self.instagramHashTagPath).getDataFromJson()

	def getInstagramPostList(self):
		return dataRepo(self.instagramPostPath).getDataFromJson()

	def getInstagramHashTagGraph(self): ##### defaultdict
		graphdic = dataRepo(self.instagramHashTagGraphPath).getGraphFromJson()
		return defaultdict(dict,graphdic) if graphdic != None else {}

	def saveInsPostData(self,data): ## data must be instagramPostModel

		instagramPosts = copy.copy(data.getPosts())
		idlist      = copy.copy(self._getPostIdList(instagramPosts))
		HashTaglist = copy.copy(self._getHashTagList(instagramPosts))

		inspostrepo = dataRepo(self.instagramPostIdPath)
		inspostrepo.saveDataToJson(idlist)

		hashtagrepo = dataRepo(self.instagramHashTagPath)
		hashtagrepo.saveDataToJson(HashTaglist)

		originalrepo = dataRepo(self.instagramPostPath)
		originalrepo.saveDataToJson(instagramPosts)

		graphrepo = dataRepo(self.instagramHashTagGraphPath)
		graphrepo.saveGraphToJson(self._addNewItem(instagramPosts))

	def _addNewItem(self,instagramPost):
		oldGraph = self.getInstagramHashTagGraph()
		for post in instagramPost:
			hashtags = post['postHashTag']
			for i in range(len(hashtags)):
				for j in range(i+1,len(hashtags)):
					oldGraph = self._addNewNode(oldGraph,hashtags[i],hashtags[j])
		return oldGraph

	def _addNewNode(self,container,item1,item2,edgs=1):

		if (item1 in container.keys()) and (item2 in container.keys()):
			if (item1 not in container[item2].keys()):
				container[item2][item1] = edgs
				container[item1][item2] = edgs
			elif(item1 in container[item1].keys()):
				container[item1][item2] += edgs
				container[item2][item1] += edgs

		else: 
			container[item1][item2] = edgs
			container[item2][item1] = edgs

		return container


	def _getPostIdList(self,data):
		return [i['postId'] for i in data]

	def _getHashTagList(self,data):
		return [tag for i in data for tag in i['postHashTag']]


		 



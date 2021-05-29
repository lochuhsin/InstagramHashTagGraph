import copy


class instagramPostModel(object):

	def __init__(self): 
		self.instagramPostContainerdict = []


	def addPost(self,dictionary=None):
		"""
		dictionary should contains the following keys
		1. postId
		2. postDate
		3. postHashTag
		4. postLike
		"""
		if self._checkIsDataValid(dictionary):
			dic = copy.deepcopy(dictionary)
			self.instagramPostContainerdict.append(dictionary)
		else:
			print('datatype or keys is not valid')
			

			
	def getPosts(self):
		return self.instagramPostContainerdict


	def _checkIsDataValid(self,dic):

		dicKeys = ['postId','postDate','postHashTag','postLike']

		for i in dic.keys():
			if i not in dicKeys:
				return False
		return True


from collections import defaultdict

class hashTagGraph(object):

	def __init__(self):

		self.container = defaultdict(dict)


	def add(self,item1,item2,edgs=1):

		if (item1 in self.container.keys()) and (item2 in self.container.keys()):
			if (item1 not in self.container[item2].keys()):
				self.container[item2][item1] = edgs
				self.container[item1][item2] = edgs
			elif(item1 in self.container[item1].keys()):
				self.container[item1][item2] += edgs
				self.container[item2][item1] += edgs

		else: 
			self.container[item1][item2] = edgs
			self.container[item2][item1] = edgs

	def setGraph(self,data):
		self.container = defaultdict(dict,data)

	def getGraph(self):
		return copy.deepcopy(self.container)






























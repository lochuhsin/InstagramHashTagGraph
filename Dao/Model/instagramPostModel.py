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































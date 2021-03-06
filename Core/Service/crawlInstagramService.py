from Core.Service.webOperationService import webOperationService
from Core.Service.webOperationService import elementOperation
from Core.Service.dataProcessService import dataProcessService
from Dao.Model.instagramPostModel import instagramPostModel
from Dao.Repository.dataRepo import dataRepo
import copy
import random
import time

class crawlInstagramService(object):

	def __init__(self):

		self.insMainPage = 'mainPage'
		self.insMainPageUrl = "https://www.instagram.com/"
		self.heightPerRoll = 1000
		self.web = None
		self.ele = None

		self.insPostIdList = None
		self.dataProcessService = None


	def setupLoginAccount(self,username = None,password = None):
		self.username = username
		self.password = password


	def start(self):
		username = self.username
		password = self.password
		if username == None or password == None:
			raise ValueError("Please setup username & password")
		
		self.dataProcessService = dataProcessService()
		self.web = webOperationService()
		self.ele = elementOperation()


		#Open new page , Tab & go to instagram
		self.web.openNewPage(self.insMainPage)
		self.web.switchPage(self.insMainPage)
		self.web.goToUrl(self.insMainPageUrl)
		time.sleep(3)
		self.web.login(username,password)
		time.sleep(4)

		#datasetup
		######### Remind that there is still a bug 
		#### when hash tag list is empty ####
		self._getoldPostId()

		hashtaglist = self._getoldhastaglist()
		count = 0
		while count <= len(hashtaglist):
			searchtag = random.choice(hashtaglist)
			print("Crawling hashtag : ",searchtag)

			self.web.goToUrl(self.insMainPageUrl + "explore/tags/" + searchtag)
			time.sleep(random.uniform(2,4))

			insPostModel = self._crawler()

			###### pass post container to data Process #######
			self.dataProcessService.saveInsPostData(insPostModel)
		count += 1


	def _crawler(self):
		insPostModel = instagramPostModel()
		last_height = self.web.getPageHeight()
		while last_height <=5000:
			
			elements = self.web.findElementsByCssSelector('div.v1Nh3.kIKUG._bz0w')

			for ele in elements:
				link = self.ele.getElementAttributeByXpath(ele,"href",".//a")

				######### Check if post already exist ########
				if self._checkIfPostNotExist(link):
					ele.click()
					time.sleep(random.uniform(2,4))

					if (self.web._checkIfElementExist("a.c-Yi7 time") and self.web._checkIfElementExist('a.xil3i')):
						
						post = self._grabInformation(link)
						insPostModel.addPost(post)

					#Close new page tab & return Back to main page
					closesvg = self.web.findElementByCssSelector("svg[aria-label='??????']")
					closesvg.click()
					
				##############################################
			self.web.scrollDownByHeight(self.heightPerRoll)
			last_height = self.web.getPageHeight()

			time.sleep(2)
			if self._checkIsPageBottom(last_height):
				break

		return insPostModel

	def _grabInformation(self,link):
		post = {}
		postOperDic = {'postId':self._getPostId,
						'postDate':self._getPostDate,
						'postHashTag':self._getPostHashTag,
						'postLike':self._getPostLike}
		
		for i in postOperDic.keys():
			if i == 'postId':
				post[i] = postOperDic[i](link)
				self.insPostIdList.append(copy.copy(post[i]))
			else:
				post[i] = postOperDic[i]()

		import pprint
		pprint.pprint(post)
		return post

	def _getPostId(self,link):
		return list(link.split('/'))[-2]

	def _getPostDate(self):
		element = self.web.findElementByCssSelector("a.c-Yi7 time")
		return element.get_attribute('dateTime')

	def _getPostHashTag(self):
		tagElements = self.web.findElementsByCssSelector('a.xil3i')

		tagContainer = []
		for tag in tagElements:
			tagContainer.append(tag.text.replace('#',''))

		return copy.copy(tagContainer)
		
	def _getPostLike(self):
		like = -1
		if(self.web._checkIfElementExist('a.zV_Nj span')):
			element = self.web.findElementByCssSelector('a.zV_Nj span')
			like = element.text

		return like

	def _getoldPostId(self):
		self.insPostIdList = copy.copy(self.dataProcessService.getInstagramPostIdList())

	def _getoldhastaglist(self):
		return self.dataProcessService.getInstagramHashTagList()

	def _checkIsPageBottom(self,height):
		return height == self.web.getPageHeight()

	def _checkIfPostNotExist(self,link):
		return self._getPostId(link) not in self.insPostIdList













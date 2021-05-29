from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import selenium.common.exceptions
import time
import os
import random
import copy


class webOperationService(object):

	def __init__(self):
		self.chrome  = None
		self.tabDic  = {}
		self._setUpWebDriver()


	def _setUpWebDriver(self):
		chromeOptions = webdriver.ChromeOptions()
		chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation'])
		chromeOptions.add_argument("--incognito")

		self.chrome = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',
			options = chromeOptions)
		

	def goToUrl(self,url):
		self.chrome.get(url)


	def openNewPage(self,pageName):
		self.chrome.execute_script("window.open('');")
		self.tabDic[pageName] = self.chrome.window_handles[len(self.chrome.window_handles)-1]
		

	def closePage(self,pageName):
		if self._checkIfPageExist(pageName):
			self.chrome.switch_to.window(self.tabDic[pageName])
			self.chrome.close()

			del self.tabDic[pageName]

	def switchPage(self,pageName):
		if self._checkIfPageExist(pageName):
			self.chrome.switch_to.window(self.tabDic[pageName])
		else:
			print('No page name')		

	def findElementByCssSelector(self,css):
		return self.chrome.find_element_by_css_selector(css)

	def findElementsByCssSelector(self,css):
		return self.chrome.find_elements_by_css_selector(css)

	def login(self,username,password):
		usern = self.chrome.find_element_by_name("username")
		usern.send_keys(username)
	  
		passw = self.chrome.find_element_by_name("password")
		passw.send_keys(password)
	    # sends the enter key
		
		passw.send_keys(Keys.RETURN)

	def closeAllPage(self):
		for i in self.tabDic.keys():
			self.chrome.switch_to.window(self.tabDic[i])
			self.chrome.close()			
		self.tabDic = {}

	def scrollDownByHeight(self,height):
		self.chrome.execute_script("window.scrollTo(0," + str(height) + ")")

	def getPageHeight(self):
		pageheight = self.chrome.execute_script("return document.body.scrollHeight")
		return pageheight

	def _checkIfPageExist(self,pageName):
		return pageName in self.tabDic.keys()

	def _checkIfElementExist(self,css):
		try:
			element=self.chrome.find_element_by_css_selector(css)
		except NoSuchElementException:
			print("No element found",css)
			return False
		return True





class elementOperation(object):

	def __init__(self):
		pass

	def getElementText(self,element):
		return element.text

	def getElementAttribute(self,element,attr):
		return element.get_attribute(attr)

	def getElementAttributeByXpath(self,element,attr,xpath):
		ele = element.find_element_by_xpath(xpath)
		return ele.get_attribute(attr)

	def getElementTextByXpath(self,element,xpath):
		ele = element.find_element_by_xpath(xpath)
		return ele.text






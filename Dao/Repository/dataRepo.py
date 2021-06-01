import json 
import os
import copy


class dataRepo(object):
	


	#### Type of data must be a list

	def __init__(self,path=None):
		self.path = path

	def saveDataToJson(self,data):
		container = copy.deepcopy(data)

		if self._isFileExist():
			oldData = self._getFile()
			for i in container:
				if i not in oldData:
					oldData.append(i)
			self._createFile(oldData)
		else:
			self._createFile(container)

	def saveGraphToJson(self,data):
		container = dict(data)
		self._createFile(container)

	def getGraphFromJson(self):

		if self._isFileExist():
			return self._getFile()
		else:
			return None

	def getDataFromJson(self):
		if self._isFileExist():
			return self._getFile()
		else:
			return[]

	def _isFileExist(self):
		return os.path.isfile(self.path)

	def _getFile(self):
		with open(self.path,'r') as f:
			return json.load(f)

	def _createFile(self,data):
		with open(self.path,'w+') as f:
			json.dump(data,f)






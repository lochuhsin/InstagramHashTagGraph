from Core.Service.dataProcessService import dataProcessService
import copy
import igraph as ig
import chart_studio.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go


class viewHashTagGraph(object):

	def __init__(self):
		self.data = None
		self.oridata = None

		self._getData()


	def setDataThreshold(self,num=None):
		self.data = None #clean data

		data = self.oridata
		newdata = copy.deepcopy(data)

		if num > 0:
			vertices = self._getVertices(data=data,num=num)

			for i in data.keys():
				if i not in vertices:
					del newdata[i]
				else:
					for j in data[i].keys():
						if j not in vertices:
							del newdata[i][j]

			self.data = newdata

		else:
			print("input invalid , must larger than zero")



	def showGraph(self):

		layt,vertices,vertexNumber = self._getGraphInfo()

		edgs = self._getEdgs()


		Xn=[layt[k][0] for k in range(vertexNumber)]
		Yn=[layt[k][1] for k in range(vertexNumber)]
		Zn=[layt[k][2] for k in range(vertexNumber)]

	
		Xe=[]
		Ye=[]
		Ze=[]

		for e in edgs:
			Xe+=[layt[e[0]][0],layt[e[1]][0],None]# x-coordinates of edge ends
			Ye+=[layt[e[0]][1],layt[e[1]][1],None]
			Ze+=[layt[e[0]][2],layt[e[1]][2],None]


		trace1=go.Scatter3d(x=Xe, y=Ye, z=Ze, mode='lines', line=dict(color='rgb(125,125,125)', width=1),hoverinfo='none')

		trace2=go.Scatter3d(x=Xn, y=Yn, z=Zn, mode='markers', name='actors', 
		                   marker=dict(symbol='circle', size=6, colorscale='Viridis', 
		                      line=dict(color='rgb(50,50,50)', width=0.5)), text=vertices, hoverinfo='text')

		axis=dict(showbackground=False, showline=False, zeroline=False, showgrid=False, showticklabels=False, title='')

		layout = go.Layout(
		         title="Network of Instagram HashTag",
		         width=1000,
		         height=1000,
		         showlegend=False,
		         scene=dict(
		             xaxis=dict(axis),
		             yaxis=dict(axis),
		             zaxis=dict(axis),
		        ))

		fig=go.Figure(data=[trace1, trace2], layout=layout)

		plot(fig, filename='ViewHashTagGraph.html')



	def _getData(self):
		datap = dataProcessService()
		self.data = datap.getInstagramHashTagGraph()
		self.oridata = copy.deepcopy(self.data)




	def _getEdgs(self):
		mapping = {}
		keylist = list(self.data.keys())
		for t in range(len(keylist)):
			mapping[keylist[t]] = t

		container = []
		for i in self.data.keys():
			for j in self.data[i].keys():
				temp = [mapping[i],mapping[j]]
				temp.sort()
				setcontainer = (temp[0],temp[1])
				container.append(setcontainer)
		return list(set(container))

	def _getGraphInfo(self):
		data = self.data

		vertices = self._getVertices(data)
		vertexNumber = len(vertices)


		graph = ig.Graph(directed=False)
		graph.es["weight"] = 1.0
		graph.add_vertices(vertices)
		for i in data.keys():
			for j in data[i].keys():
					graph[i,j] = data[i][j]	
		layt = graph.layout('kk', dim=3)	
		

		return 	layt,vertices,vertexNumber


	def _getVertices(self,data=None,num = None):

		vertices = []
		for i in data.keys():
			counter = 0
			if num == None:
				vertices.append(i)
			else:			
				for j in data[i].keys():
					counter+= data[i][j]
				if counter >= int(num):
					vertices.append(i)
		return vertices

		
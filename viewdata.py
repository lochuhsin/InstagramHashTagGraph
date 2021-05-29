from Core.Service.dataProcessService import dataProcessService

service = dataProcessService()

data = service.getInstagramHashTagGraph()
posts = service.getInstagramPostList()
postId = service.getInstagramPostIdList()
print("number of hashtags : ",len(data.keys()))
print("number of posts: ",len(posts))

graph = data

pack10  =0
pack100 = 0
pack1000 = 0
pack10000 = 0
pack100000 = 0
nodeName = []

for i in graph.keys():
	node = graph[i]
	count = 0
	for j in node.keys():
		count += node[j]

	if count > 10 and count <= 100:
		pack10 += 1

	elif count > 100 and count <= 1000:
		pack100 += 1
	elif count > 1000 and count <= 10000:
		pack1000 += 1
	elif count > 10000 and count < 100000:
		pack10000 += 1
	elif count > 100000:
		pack100000 += 1
		nodeName.append(i)



del graph

print("frequency 10 up  number: ",pack10)
print("frequency 100 up  number: ",pack100)
print("frequency 1000 up  number: ",pack1000)
print("10000 up number ",pack10000 )
print("names: ",nodeName)

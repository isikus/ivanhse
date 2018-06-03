import sys
import gensim, logging
import networkx as nx
import matplotlib.pyplot as plt

def get_words(keyword):
	with open(keyword+'.txt','r',encoding='utf-8') as intxt:
		w = intxt.readlines()
		words = [word[:-1] for word in w]
	return words

G = nx.Graph() # пустой граф

m = 'araneum_upos_skipgram_600_2_2017.bin.gz'
model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
print("Model loaded")

model.init_sims(replace=True)

words = get_words('funny')

print("Words accounting started")
for i in range(len(words)):
	# есть ли слово в модели? Может быть, и нет
	if words[i] in model:
		G.add_node(i, label=words[i])
	else:
		# Увы!
		# print(words[i] + ' is not present in the model')
		pass


for i in range(len(words)):
	# есть ли слово в модели? Может быть, и нет
	if words[i] in model:
		for k in range(i+1,len(words)):
			if words[k] in model:
				# print(words[i],words[k],model.similarity(words[i], words[k]))
				if model.similarity(words[i], words[k]) > 0.5:
					G.add_edge(i,k)
			else:
				# Увы!
				# print(words[k] + ' is not present in the model')
				pass
	else:
		# Увы!
		# print(words[i] + ' is not present in the model')
		pass

labels={}
for i in range(len(words)):
	if i in G.nodes():
		labels[i]=words[i]

deg = nx.degree_centrality(G)
degs = sorted(deg, key=deg.get, reverse=True)
print("Топ-5 центральных слов:")
for i in range(0,5):
	print(labels[degs[i]]) # Топ-5 центральных
radii = []
for c in sorted(nx.connected_component_subgraphs(G), key=len, reverse=True):
	try:
		radii.append(nx.radius(c))
	except:
		pass
print()
print("Радиусы для различных компонент связности:")
for r in radii:
	print(r) # Радиус
print()
print("Коэффициент кластеризации:")
print(nx.average_clustering(G)) # Кластеризация

# для начала надо выбрать способ "укладки" графа. Их много, возьмём для начала такой:
pos=nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos, node_color='red', node_size=50) # рисуем узлы красным цветом, задаём размер узла
nx.draw_networkx_edges(G, pos, edge_color='yellow') # рисуем рёбра жёлтым
nx.draw_networkx_labels(G, pos, labels, font_size=10, font_family='Arial')
plt.axis('off') # по умолчанию график будет снабжён осями с координатами, здесь они бессмысленны, так что отключаем
plt.show() # что получилось?

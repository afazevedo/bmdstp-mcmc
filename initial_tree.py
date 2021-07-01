def escolha(node): #escolhe um vizinho aleatoriamente
  vizinhos = list(G.neighbors(node))
  escolhe = np.random.choice(vizinhos)

  return escolhe

def verifica(nodes, path):
  check =  all(item in path for item in nodes)
 
  return check


def random_walk(v_inicial):
  visitado = np.zeros(nx.number_of_nodes(G))
  is_visited = np.zeros(nx.number_of_nodes(G))
  caminho = [v_inicial]
  is_visited[v_inicial] = 1
  aux2 = v_inicial
  nodes = np.array(G.nodes())
  escolhe = escolha(aux2)
  visitado[v_inicial] = escolhe
  visitado[escolhe] = v_inicial
  is_visited[escolhe] = 1
  while True:
    escolhe = escolha(aux2) #escolhe aleatoriamente o vizinho
    if is_visited[escolhe] < 1.0:
      visitado[escolhe] = caminho[len(caminho) - 1]
    is_visited[escolhe] = 1
    caminho.append(escolhe)
    if verifica(nodes, caminho) == True:
      break
    aux2 = escolhe
    
  return caminho, visitado



def generate_random_tree(G):
  x = random.randint(0,nx.number_of_nodes(G) -1)
  print(x)
  path, visitado = random_walk(x)
  print(path)
  print(visitado)
  H = nx.Graph()
  for i in range(len(visitado)):
    H.add_edge(visitado[i],i)

  return H
  




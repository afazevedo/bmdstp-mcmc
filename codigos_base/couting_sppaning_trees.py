import networkx as nx
import numpy as np
import matplotlib as plt
from scipy import linalg


def matrix_sum(A,B):
  C = np.zeros((len(A),len(A)))
  #verificar se A e B tem a mesma quantidade de linhas e colunas
  nLinhasA,nLinhasB  = len(A), len(B)
  nColA, nColB = len(A[0]), len(B[0])
  n = nLinhasA #número de linhas ou colunas
  if nLinhasA == nLinhasB and nColA == nColB:
    #posso somar
    for i in range(n):
      for j in range(n):
        C[i][j] = A[i][j] + B[i][j]
  else:
    print("Matrizes não tem a mesma ordem")
  return C

def oposta(M):
  op = np.zeros((len(M),len(M)))
  for i in range(len(M)):
    for j in range(len(M)):
      op[i][j] = - M[i][j]
  return op

def diag_weight_matrix(num_nodes): #Retorna a matriz
  P = np.zeros((num_nodes,num_nodes))
  for i in range(num_nodes):
    P[i][i] = G.degree(i)
  return P

#para calcular o determinante da matriz basta usar:
#np.linalg.det()

def minor_of_element(A,i,j):
    sub_A = np.delete(A,i-1,0)     # Delete i-th row
    sub_A = np.delete(sub_A,j-1,1) # Delete j-th column
    M_ij = np.linalg.det(sub_A)    # Minor of the element at ith row and jth column
    return np.around(M_ij,decimals=3)  # Rounding the value

def minor_matrix(A):
    m = np.shape(A)[0]    # Order of the matrix
    M_A = np.zeros([m,m])   # Initializing the minor matrix with zeros
    for i in range(1,m+1):
        for j in range(1,m+1):
            M_A[i-1,j-1] = minor_of_element(A,i,j)
    return M_A

def cofactor_matrix(A):
    m = np.shape(A)[0]   # Order of the matrix
    C_A = np.zeros([m,m])   # Initializing the cofactor matrix with zeros
    for i in range(1,m+1):
        for j in range(1,m+1):
            C_A[i-1,j-1] = pow(-1,i+j)*minor_of_element(A,i,j)
    return C_A

def number_of_spanning_trees(graph):
  adjacency_matrix = np.array(nx.to_numpy_matrix(G))
  adjacency_matrix_oposta = oposta(adjacency_matrix)
  degree_diag = diag_weight_matrix(G.number_of_nodes())
  aux_matrix = result_sum = matrix_sum(adjacency_matrix_oposta,degree_diag)
  cf = cofactor_matrix(aux_matrix)
  return cf[0][0]

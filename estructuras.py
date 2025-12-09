class ArbolBinario:
    def __init__(self, valor): # Inicializa un nodo del árbol binario
        self.valor = valor
        self.izquierda = None
        self.derecha = None

    def insertar(self, valor): # Inserta un valor en el árbol binario
        if valor < self.valor:
            if self.izquierda is None:
                self.izquierda = ArbolBinario(valor)
            else:
                self.izquierda.insertar(valor)
        else:
            if self.derecha is None:
                self.derecha = ArbolBinario(valor)
            else:
                self.derecha.insertar(valor)

    def buscar(self, valor): # Busca un valor en el árbol binario.
        if valor == self.valor:
            return True
        elif valor < self.valor:
            if self.izquierda is None:
                return False
            return self.izquierda.buscar(valor)
        else:
            if self.derecha is None:
                return False
            return self.derecha.buscar(valor)

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def traverse_linked_list(head): # Recorre una lista enlazada y devuelve una lista con los datos de cada nodo
    result = [] 
    currentNode = head
    while currentNode: # Recorre la lista enlazada y agrega los datos a la lista result
        result.append(currentNode.data) # Agrega el dato del nodo actual a la lista result
        currentNode = currentNode.next
    return result


def deleteSpecificNode(head, nodeToDelete): # Elimina un nodo específico de una lista enlazada
  if head == nodeToDelete:
    return head.next

  currentNode = head
  while currentNode.next and currentNode.next != nodeToDelete:
    currentNode = currentNode.next

  if currentNode.next is None:
    return head

  currentNode.next = currentNode.next.next

  return head

def insertNodeAtPosition(head, newNode, position): # Inserta un nodo en una posición específica de una lista enlazada
  if position == 1:
    newNode.next = head
    return newNode

  currentNode = head
  for _ in range(position - 2):
    if currentNode is None:
      break
    currentNode = currentNode.next

  newNode.next = currentNode.next
  currentNode.next = newNode
  return head

import math

########################################
#
# Name: Tyler Mertz
#
# Program uses Stack and Queue data structures to create an adjacency graph and allows user to perform breadth-first
# search and depth-first search on the graph.
#
########################################

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return "Node({})".format(self.value)

    __repr__ = __str__

#Queue class
class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def __str__(self):
        temp = self.head
        out = []
        while temp:
            out.append(str(temp.value))
            temp = temp.next
        out = ' '.join(out)
        return f'Head:{self.head}\nTail:{self.tail}\nQueue:{out}'

    __repr__ = __str__

    def isEmpty(self):
        return self.head == None

    def enqueue(self, x):
        newNode = Node(x)

        if self.isEmpty():
            self.head = newNode
            self.tail = newNode

        else:
            self.tail.next = newNode
            self.tail = newNode
        self.count += 1

    def dequeue(self):

        if self.isEmpty():
            self.tail = None
            return 'Queue is empty'

        else:
            dequeue_value = self.head.value
            self.head = self.head.next
            return dequeue_value

    def __len__(self):
        return self.count

    def reverse(self):

        if self.isEmpty():
            self.tail = None
            return 'Queue is empty'

        else:
            next = self.head.next
            prev = self.head
            prev.next = None

            while next:
                temp = next.next
                next.next = prev
                prev = next
                next = temp

                self.head, self.tail = self.tail, self.head

#Stack class
class Stack:
    def __init__(self):
        self.top = None
        self.count = 0

    def __str__(self):
        temp = self.top
        out = []
        while temp:
            out.append(str(temp.value))
            temp = temp.next
        out = '\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top, out))

    __repr__ = __str__

    def isEmpty(self):
        return self.top == None

    def __len__(self):
        count = 0
        temp = self.top

        while temp:
            count = count + 1
            temp = temp.next
        return count

    def push(self, value):
        newNode = Node(value)
        newNode.next = self.top
        self.top = newNode

    def pop(self):
        if self.top is None:
            return None
        else:
            temp = self.top.value
            self.top = self.top.next
            return temp

    def peek(self):
        return self.top.value

#-----Graph code-----
class Graph:
    def __init__(self, graph_repr):
        self.vertList = graph_repr

    #Uses starting vertex and returns order in which nodes are visited with respect to breadth
    def bfs(self, start):
        '''
            >>> g1 = {'A': ['B','D','G'],
            ... 'B': ['A','E','F'],
            ... 'C': ['F'],
            ... 'D': ['A','F'],
            ... 'E': ['B','G'],
            ... 'F': ['B','C','D'],
            ... 'G': ['A','E']}
            >>> g=Graph(g1)
            >>> g.bfs('A')
            ['A', 'B', 'D', 'G', 'E', 'F', 'C']
        '''
        visited = []
        q = Queue()
        q.enqueue(start)
        while not q.isEmpty():
            #dequeue vertex
            v = q.dequeue()

            #Appends vertex that are visited to list, finds vertex's neighbors, and sorts them
            if not(v in visited):
                visited.append(v)
                neighbor_list=[i[0] for i in self.vertList[v]]
                neighbor_list.sort()

                #Enqueues vertexs that are neighbors of v if they are not already visited
                for i in neighbor_list:
                        if not(i in visited):
                            q.enqueue(i)
        return visited

    def dfs(self, start):
        '''
            >>> g1 = {'A': ['B','D','G'],
            ... 'B': ['A','E','F'],
            ... 'C': ['F'],
            ... 'D': ['A','F'],
            ... 'E': ['B','G'],
            ... 'F': ['B','C','D'],
            ... 'G': ['A','E']}
            >>> g=Graph(g1)
            >>> g.dfs('A')
            ['A', 'B', 'E', 'G', 'F', 'C', 'D']
        '''
        visited = []
        s = Stack()
        s.push(start)
        while not s.isEmpty():
            v = s.pop()
            #if v is not visited yet add to list and sort its neighbors to be appended to list
            if not(v in visited):
                visited.append(v)
                neighbor_list = [i[0] for i in self.vertList[v]]

                neighbor_list.sort()
                neighbor_list = neighbor_list[::-1]

            #adjacent vertexes are added to list if not already visited
            for neighbor in neighbor_list:
                if not(neighbor in visited):
                    s.push(neighbor)
        return visited


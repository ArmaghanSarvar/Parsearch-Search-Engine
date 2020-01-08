import heapq


class Heap(object):   # Max Heap
    def __init__(self, initial=None, key=lambda x: x[1]):
        self.key = key
        if initial:
            self.data = [(key(item), item) for item in initial]
            heapq.heapify(self.data)
        else:
            self.data = []

    def push(self, item):
        heapq.heappush(self.data, (-self.key(item), item))

    def pop(self):
        if len(self.data) == 0:
            return None
        return heapq.heappop(self.data)[1]

    def clear(self):
        while self.pop() is not None:
            pass


heap = Heap()


def pushDocument(document, score):
    heap.push([document, score])


def popDocument():
    if len(heap.data) > 0:
        node = heap.pop()
        return node[0], node[1]
    return None


def clearHeap():
    heap.clear()

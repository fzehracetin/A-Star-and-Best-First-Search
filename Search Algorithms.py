from PIL import Image
from math import sqrt
import numpy as np
import time


class Point:
    x: float
    y: float
    f: float
    h: float
    g: float

    def __init__(self, x, y, f):
        self.x = x
        self.y = y
        self.f = f
        self.g = 0
        self.h = 0
        self.parent = None

    def equal(self, other):
        if self.x == other.x and self.y == other.y:
            return True


def distance(point, x, y):
    return sqrt((point.x - x)**2 + (point.y - y)**2)


def insert_in_heap(heap, top, point):

    heap.append(point)
    i = top
    parent = (i - 1)/2

    while i >= 1 and heap[int(i)].f < heap[int(parent)].f:
        heap[int(i)], heap[int(parent)] = heap[int(parent)], heap[int(i)]  # swap
        i = parent
        parent = (i - 1) / 2
    return


def calculate_weight(x, y, liste, top, point, visited, index1, index2):

    if visited[int(x)][int(y)] == 0:
        r, g, b = image.getpixel((x, y))
        if x == end.x and y == end.y:
            print("YES")
        if r is 0:
            r = 1

        new_point = Point(x, y, 0)
        new_point.parent = point
        new_point.h = distance(end, x, y) * (256 - r)

        if index1 == 1:  # a_star
            temp_point = new_point
            new_point.g = temp_point.parent.g + 256 - r

        new_point.f = new_point.h + new_point.g

        if index2 == 0:
            liste.append(new_point)
        else:  # heap
            insert_in_heap(liste, top, new_point)

        top += 1
        visited[int(x)][int(y)] = 1

    return top


def add_neighbours(point, liste, top, visited, index1, index2):

    if (point.x == width and point.y == height) or (point.x == 1 and point.y == 1) or \
            (point.x == 1 and point.y == height) or (point.x == width and point.y == 1):
        if point.x == width and point.y == height:
            constx = -1
            consty = -1
        elif point.x == 1 and point.y == 1:
            constx = 1
            consty = 1
        elif point.x == width and point.y == 1:
            constx = 1
            consty = -1
        else:
            constx = -1
            consty = 1
        top = calculate_weight(point.x + constx, point.y, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x, point.y + consty, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x + constx, point.y + consty, liste, top, point, visited, index1, index2)

    elif point.x == 1 or point.x == width:
        top = calculate_weight(point.x, point.y - 1, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x, point.y + 1, liste, top, point, visited, index1, index2)
        if point.x == 1:
            const = 1
        else:
            const = -1
        top = calculate_weight(point.x + const, point.y - 1, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x + const, point.y + 1, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x + const, point.y, liste, top, point, visited, index1, index2)

    elif point.y == 1 or point.y == height:
        top = calculate_weight(point.x - 1, point.y, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x + 1, point.y, liste, top, point, visited, index1, index2)
        if point.y == 1:
            const = 1
        else:
            const = -1
        top = calculate_weight(point.x - 1, point.y + const, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x + 1, point.y + const, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x, point.y + const, liste, top, point, visited, index1, index2)
    else:
        top = calculate_weight(point.x - 1, point.y, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x - 1, point.y - 1, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x - 1, point.y + 1, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x + 1, point.y - 1, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x + 1, point.y, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x + 1, point.y + 1, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x, point.y + 1, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x, point.y - 1, liste, top, point, visited, index1, index2)

    return top


def paint(point):
    yol = []
    while not point.equal(start):
        yol.append(point)
        image.putpixel((int(point.x), int(point.y)), (0, 0, 0))
        point = point.parent
    end_time = time.time()
    image.show()
    print("--------------YOL------------------")
    for i in range(len(yol)):
        print("x: {}, y:{}, distance:{}".format(yol[i].x, yol[i].y, yol[i].f))
    print("------------------------------------")
    print("--- %s seconds ---" % (end_time - start_time))


def bfs_and_a_star_with_stack(index):
    stack = []
    top = 0
    found = False
    point = None
    stack.append(start)
    visited = np.zeros((width, height))
    visited[int(start.x)][int(start.y)] = 1
    j = 0
    max_element = 0

    while stack and not found:
        point = stack.pop(top)
        # print("x: {}, y:{}, f:{}".format(point.x, point.y, point.f))
        top -= 1

        if point.equal(end):
            found = True
        else:
            top = add_neighbours(point, stack, top, visited, index, 0)
            stack.sort(key=lambda point: point.f, reverse=True)
            if len(stack) > max_element:
                max_element = len(stack)

            j += 1

    if found:
        paint(point)
        print("Stackten çekilen eleman sayısı: ", j)
        print("Stackteki maksimum eleman sayısı: ", max_element)
    return


def find_smallest_child(heap, i, top):
    if 2 * i + 2 < top:  # has two child
        if heap[2*i + 1].f < heap[2*i + 2].f:
            return 2*i + 1
        else:
            return 2*i + 2
    elif 2*i + 1 < top:  # has one child
        return 2*i + 1
    else:  # has no child
        return 0


def remove_min(heap, top):
    if top == 0:
        return None
    min_point = heap[0]
    top -= 1
    heap[0] = heap[top]
    del heap[top]
    i = 0
    index = find_smallest_child(heap, i, top)

    while index != 0 and heap[i].f > heap[index].f:
        heap[i], heap[index] = heap[index], heap[i]
        i = index
        index = find_smallest_child(heap, i, top)
    return min_point, top


def bfs_and_a_star_with_heap(index):
    heap = []
    found = False
    yol = []
    point = None
    heap.append(start)
    visited = np.zeros((width, height))
    visited[int(start.x)][int(start.y)] = 1
    j = 0
    top = 1
    max_element = 0

    while heap and not found:
        point, top = remove_min(heap, top)
        # print("x: {}, y:{}, f:{}".format(point.x, point.y, point.f))

        if point.equal(end):
            found = True
        else:
            top = add_neighbours(point, heap, top, visited, index, 1)
            if len(heap) > max_element:
                max_element = len(heap)
            j += 1

    if found:
        paint(point)
        print("Stackten çekilen eleman sayısı: ", j)
        print("Stackteki maksimum eleman sayısı: ", max_element)
    return


if __name__ == "__main__":
    start_time = time.time()
    image = Image.open("deneme1.png")
    width, height = image.size
    print("Width: {}, Height: {}".format(width, height))

    image = image.convert('RGB')

    start= Point(300, 150, -1)
    start.parent = -1
    end = Point(451, 353, -1)

    bfs_and_a_star_with_stack(1)
    # bfs_and_a_star_with_heap(1)

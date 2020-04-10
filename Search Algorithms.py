from PIL import Image
from math import sqrt
import numpy as np
import time
import matplotlib.backends.backend_tkagg
import matplotlib.pyplot as plt


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


class Output:
    result_image: Image
    total_time: float
    n_elements: int
    max_elements: int

    def __init__(self, result_image, total_time, n_elements, max_elements):
        self.result_image = result_image
        self.total_time = total_time
        self.n_elements = n_elements
        self.max_elements = max_elements
        self.name = None

    def plot_times(self, other1, other2, other3):
        fig, ax = plt.subplots()
        ax.bar([self.name, other1.name, other2.name, other3.name],
               [self.total_time, other1.total_time, other2.total_time, other3.total_time])
        fig.suptitle("Toplam Zamanlar")
        fname = image_name.split('.')
        plt.savefig(fname[0] + "times.png")
        plt.show()

    def plot_n_elements(self, other1, other2, other3):
        fig, ax = plt.subplots()
        ax.bar([self.name, other1.name, other2.name, other3.name],
               [self.n_elements, other1.n_elements, other2.n_elements, other3.n_elements])
        fig.suptitle("Stack'ten Çekilen Toplam Eleman Sayısı")
        fname = image_name.split('.')
        plt.savefig(fname[0] + "n_elements.png")
        plt.show()

    def plot_max_elements(self, other1, other2, other3):
        fig, ax = plt.subplots()
        ax.bar([self.name, other1.name, other2.name, other3.name],
               [self.max_elements, other1.max_elements, other2.max_elements, other3.max_elements])
        fig.suptitle("Stack'te Bulunan Maksimum Eleman Sayısı")
        fname = image_name.split('.')
        plt.savefig(fname[0] + "max_elements.png")
        plt.show()


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
            print("Path found.")
        if r is 0:
            r = 1

        new_point = Point(x, y, 0)
        new_point.parent = point
        new_point.h = distance(end, x, y) * (256 - r)
        new_point.g = 0

        if index1 == 1:  # a_star
            new_point.g = new_point.parent.g + 256 - r

        new_point.f = new_point.h + new_point.g # bfs'de g = 0

        if index2 == 0: # stack
            liste.append(new_point)
        else:  # heap
            insert_in_heap(liste, top, new_point)

        top += 1
        visited[int(x)][int(y)] = 1

    return top


def add_neighbours(point, liste, top, visited, index1, index2):
    # print(point.x, point.y)
    if (point.x == width - 1 and point.y == height - 1) or (point.x == 0 and point.y == 0) or \
            (point.x == 0 and point.y == height - 1) or (point.x == width - 1 and point.y == 0):
        # print("first if")
        if point.x == width - 1 and point.y == height - 1:
            constx = -1
            consty = -1
        elif point.x == 0 and point.y == 0:
            constx = 1
            consty = 1
        elif point.x == width - 1 and point.y == 0:
            constx = 1
            consty = -1
        else:
            constx = -1
            consty = 1
        top = calculate_weight(point.x + constx, point.y, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x, point.y + consty, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x + constx, point.y + consty, liste, top, point, visited, index1, index2)

    elif point.x == 0 or point.x == width - 1:
        # print("nd if")
        top = calculate_weight(point.x, point.y - 1, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x, point.y + 1, liste, top, point, visited, index1, index2)
        if point.x == 0:
            const = 1
        else:
            const = -1
        top = calculate_weight(point.x + const, point.y - 1, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x + const, point.y + 1, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x + const, point.y, liste, top, point, visited, index1, index2)

    elif point.y == 0 or point.y == height - 1:
        # print("3rd if")
        top = calculate_weight(point.x - 1, point.y, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x + 1, point.y, liste, top, point, visited, index1, index2)
        if point.y == 0:
            const = 1
        else:
            const = -1
        top = calculate_weight(point.x - 1, point.y + const, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x + 1, point.y + const, liste, top, point, visited, index1, index2)
        top = calculate_weight(point.x, point.y + const, liste, top, point, visited, index1, index2)
    else:
        # print("4th if")
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
        image.putpixel((int(point.x), int(point.y)), (60, 255, 0))
        point = point.parent
    end_time = time.time()
    # image.show()

    '''print("--------------YOL------------------")
    for i in range(len(yol)):
        print("x: {}, y:{}, distance:{}".format(yol[i].x, yol[i].y, yol[i].f))
    print("------------------------------------")'''

    return image, (end_time - start_time)


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
        result_image, total_time = paint(point)
        # print("Stackten çekilen eleman sayısı: ", j)
        # print("Stackteki maksimum eleman sayısı: ", max_element)
    return result_image, total_time, j, max_element


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
        result_image, total_time = paint(point)
    else:
        return

    return result_image, total_time, j, max_element


if __name__ == "__main__":


    print("UYARI: Seçilecek görüntü exe dosyası ile aynı klasörde olmalıdır.")
    image_name = input("Algoritmanın üzerinde çalışacağı görüntünün ismini giriniz (Örnek input: image.png): ")
    print(image_name)
    print("-------------------Algoritmalar------------------")
    print("1- Best First Search with Stack")
    print("2- Best First Search with Heap")
    print("3- A* with Stack")
    print("4- A* with Heap")
    print("5- Analiz (tüm algoritmaların çalışmalarını ve kıyaslamalarını gör)")
    alg = input("Algoritmayı ve veri yapısının numarasını seçiniz (Örnek input: 1): ")

    image = Image.open(image_name)
    width, height = image.size
    image = image.convert('RGB')

    print("Görüntünün genişliği: {}, yüksekliği: {}".format(width, height))
    print("NOT: Başlangıç ve bitiş noktasının koordinatları genişlik ve uzunluktan küçük olmalıdır.")

    sx, sy = input("Başlangıç noktasının x ve y piksel koordinatlarını sırasıyla giriniz (Örnek input: 350 100): ").split()
    ex, ey = input("Bitiş noktasının x ve y piksel koordinatlarını sırasıyla giriniz (Örnek input: 200 700): ").split()

    start = Point(int(sx), int(sy), -1)
    start.parent = -1
    end = Point(int(ex), int(ey), -1)

    start_time = time.time()

    if int(alg) == 1:
        result_image, total_time, n_elements, max_elements = bfs_and_a_star_with_stack(0)
    elif int(alg) == 2:
        result_image, total_time, n_elements, max_elements = bfs_and_a_star_with_heap(0)
    elif int(alg) == 3:
        result_image, total_time, n_elements, max_elements = bfs_and_a_star_with_stack(1)
    elif int(alg) == 4:
        result_image, total_time, n_elements, max_elements = bfs_and_a_star_with_heap(1)

    elif int(alg) == 5:
        result_image, total_time, n_elements, max_elements = bfs_and_a_star_with_stack(0)
        output1 = Output(result_image, total_time, n_elements, max_elements)
        print(n_elements, total_time, max_elements)
        output1.name = "BFS with Stack"
        print("1/4")

        image = Image.open(image_name)
        width, height = image.size
        image = image.convert('RGB')

        start_time = time.time()
        result_image, total_time, n_elements, max_elements = bfs_and_a_star_with_heap(0)
        output2 = Output(result_image, total_time, n_elements, max_elements)
        print(n_elements, total_time, max_elements)
        output2.name = "BFS with Heap"
        print("2/4")

        image = Image.open(image_name)
        width, height = image.size
        image = image.convert('RGB')

        start_time = time.time()
        result_image, total_time, n_elements, max_elements = bfs_and_a_star_with_stack(1)
        output3 = Output(result_image, total_time, n_elements, max_elements)
        output3.name = "A* with Stack"
        print(n_elements, total_time, max_elements)
        print("3/4")

        image = Image.open(image_name)
        width, height = image.size
        image = image.convert('RGB')

        start_time = time.time()
        result_image, total_time, n_elements, max_elements = bfs_and_a_star_with_heap(1)
        output4 = Output(result_image, total_time, n_elements, max_elements)
        output4.name = "A* with Heap"
        print("4/4")

        output1.plot_times(output2, output3, output4)
        output1.plot_max_elements(output2, output3, output4)
        output1.plot_n_elements(output2, output3, output4)

        print("Bastırılan görüntüler sırasıyla BFS stack, BFS heap, A* stack ve A* heap şeklindedir.")
        fname = image_name.split('.')
        output1.result_image.show()
        output1.result_image.save(fname[0] + "BFS_stack.png")
        output2.result_image.show()
        output2.result_image.save(fname[0] + "BFS_heap.png")
        output3.result_image.show()
        output3.result_image.save(fname[0] + "A_star_stack.png")
        output4.result_image.show()
        output4.result_image.save(fname[0] + "A_star_heap.png")
        exit(0)

    else:
        print("Algoritma numarası hatalı girildi, tekrar deneyin.")
        exit(0)

    print("Stackten çekilen eleman sayısı: ", n_elements)
    print("Stackteki maksimum eleman sayısı: ", max_elements)
    print("Toplam süre: ", total_time)
    result_image.show()




import collections
from itertools import chain, groupby

import numpy as np
from PIL import Image


def findDim(array, cp):
    a = array[cp[0]:, cp[1]:]
    b = np.array(np.where(a == [255, 255, 255, 225]))
    return (b[:2, 0])[1]
def bfs(grid, h, w, start):
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[x][y] == 3:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 <h  and 0 <= y2 < w and grid[x2][y2] != 1  and grid[x2][y2] != 4 and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

def bfs2(grid, h, w, start, goal):
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if x==goal[0] and y==goal[1]:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 <h  and 0 <= y2 < w and grid[x2][y2] != 1  and grid[x2][y2] != 4 and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

def udlr(shortest_path):
    path = []
    for c1 in range(0, len(shortest_path) - 1):
        if (shortest_path[c1 + 1][0] - shortest_path[c1][0] > 0):
            path.append('d')
        elif (shortest_path[c1 + 1][1] - shortest_path[c1][1] > 0):
            path.append('r')
        elif (shortest_path[c1 + 1][0] - shortest_path[c1][0] < 0):
            path.append('u')
        elif (shortest_path[c1 + 1][1] - shortest_path[c1][1] < 0):
            path.append('l')
    return path.copy()

if __name__ == "__main__":
    inputImagePath, C, Cmax = input().split(' ')
    C=int(C)
    Cmax = int(Cmax)
    print([C,Cmax])
    image = Image.open(inputImagePath)
    array = np.array(image)
    image.close()
    black_pixels = np.array(np.where(array == [0,0,0,225]))
    first_black_pixel = black_pixels[:2, 0]
    last_black_pixel = black_pixels[:2,-1]
    dim = findDim(array, first_black_pixel.copy())
    h = (last_black_pixel[0] - first_black_pixel[0])//dim
    w = (last_black_pixel[1] - first_black_pixel[1])//dim
    matrix = np.zeros((h,w), dtype=int)
    for x in range(0, h):
        for y in range(0, w):
            pixel_colors = array[(first_black_pixel[0] + dim//2 + x*dim), (first_black_pixel[1] + dim//2 + y*dim)]
            if pixel_colors[1] == 0:
                matrix[x][y] = 1
            elif pixel_colors[1] == 34:
                matrix[x][y] = 2
            elif pixel_colors[1] == 128:
                matrix[x][y] = 3
            elif pixel_colors[1] == 82:
                matrix[x][y] = 4
            elif pixel_colors[1] == 215:
                matrix[x][y] = 5
    print("Task 1")
    print([h,w])
    for e in matrix:
        print(np.array2string(e, separator=', '))

    roomba = np.where(matrix == 2)
    shortest_path = bfs(matrix, h,w, (int(roomba[0]), int(roomba[1])))
    path = udlr(shortest_path)
    print('Task 2')
    print(path)


    path_for_cleaning = []
    points = np.argwhere(matrix == 5)
    first_point = roomba
    while(points.shape[0]>1):
        distance = []
        for point in points:
            distance.append(len(bfs2(matrix, h, w, (int(first_point[0]), (int(first_point[1]))), ((int(point[0]), (int(point[1])))))))
        i = distance.index(min(distance))
        path_for_cleaning.append(bfs2(matrix, h, w, (int(first_point[0]), (int(first_point[1]))), (int(points[i][0]), (int(points[i][1])))))
        first_point = points[i]
        points = np.delete(points, i, 0)
    path_for_cleaning.append(bfs2(matrix, h, w, (int(first_point[0]), (int(first_point[1]))), (int(points[0][0]), (int(points[0][1])))))
    p = []
    for x in path_for_cleaning:
        p += udlr(x)
    print('Task 3')
    print(p)

    print('Task 4')
    path_for_cleaning = []
    points = np.argwhere(matrix == 5)
    first_point = roomba
    while (points.shape[0] > 1):
        distance = []
        for point in points:
            distance.append(len(
                bfs2(matrix, h, w, (int(first_point[0]), (int(first_point[1]))), ((int(point[0]), (int(point[1])))))))
        i = distance.index(min(distance))
        path_to_next_point = bfs2(matrix, h, w, (int(first_point[0]), (int(first_point[1]))), (int(points[i][0]), (int(points[i][1]))))
        path_to_charging = bfs(matrix, h, w, (int(first_point[0]), (int(first_point[1]))))
        if (len(path_to_next_point) + len(path_to_charging) > C):
            C = Cmax
            path_for_cleaning.append(path_to_charging)
            for k in points:
                if np.any(np.all(k == path_to_charging, axis=1)):
                    index = np.where(points[0]==k)
                    points = np.delete(points, index, 0)

                if len(points)==0:
                    continue
            first_point = (np.argwhere(matrix == 3))[0]
        else:
            path_for_cleaning.append(path_to_next_point)
            first_point = points[i]
            points = np.delete(points, i, 0)
            C-=1
    path_for_cleaning.append(
        bfs2(matrix, h, w, (int(first_point[0]), (int(first_point[1]))), (int(points[0][0]), (int(points[0][1])))))
    p = []
    for x in path_for_cleaning:
        p += udlr(x)
    print(p)

    print('Task 5')
    rep = 0
    path_for_cleaning = []
    points = []
    points5 = np.argwhere(matrix==5)
    points3 = np.argwhere(matrix==3)
    points0 = np.argwhere(matrix==0)
    for point in points5:
        points.append(point)
    for point in points3:
        points.append(point)
    for point in points0:
        points.append(point)
    first_point = roomba
    while (len(points) > 1):
        distance = []
        for point in points:
            distance.append(len(
                bfs2(matrix, h, w, (int(first_point[0]), (int(first_point[1]))), ((int(point[0]), (int(point[1])))))))
        i = distance.index(min(distance))
        path_for_cleaning.append(
            bfs2(matrix, h, w, (int(first_point[0]), (int(first_point[1]))), (int(points[i][0]), (int(points[i][1])))))
        first_point = points[i]
        points = np.delete(points, i, 0)
    path_for_cleaning.append(
        bfs2(matrix, h, w, (int(first_point[0]), (int(first_point[1]))), (int(points[0][0]), (int(points[0][1])))))
    p = []
    p.append(rep)
    for x in path_for_cleaning:
        p += udlr(x)
    path = list(chain.from_iterable(path_for_cleaning))
    path = [key for key, _group in groupby(path)]
    for x in range(len(path) - 1):
        for y in range(x+1, len(path)):
            if path[x]==path[y]:
                rep+=1
    p[0] = rep
    print(p)

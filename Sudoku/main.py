from PIL import Image
import numpy as np
import os

def findFirstBlack(array):
    return divmod(array.argmin(), array.shape[1])

def isBlank(im_a):
    if im_a.all()==True:
        return True
    return False

def findFirstWhite(array):
    return divmod(array.argmax(), array.shape[1])

def findFirstNextBlack(array, current_position):
    for i in range(current_position[0], len(array)):
        if current_position[1] == array.shape[1]:
            current_position[1] = 0
        for j in range(current_position[1], len(array[0])):
            if array[i][j]==0:
                return current_position.copy();
            current_position[1] += 1
        current_position[0] += 1
    return np.array([-1, -1])

def findFirstNextWhite(array, current_position):
    for i in range(current_position[0], len(array)):
        if current_position[1] == array.shape[1]:
            current_position[1] = 0
        for j in range(current_position[1], len(array[0])):
            if array[i][j]==1:
                return current_position.copy();
            current_position[1] += 1
        current_position[0] += 1
    return np.array([-1, -1])

def cropBeter(im):
    im_a = np.array(im)
    coordinates = findFirstBlack(im_a)
    filler = coordinates[0]
    size = im.size
    top = filler
    bottom = size[0] - filler
    left = filler
    right = size[1] - filler
    return im.crop((left, top, right, bottom))

def numberMatrix(path, im2):
    for i in range(1, 10, 1):
        name = str(i) + ".png"
        path_d = os.path.join(path, "digits", name)
        digit = Image.open(path_d)
        digit = digit.resize(im2.size)
        d_array = np.array(digit)
        digit.close()
        d = d_array[:, :, 3]
        d = d.astype(bool)
        if i == 1:
            nm = d
        else:
            nm = np.vstack((nm, d))
    return nm

def number(im2, nm):
    im2_a=np.array(im2)
    if isBlank(im2_a):
        return 0

    im2 = cropBeter(im2)
    im2_array = np.array(im2)
    sim = np.zeros(9)

    for i in range(1, 10, 1):
        similarity = 0
        for x in range(im2_array.shape[0]):
            for y in range(im2_array.shape[1]):
                if im2_array[x][y] != nm[(i-1)*nm.shape[0]//9 + x][y]:
                    similarity += 1
        sim[i - 1] = similarity
    return sim.argmax() + 1

def findNextCellToFill(grid, i, j):
    for x in range(i, 9):
        for y in range(j, 9):
            if grid[x][y] == 0:
                return x, y
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1

def solveSudoku(grid, i=0, j=0):
    i, j = findNextCellToFill(grid, i, j)
    if i == -1:
        return True
    for e in range(1, 10):
        if isValid(grid, i, j, e):
            grid[i][j] = e
            if solveSudoku(grid, i, j):
                return True
            grid[i][j] = 0
    return False

def isValid(grid, i, j, e):
    rowOk = all([e != grid[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(9)])
        if columnOk:
            secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
            for x in range(secTopX, secTopX + 3):
                for y in range(secTopY, secTopY + 3):
                    if grid[x][y] == e:
                        return False
            return True
    return False

def printSudoku(sudoku):
    for i in sudoku:
        for j in i:
            print(j, end=",")
        print('\b')


if __name__ == "__main__":
    path = input()
    name_of_png = path[-2:] + ".png"
    path_s = os.path.join(path, name_of_png)
    im = Image.open(path_s)
    im = im.convert('1')
    array = np.array(im)
    sudoku = np.zeros((9, 9), dtype=int)

    first_white = findFirstWhite(array)
    current_position = np.asarray(findFirstWhite(array))
    first_black = findFirstNextBlack(array, current_position)
    second_white = findFirstNextWhite(array, current_position)
    dimension_of_square = first_black[1] - first_white[1]
    small_line = second_white[1] - first_black[1]
    start_big_line = first_white[1] + 2 * small_line + 3 * dimension_of_square
    current_position[1] = start_big_line
    end_big_line = findFirstNextWhite(array, current_position)
    big_line = end_big_line[1] - start_big_line
    im2 = im.crop(
        (first_white[1], first_white[0], first_white[1] + dimension_of_square, first_white[0] + dimension_of_square))
    nm = numberMatrix(path, im2)
    im2.close()
    current_position[0] = first_white[0]
    current_position[1] = first_white[1]
    for x in range(0, 9, 1):
        for y in range(0, 9, 1):
            left = current_position[1]
            top = current_position[0]
            im2 = im.crop((left, top, left + dimension_of_square, top + dimension_of_square))
            sudoku[x][y] = number(im2, nm)
            im2.close()
            if (y == 2 or y == 5):
                current_position[1] += (big_line + dimension_of_square)
            else:
                current_position[1] += (small_line + dimension_of_square)
        current_position[1] = first_white[1]
        if (x == 2 or x == 5):
            current_position[0] += (big_line + dimension_of_square)
        else:
            current_position[0] += (small_line + dimension_of_square)


    printSudoku(sudoku)
    solveSudoku(sudoku)
    printSudoku(sudoku)
    im.close()
import copy
from typing import List

import numpy as np
import pyautogui
import time
import cv2
from PIL import Image

pyautogui.PAUSE = 0.001
time.sleep(3)


# while True:
#     try:
#         pix = pyautogui.pixel(pyautogui.position()[0], pyautogui.position()[1])
#     except:
#         pix = pyautogui.pixel(pyautogui.position()[0], pyautogui.position()[1])
#     print(pix)
# pyautogui.click(1300, 250)
# pyautogui.click(1300, 600)
# time.sleep(1.5)

def pp(list_of_elements):
    for x in list_of_elements:
        print(x)


def check_if_valid(position: List[int], number: int, list_of_elements: List[List[int]]):
    # pp(list_of_elements)
    # position: [x, y]
    # number: the number the check is on
    # list_of_elements: grid
    # check element in grid
    # get row
    if number in list_of_elements[position[0]][:position[1]] + list_of_elements[position[0]][position[1] + 1:]:
        return False
    # get column
    column = [list_of_elements[i][position[1]] for i in range(9)]
    column.pop(position[0])
    if number in column:
        return False
    # get sub-grid
    new_position = copy.copy(position)
    if new_position[1] < 2:
        new_position[1] = 2
    if new_position[0] < 2:
        new_position[0] = 2
    sub_grid_positions = [[new_position[1] - new_position[1] % 3, new_position[1] - new_position[1] % 3 + 3],
                          [new_position[0] - new_position[0] % 3, new_position[0] - new_position[0] % 3 + 3]]
    sub_grid = []
    for y in range(sub_grid_positions[0][0], sub_grid_positions[0][1]):
        for x in range(sub_grid_positions[1][0], sub_grid_positions[1][1]):
            if x == position[0] and y == position[1]:
                continue
            sub_grid.append(list_of_elements[x][y])
    if number in sub_grid:
        return False
    return True


def get_valid_numbers(grid):
    valid_numbers = [[[] for _ in range(9)] for _ in range(9)]
    for x, i in enumerate(grid):
        # for j in range(1, 10):
        #     if j in i:
        #         free_nums[j] -= 1
        for y, j in enumerate(i):
            if j != 0:
                continue
            for num in range(1, 10):
                if check_if_valid([x, y], num, grid):
                    valid_numbers[x][y].append(num)
    return valid_numbers


def brute_force(grid):
    for x in range(9):
        for y in range(9):
            if grid[x][y] == 0:
                for n in range(1, 10):
                    if check_if_valid([x, y], n, grid):
                        grid[x][y] = n
                        if brute_force(grid):
                            return grid
                        grid[x][y] = 0
                return

    return grid


start_all = time.time()
start_region_x = 680
start_region_y = 240
end_region_x = 1180
end_region_y = 740
size_of_cell = (end_region_x - start_region_x) // 9
im = pyautogui.screenshot(
    region=(start_region_x, start_region_y, end_region_x - start_region_x, end_region_y - start_region_y))
pixel_map = im.load()

img = Image.new(im.mode, im.size)
pixels_new = img.load()
for i in range(img.size[0]):
    for j in range(img.size[1]):
        # if pixel_map[i, j] == (52, 72, 97) or pixel_map[i, j] == (196, 203, 216):
        if pixel_map[i, j][0] < 220 and pixel_map[i, j][1] < 220 and pixel_map[i, j][2] < 220:
            pixel_map[i, j] = (0, 0, 0)
        else:
            pixels_new[i, j] = (255, 255, 255)  # pixel_map[i, j]
img.save('grid.png')
images = [cv2.imread(f'{i}.png') for i in range(1, 10)]
board = cv2.imread('grid.png')

method = cv2.TM_CCOEFF_NORMED
grid = [[0 for _ in range(9)] for _ in range(9)]

# pp(grid)
for i in range(9):
    result = cv2.matchTemplate(images[i], board, method)
    loc = np.where(result >= 0.9)
    last = (0, 0)
    for pt in zip(*loc[::-1]):
        if (pt[0], pt[1]) > (last[0] + 5, last[1] + 5) or (pt[0], pt[1]) < (last[0] - 5, last[1] - 5):
            # print(i+1, pt[0], pt[1], pt[1] // size_of_cell, pt[0] // size_of_cell)
            grid[pt[1] // size_of_cell][pt[0] // size_of_cell] = i + 1
            last = (pt[0], pt[1])
            # pyautogui.moveTo(pt[0] + 223, pt[1] + 373)
            # time.sleep(1)
# pp(grid)
copied_grid = copy.deepcopy(grid)
# valid_numbers = get_valid_numbers(grid)
# pp(valid_numbers)
start = time.time()
grid = brute_force(grid)
end = time.time()
print(end - start)
# pp(grid)
# print()
# pp(copied_grid)
pp(grid)
for pos_y, y in enumerate(grid):
    pyautogui.click(start_region_x + 25, pos_y * size_of_cell + start_region_y + 25)
    for pos_x, x in enumerate(y):
        if copied_grid[pos_y][pos_x] != 0:
            pyautogui.press('right')
            continue
        pyautogui.click(pos_x * size_of_cell + start_region_x + 25, pos_y * size_of_cell + start_region_y + 25)
        pyautogui.press(str(x))
        pyautogui.press('right')
        # for i in x:
        #     pyautogui.press(str(i))
        pyautogui.press('right')
# end_all = time.time()
# print(end_all - start_all)

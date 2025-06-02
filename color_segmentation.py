import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def show_matrix(matr: list[list[int]], title: str = None):
    plt.figure(figsize=(len(matr[0]), len(matr)))
    plt.pcolormesh(matr, edgecolors='black', cmap='gist_yarg')
    plt.gca().invert_yaxis()
    if title: plt.title(title)
    plt.show()

def print_matrix(matr: list[list[int]]):
    for row in matr:
        print()
        for n in row:
            print(round(n, 2), end='; ')
    print()

img = np.array(Image.open('segment_test.png').convert("RGB"))
image_width = len(img[0])
image_height = len(img)

visited = [[False for _ in range(image_width)] for _ in range(image_height)]

def color_diff(c1, c2):
    return sum(abs(a - b) for a, b in zip(c1, c2))

def get_neighbors(x, y):
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < image_width and 0 <= ny < image_height:
            yield nx, ny

def dfs(x, y, value, current_object, threshold=30):
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if visited[cy][cx]:
            continue
        visited[cy][cx] = True
        current_object.append((cx, cy))
        for nx, ny in get_neighbors(cx, cy):
            if not visited[ny][nx] and color_diff(img[ny][nx], value) < threshold:
                stack.append((nx, ny))

def extract_and_save_objects():
    objects = []
    for y in range(image_height):
        for x in range(image_width):
            if not visited[y][x]:
                value = img[y][x]
                current_object = []
                dfs(x, y, value, current_object)
                if len(current_object) > 1:
                    objects.append(current_object)

    for i, obj_coords in enumerate(objects):
        coords = np.array(obj_coords)
        xs = coords[:, 0]
        ys = coords[:, 1]

        x_min, x_max = xs.min(), xs.max()
        y_min, y_max = ys.min(), ys.max()

        obj_img = np.zeros((y_max - y_min + 1, x_max - x_min + 1, 3), dtype=np.uint8)

        for (x, y) in obj_coords:
            obj_img[y - y_min, x - x_min] = img[y, x]

        Image.fromarray(obj_img).save(f".\objects\object_{i}.png")

# Запуск
extract_and_save_objects()

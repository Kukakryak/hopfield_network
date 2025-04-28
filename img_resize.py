import matplotlib.pyplot as plt


def show_matrix(matr: list[list[int]], title: str = None):
    plt.figure(figsize=(len(matr[0]), len(matr)))
    plt.pcolormesh(matr, edgecolors='black', cmap='Oranges')
    plt.gca().invert_yaxis()
    if title: plt.title(title)
    plt.show()


def print_matrix(matr: list[list[int]]):
    for row in matr:
        print()
        for n in row:
            print(round(n, 2), end='; ')
    print()


def resize_matrix(matr: list[list[int]], new_scale: tuple):
    def upscale():
        x = int(j * scale_x)
        y = int(i * scale_y)
        new_matr[i][j] = matr[y][x]
    def downscale():
        x_start = int(j * scale_x)
        x_end = int((j + 1) * scale_x)
        y_start = int(i * scale_y)
        y_end = int((i + 1) * scale_y)
        cell = []
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                cell.append(matr[y][x])
        new_matr[i][j] = int(sum(cell) / len(cell))
    orig_x = len(matr[0])
    orig_y = len(matr)
    new_matr = [[0] * new_scale[1] for _ in range(new_scale[0])]
    scale_x = orig_x/new_scale[0]
    scale_y = orig_y/new_scale[1]
    oper = lambda: upscale() if (orig_x * orig_y) < (new_scale[0] * new_scale[1]) else downscale()
    for i in range(new_scale[1]):
        for j in range(new_scale[0]):
            oper()
    return new_matr

def tests():
    img = [
        [1, -1, -1, -1, -1, -1, -1, -1, 1],
        [-1, 1, -1, -1, -1, -1, -1, 1, -1],
        [-1, -1, 1, -1, -1, -1, 1, -1, -1],
        [-1, -1, -1, 1, -1, 1, -1, -1, -1],
        [-1, -1, -1, -1, 1, -1, -1, -1, -1],
        [-1, -1, -1, 1, -1, 1, -1, -1, -1],
        [-1, -1, 1, -1, -1, -1, 1, -1, -1],
        [-1, 1, -1, -1, -1, -1, -1, 1, -1],
        [1, -1, -1, -1, -1, -1, -1, -1, 1]
    ]

    img_2 = [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, 1, 1, 1, -1, -1, -1],
        [-1, -1, 1, 1, 1, 1, 1, -1, -1],
        [-1, -1, 1, 1, 1, 1, 1, -1, -1],
        [-1, -1, 1, 1, 1, 1, 1, -1, -1],
        [-1, -1, -1, 1, 1, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    ]
    big_x = [
        [1 if i == j or i == 19 - j else -1 for i in range(20)]
        for j in range(20)
    ]
    gradient_x = [
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
 [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
 [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
 [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0,10,10, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0,11,11, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0,12, 0, 0,12, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0,13, 0, 0, 0, 0,13, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0,14, 0, 0, 0, 0, 0, 0,14, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0,15, 0, 0, 0, 0, 0, 0, 0, 0,15, 0, 0, 0, 0, 0],
 [0, 0, 0, 0,16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,16, 0, 0, 0, 0],
 [0, 0, 0,17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,17, 0, 0, 0],
 [0, 0,18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,18, 0, 0],
 [0,19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,19, 0],
 [20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,20]
]

    resized = resize_matrix(matr=img, new_scale=(20,20))
    show_matrix(matr=img, title='Исходная матрица')
    show_matrix(matr=resized, title='Увеличенная матрица')
    reduced = resize_matrix(matr=gradient_x, new_scale=(10, 10))
    show_matrix(matr=gradient_x, title='Исходная матрица')
    show_matrix(matr=reduced, title='Уменьшенная матрица')


if __name__ == '__main__':
    tests()
import matplotlib.pyplot as plt


def show_matrix(matr: list[list[int]]):
    plt.figure(figsize=(len(matr[0]), len(matr)))
    plt.pcolormesh(matr, edgecolors='black', cmap='gist_yarg')
    plt.gca().invert_yaxis()
    plt.show()


def print_matrix(matr: list[list[int]]):
    for row in matr:
        print()
        for n in row:
            print(round(n, 2), end='; ')
    print()


def matrix_multiply(matrix: list[list[int]], scnd_matrix=None, vector=None):
    result = 0
    vector = matrix_to_vector(matrix)
    scnd_vector = matrix_to_vector(scnd_matrix)
    for x, y in zip(vector, scnd_vector):
        result += (x * y)
    return result / 9


def matrix_to_vector(matrix: list[list[int]]):
    vector = []
    for row in matrix:
        for num in row:
            vector.append(num)
    return vector


def matrix_sum(matrix: list[list[int]], scnd_matrix: list[list[int]]):
    result = []
    for row, scnd_row in zip(matrix, scnd_matrix):
        temp = []
        for x, y in zip(row, scnd_row):
            temp.append(x + y)
        result.append(temp)
    return result


def sum_layers(layers: list[list[list[int]]]):
    summary = layers[0]
    for matr in layers:
        if matr != summary:
            summary = matrix_sum(summary, matr)
    return summary


def convolution(a: list[list[int]], b: list[list[int]]):
    result = []
    for i in range(layer_length):
        s = []
        for j in range(layer_width):
            try:
                t = []
                # один цикл == один кусок матрицы
                for k in range(kernel_length):
                    t.append(a[i + k][j:j + kernel_length])
                s.append(matrix_multiply(matrix=t, scnd_matrix=b))
            except IndexError:
                break
        result.append(s)
    return result


# Итеративность поломана, так что больше одной итерации не сработает
def reduce_image_size(image: list[list[int]], kernels: list[list[list[int]]], iters: int = 1):
    global layer_length, layer_width
    for i in range(iters):
        layers = [convolution(image, kern) for kern in kernels]
        for j in range(kernels_amount):
            try:
                image = sum_layers(layers)
            except IndexError:
                layer_length = len(image)
                layer_width = len(image[0])
                break
    return image


def extract_object(image: list[list[int]]):
    def transposition(matr: list[list[int]]):
        result = []
        for i in range(len(matr[0])):
            temp = []
            for j in range(len(matr)):
                temp.append(matr[j][i])
            if sum(temp) != -len(temp):
                result.append(temp)
        return result
    return transposition(transposition(image))

image_length = 9
image_width = 9
kernel_length = 3
kernel_width = 3
kernels_amount = 3
layer_length = 7
layer_width = 7
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
    [-1, -1, 1,  1,  1,  1, 1, -1, -1],
    [-1, -1, 1,  1,  1,  1, 1, -1, -1],
    [-1, -1, 1,  1,  1,  1, 1, -1, -1],
    [-1, -1, -1, 1, 1, 1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1]
]

convolution_kernels = [
    [
        [1, -1, -1],
        [-1, 1, -1],
        [-1, -1, 1],
    ],
    [
        [1, -1, 1],
        [-1, 1, -1],
        [1, -1, 1],
    ],
    [
        [-1, -1, 1],
        [-1, 1, -1],
        [1, -1, -1],
    ]
]


def tests():
    pass
    # reduced = reduce_image_size(image=img, kernels=convolution_kernels)
    # show_matrix(img)
    # show_matrix(reduced)
    # show_matrix(img_2)
    # show_matrix(extract_object(img_2))


if __name__ == '__main__':
    tests()

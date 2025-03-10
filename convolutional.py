import matplotlib.pyplot as plt
import math

def show_matrix(matr: list[list[int]]):
    plt.figure(figsize=(len(matr), len(matr[0])))
    plt.pcolormesh(matr, edgecolors='black', cmap='gist_yarg')
    plt.show()

def print_matrix(matr: list[list[int]]):
    for row in matr:
        print()
        for n in row:
            print(round(n, 2), end='; ')
    print()

def matrix_multiply(matrix: list[list[int]], scnd_matrix = None, vector = None):
    result = 0
    vector = matrix_to_vector(matrix)
    v_iter = iter(vector)
    for i in range(len(scnd_matrix)):
        for j in range(len(scnd_matrix[i])):
            result += scnd_matrix[i][j]*next(v_iter)
    return result/9

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
        first_iter = iter(row)
        scnd_iter = iter(scnd_row)
        for x, y in zip(first_iter, scnd_iter):
            temp.append(x+y)
        result.append(temp)
    return result

def convolution(a: list[list[int]], b: list[list[int]]):
    result = []
    for j in range(layer_length):
        s = []
        for k in range(layer_length):
            try:
                t = []
                # один цикл == один кусок матрицы
                for i in range(kernel_length):
                    t.append(a[j+i][k:k+kernel_length])
                s.append(matrix_multiply(matrix=t, scnd_matrix=b))
            except IndexError:
                break
        result.append(s)
    return result



image_length = 9
image_width = 9
kernel_length = 3
kernel_width = 3
kernels_amount = 3
layer_length = 7
layer_width = 7
img = [[1, -1, -1, -1, -1, -1, -1, -1, 1],
         [-1, 1, -1, -1, -1, -1, -1, 1, -1],
         [-1, -1, 1, -1, -1, -1, 1, -1, -1],
         [-1, -1, -1, 1, -1, 1, -1, -1, -1],
         [-1, -1, -1, -1, 1, -1, -1, -1, -1],
         [-1, -1, -1, 1, -1, 1, -1, -1, -1],
         [-1, -1, 1, -1, -1, -1, 1, -1, -1],
         [-1, 1, -1, -1, -1, -1, -1, 1, -1],
         [1, -1, -1, -1, -1, -1, -1, -1, 1]]

convolution_kernels = [
[
    [1,-1,-1],
    [-1,1,-1],
    [-1,-1,1],
],
[
    [1,-1,1],
    [-1,1,-1],
    [1,-1,1],
],
[
    [-1,-1,1],
    [-1,1,-1],
    [1,-1,-1],
]
]
con1 = convolution(img, convolution_kernels[0])
con2 = convolution(img, convolution_kernels[1])
con3 = convolution(img, convolution_kernels[2])
convolution_layers = [con1, con2, con3]
con_sum = matrix_sum(con3, matrix_sum(con1, con2))
for con in convolution_layers:
    print_matrix(con)
print_matrix(con_sum)
show_matrix(img)
show_matrix(con_sum)
for j in con_sum:
    for k in range(len(j)):
        if j[k] > 1: j[k] = 1
        else: j[k] = -1
show_matrix(con_sum)
print_matrix(con_sum)
import time
from colorama import Back as back, Fore as fore, init

init(autoreset=True)

# Вывод матрицы в виде изображения (если на входе вектор, он преобразуется в матрицу)
def beautiful_print(vector=None, matrix=None, symbolic=False):
    # Вывод с использованием colorama
    def colored_print():
        match num:
            case 1:
                print(fore.LIGHTWHITE_EX + back.BLACK + ' ' + str(num), end=back.BLACK + ' ')
            case -1:
                print(fore.BLACK + back.LIGHTWHITE_EX + str(num), end=back.LIGHTWHITE_EX + ' ')
            case 0:
                print(back.WHITE + ' ' + str(num), end=back.WHITE + ' ')
            case _:
                symbol = ''
                if num >= 0: symbol = ' '
                print(back.YELLOW + symbol + str(num), end=back.YELLOW + ' ')
    # Вывод с использованием символов таблицы юникод
    def symbolic_print():
        match num:
            case 1:
                print('\u25A0', end=' ')
            case -1:
                print('\u25A1', end=' ')
            case 0:
                print('\u25A8', end=' ')
            case _:
                print('\u25A3', end=' ')

    if vector:
        matrix = vector_to_matrix(vector)
    for row in matrix:
        print()
        for num in row:
            if symbolic:
                symbolic_print()
            else:
                colored_print()
    print()

# Умножение векторов
def vector_multiply(vector: list[int], scnd_vector: list[int]):
    matrix = []
    for i in range(len(vector)):
        temp = []
        for k in range(len(scnd_vector)):
            temp.append(vector[i] * scnd_vector[k])
            if k == len(vector) - 1:
                matrix.append(temp)
    return matrix

# Сложение матриц
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

# Умножение матриц
def matrix_multiply(matrix: list[list[int]], scnd_matrix = None, vector = None):
    result = []
    if scnd_matrix:
        vector = matrix_to_vector(scnd_matrix)
    for row in matrix:
        v_iter = iter(vector)
        r_iter = iter(row)
        value = 0
        for x, y in zip(r_iter, v_iter):
            value += x * y
        result.append(value)
    return result

# Преобразование матрицы в вектор
def matrix_to_vector(matrix: list[list[int]]):
    vector = []
    for row in matrix:
        for num in row:
            vector.append(num)
    return vector

# Преобразование вектора в матрицу
def vector_to_matrix(vector: list[int]):
    matrix = []
    v_iter = iter(vector)
    vector_len = int(len(vector) ** 0.5)
    for i in range(vector_len):
        row = (next(v_iter) for _ in range(vector_len))
        matrix.append(row)
    return matrix

# Приведение матрицы к каноничному виду
def canonical_net(matrix: list[list[int]]):
    for i in range(0, len(matrix)): matrix[i][i] = 0
    return matrix

# Прыжковая функция
def sign_function(vector: list[int]):
    s_vector = []
    for num in vector:
        if num >= 0: s_vector.append(1)
        if num < 0: s_vector.append(-1)
    return s_vector


def tests():
    first_vector = [-1, 1, -1, 1]
    scnd_vector = [1, -1, 1, 1]
    third_vector = [-1, 1, -1, -1]
    corrupted_vector = [1, -1, 1, -1]
    first_matrix = vector_multiply(first_vector, first_vector)
    second_matrix = vector_multiply(scnd_vector, scnd_vector)
    third_matrix = vector_multiply(third_vector,third_vector)
    beautiful_print(matrix=first_matrix)
    beautiful_print(matrix=second_matrix)
    beautiful_print(matrix=third_matrix)
    first_sum = matrix_sum(matrix=first_matrix, scnd_matrix=second_matrix)
    second_sum = matrix_sum(matrix=first_sum, scnd_matrix=third_matrix)
    canonical_sum = canonical_net(second_sum)
    beautiful_print(matrix=canonical_sum)
    while True:
        multiplied = matrix_multiply(vector=corrupted_vector, matrix=canonical_sum)
        corrupted_vector = sign_function(multiplied)
        beautiful_print(vector=scnd_vector, symbolic=False)
        print()
        time.sleep(1)


if __name__ == "__main__":
    tests()

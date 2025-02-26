from math import e as euler
from tabulate import tabulate
from time import sleep, time
# Сигмоидная функция активации и её производная
sign_function = lambda x: 1 / (1 + pow(euler, -x))
sign_derivative = lambda x: x * (1 - x)

# Класс объектов-нейронов, у каждого нейрона есть номер, активность и весовой вектор
class Neuron:
    number: int
    activity: float
    weights: list[float]
    error: float = 0.0
    last_correction: list[float]

    def __init__(self, number: int, weights: list[float], value: float):
        self.number = number
        self.activity = value
        self.weights = weights
        self.last_correction = [0] * len(weights)

    def __str__(self):
        return f'Активность нейрона {self.number} = {self.activity}\nОшибка нейрона = {self.error}\n'

    @staticmethod
    def create_neuron(number: int, weights: list[float], value: float = 0.0):
        return Neuron(number, weights, value)


# Создание списка нейронов на основе весовой матрицы, каждый нейрон получает свой весовой вектор.
def neurons_by_weights(weight_matrix: list[list[float]]):
    neurons = []
    for i in range(len(weight_matrix)):
        neurons.append(Neuron.create_neuron(number=i + 1, weights=weight_matrix[i]))
    return neurons


# Приведение смежной матрицы к весовой, удаление двунаправленных связей между нейронами.
def adjacency_to_weight(matrix: list[list[float]]):
    for i in range(len(matrix)):
        for k in range(len(matrix[i])):
            if matrix[i][k] != 0: matrix[k][i] = 0
    return matrix


# Расчет активностей нейронов, возвращает список объектов Neuron, присвоив полученные активности нейронам
# input_neurons - список номеров входных нейронов
# output_neurons - список номеров выходных нейронов
def calculate_neurons_activities(neurons: list[Neuron], input_neurons: list[int], output_neurons: list[int]):
    for neuro_out in output_neurons:
        combined = 0
        outer = neurons[neuro_out - 1]
        for neuro_in in input_neurons:
            inner = neurons[neuro_in - 1]
            combined += inner.activity * inner.weights[neuro_out - 1]
        else:
            # print(f'Комбинированный ввод для нейрона {outer.number} =', rnd(combined))
            outer.activity = sign_function(combined)
    return neurons


# Расчет ошибок нейронов, возвращает список объектов Neuron, присвоив им полученные ошибки
def calculate_backpropagations(neurons: list[Neuron], output_neuron: int):
    global expected_output
    neurons[output_neuron - 1].error = ((expected_output - neurons[output_neuron - 1].activity) *
                                          sign_derivative(neurons[output_neuron - 1].activity))
    layer = [output_neuron - 1]
    next_layer = []
    for i in range(output_neuron - 2, 1, -1):
        output_weights = sum(map(lambda x: neurons[x].error * neurons[i].weights[x], layer))
        neurons[i].error = output_weights * sign_derivative(neurons[i].activity)
        next_layer.append(i)
        if neurons[i - 1].weights[layer[0]] == 0:
            layer = next_layer
            next_layer = []
    return neurons


def calculate_correction_values(neurons: list[Neuron]):
    global y
    for n in neurons:
        for i in range(len(n.weights)):
            if n.weights[i] != 0:
                correction = training_rate * neurons[i].error * n.activity + y * n.last_correction[i]
                n.weights[i] = n.weights[i] + correction
                n.last_correction.append(correction)
                # print(f'W[{n.number},{neurons[i].number}] = {correction}')
            else:
                if len(n.weights) != len(neurons):
                    n.last_correction.append(0.0)
    return neurons

# Входные данные
data_sensor = [0.6, 0.7]

# Ожидаемый выход сети
expected_output = 0.9

# Норма обучения
training_rate = 0.05

# Момент
y = 0.3

# Смежная матрица сети
adjacency_matrix = [[0, 0, -1, 2.5, 1, 0, 0, 0],
                    [0, 0, 1, 0.4, -1.5, 0, 0, 0],
                    [-1, 1, 0, 0, 0, 2.2, 0.34, 0],
                    [2.5, 0.4, 0, 0, 0, -1.4, 1.05, 0],
                    [1, -1.5, 0, 0, 0, 0.56, 3.1, 0],
                    [0, 0, 2.2, -1.4, 0.56, 0, 0, 0.75],
                    [0, 0, 0.34, 1.05, 3.1, 0, 0, -0.22],
                    [0, 0, 0, 0, 0, 0.75, -0.22, 0]]


def tests():
    # Формируем список нейронов на основе смежной матрицы сети
    weight_matrix = adjacency_to_weight(adjacency_matrix)
    neurons = neurons_by_weights(weight_matrix)

    # Присваиваем входным нейронам входные значения
    neurons[0].activity = data_sensor[0]
    neurons[1].activity = data_sensor[1]

    # Расчет активностей нейронов скрытых слоев
    first_hidden_layer = calculate_neurons_activities(neurons=neurons, input_neurons=[1, 2], output_neurons=[3, 4, 5])
    second_hidden_layer = calculate_neurons_activities(neurons=first_hidden_layer, input_neurons=[3, 4, 5],
                                                       output_neurons=[6, 7])

    # Расчет активности выходного нейрона сети
    output_neuron = calculate_neurons_activities(neurons=second_hidden_layer, input_neurons=[6, 7], output_neurons=[8])
    # for n in output_neuron:
    #     print(n)

    # Ошибки всех нейронов сети
    errors = calculate_backpropagations(neurons=neurons, output_neuron=8)
    for n in errors:
        print(n)

    corrected = calculate_correction_values(neurons=neurons)
    neurons = neurons_by_weights(weight_matrix)
    neurons[0].activity = data_sensor[0]
    neurons[1].activity = data_sensor[1]
    output = neurons[7]
    start_time = time()
    network_progress = 0
    iter_errors = []
    def iteration(nrns):
        nrns = calculate_neurons_activities(neurons=nrns, input_neurons=[1, 2],
                                            output_neurons=[3, 4, 5])
        nrns = calculate_neurons_activities(neurons=nrns, input_neurons=[3, 4, 5],
                                            output_neurons=[6, 7])
        nrns = calculate_neurons_activities(neurons=nrns, input_neurons=[6, 7],
                                            output_neurons=[8])
        nrns = calculate_backpropagations(neurons=nrns, output_neuron=8)
        nrns = calculate_correction_values(neurons=nrns)
        return nrns

    # Функция предназначена для остановки цикла обучения, если нейросеть остановилась на одном месте
    # и не пришла к ожидаемому выводу
    def compare_errors():
        if len(iter_errors) == 10:
            if len(set(iter_errors)) == 1:
                return True
            else:
                iter_errors.clear()
        else:
            iter_errors.append(neurons[6].error)
            return False

    learning_limit = float(input("Задайте лимит процента обучения нейросети (0 == без лимита): "))
    while not compare_errors():
        if (network_progress == learning_limit) & (learning_limit != 0): break
        neurons = iteration(neurons)
        network_progress = round(output.activity/expected_output*100,2)
        print(f'Выход сети: {output.activity}\tОшибка: {output.error}\t'
              f'Прогресс: {network_progress}%\tВремя обучения:{round(time()-start_time,2)}s\n')

    headers = []
    weight_matrix = []
    for n in neurons:
        headers.append(n.number)
        weight_matrix.append(n.weights)
    print(tabulate(weight_matrix, headers=headers, tablefmt='fancy_grid', showindex=headers))


if __name__ == '__main__':
    tests()

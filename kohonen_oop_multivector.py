from math import e as euler
from tabulate import tabulate
from time import sleep, time
from os import makedirs
import csv
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

    def __init__(self, number: int, weights: list[float], activity: float):
        self.number = number
        self.activity = activity
        self.weights = weights
        self.last_correction = [0] * len(weights)

    def __str__(self):
        return (f'number: {self.number}; activity: {self.activity}; weights: {self.weights}; '
                f'error: {self.error}; last_correction: {self.last_correction}')

    def generate_dict(self):
        ndict = {'number': self.number,
                'activity': self.activity,
                'weights': self.weights,
                'error': self.error,
                'last_correction': self.last_correction}
        return ndict
    @staticmethod
    def create_neuron(number: int, weights: list[float], activity: float = 0.0):
        return Neuron(number, weights, activity)

    @staticmethod
    def create_neuron_by_dict(n_dict: dict):
        weights = [float(n.replace(']', '').replace('[', '')) for n in n_dict.get('weights').split(',')]
        last_correction = [float(n.replace(']', '').replace('[', '')) for n in n_dict.get('last_correction').split(',')]
        n = Neuron(number=int(n_dict.get('number')), activity=float(n_dict.get('activity')),
                      weights=weights)
        n.error = float(n_dict.get('error'))
        n.last_correction = last_correction
        return n

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
            outer.activity = sign_function(combined)
    return neurons


# Расчет ошибок нейронов, возвращает список объектов Neuron, присвоив им полученные ошибки
def calculate_backpropagations(neurons: list[Neuron], output_neuron: int, expected: float):
    neurons[output_neuron - 1].error = ((expected - neurons[output_neuron - 1].activity) *
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
                n.last_correction[i] = correction
            else:
                if len(n.weights) != len(neurons):
                    n.last_correction.append(0.0)
    return neurons

class NeuroDialect(csv.Dialect):
    delimiter = ";"
    escapechar = '\\'
    doublequote = False
    skipinitialspace = True
    lineterminator = '\n'
    quoting = csv.QUOTE_NONE

# Сохранение нейронной сети в виде файла .csv
def save_trained_network(nrns: list[Neuron], filename: str = 'trained_network.csv'):
    with open(file=filename, mode='w') as file:
        fields = nrns[0].generate_dict().keys()
        w = csv.DictWriter(f=file, fieldnames=fields, dialect=NeuroDialect())
        w.writeheader()
        for neuro in nrns:
            w.writerow(neuro.generate_dict())
    file.close()

# Сохранение каждого вектора мультивекторной сети в виде файлов .csv
def save_multivector_network(network: list[list[Neuron]]):
    makedirs('./multivector', exist_ok=True)
    with open(file='./multivector/vectors', mode='w') as file:
        for i in range(len(network)):
            filename = f'trained_vector{i}.csv'
            save_trained_network(network[i], filename=f'./multivector/{filename}')
            file.writelines(filename+'\n')
    file.close()

# Загрузка мультивекторной сети из файлов
def file_based_multivector_network():
    networks = []
    with open(file='./multivector/vectors', mode='r') as file:
        files = file.readlines()
        file.close()
    for f in files:
        networks.append(file_based_network(f'./multivector/{f.rstrip()}'))
    return networks

# Загрузка нейронной сети из файла
def file_based_network(filename: str = 'trained_network.csv'):
    neurons = []
    with open(file=filename, mode='r', encoding='1251') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            neurons.append(Neuron.create_neuron_by_dict(row))
    return neurons

# Входные данные
data_sensor = [
  [0.11, 0.32],
  [0.68, 0.89],
  [0.03, 0.44],
  [0.69, 0.70],
  [0.32, 0.05],
  [0.89, 0.50],
  [0.43, 0.32],
  [0.60, 0.55]
]


# Ожидаемый выход сети
expected_output = [0.2, 0.7, 0.2, 0.7, 0.2, 0.7, 0.2, 0.7]

outputs_amount = 8
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
    weight_matrix = adjacency_to_weight(adjacency_matrix)
    networks_list = []
    for i in range(len(data_sensor)):
        neurons = neurons_by_weights(weight_matrix)
        neurons[0].activity = data_sensor[i][0]
        neurons[1].activity = data_sensor[i][1]
        networks_list.append(neurons)
    if int(input("Загрузить сохраненную сеть? (1 или 0): ")) == 1:
        try:
            networks_list = file_based_multivector_network()
        except FileNotFoundError:
            print("Ошибка! Файл с данными нейронной сети отсутствует. Составляем на основе весовой матрицы...")
    network_progress = 0.0
    errors = 0
    def iteration(nrns: list[Neuron], num: int):
        nrns = calculate_neurons_activities(neurons=nrns, input_neurons=[1, 2],
                                            output_neurons=[3, 4, 5])
        nrns = calculate_neurons_activities(neurons=nrns, input_neurons=[3, 4, 5],
                                            output_neurons=[6, 7])
        nrns = calculate_neurons_activities(neurons=nrns, input_neurons=[6, 7],
                                            output_neurons=[8])
        nrns = calculate_backpropagations(neurons=nrns, output_neuron=8, expected=expected_output[num])
        nrns = calculate_correction_values(neurons=nrns)
        return nrns

    comp_errors = []
    def compare_errors():
        if len(comp_errors) == 10:
            if len(set(comp_errors)) == 1:
                print('!!! Остановка обучения, сеть остановилась на одном месте !!!')
                return True
            else:
                comp_errors.clear()
        else:
            comp_errors.append(errors)
            return False
    learning_limit = int(input("Задайте лимит количества эпох нейросети (0 == без лимита): "))
    start_time = time()
    epochs = 0
    while not compare_errors():
        if (epochs == learning_limit) & (learning_limit != 0): break
        activities = [n[7].activity for n in networks_list]
        errors = sum([n[7].error for n in networks_list])/len(networks_list)
        epochs+=1
        for i in range(len(networks_list)):
            networks_list[i] = iteration(networks_list[i],i)
            network_progress = round(sum([activities[n]/expected_output[n]*100
                                    for n in range(len(networks_list))])/len(networks_list), 2)
        print(f'Эпоха: {epochs}\tОшибка: {errors}\tПрогресс: {network_progress}%'
              f'\tВремя обучения:{round(time()-start_time,2)}s\n')

    if int(input("Сохранить сеть последней эпохи? (1 или 0): ")) == 1:
        save_multivector_network(networks_list)
    print('Активности векторов сети: ')
    print([n[7].activity for n in networks_list])
    # for net in networks_list:
    #     headers = []
    #     weight_matrix = []
    #     for n in net:
    #         headers.append(n.number)
    #         weight_matrix.append(n.weights)
    #     print(f'||| Вывод вектора сети: {net[7].activity} |||')
    #     print(tabulate(weight_matrix, headers=headers, tablefmt='fancy_grid', showindex=headers), end='\n')

if __name__ == '__main__':
    tests()

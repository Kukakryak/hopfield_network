from math import e as euler
# Входные данные
data_sensor = [0.6, 0.7]

# Ожидаемый выход сети
expected_output = 0.9

# Норма обучения
training_rate = 0.3

# Момент
y = 0.3

# Элемент смещения
bias1 = 1
bias2 = 1

# Сигмоидная функция активации
sign_function = lambda x: 1 / (1 + pow(euler, -x))

# Весовые коэффициенты от входного слоя к первому скрытому слою ( номер столбца - номер входного нейрона, номер строки - номер скрытого нейрона )
input_weights1 = [
  [-1,   1 ],
  [2.5, 0.4],
  [ 1, -1.5]
]

# Весовые коэффициенты от первого скрытого слоя ко второму скрытому слою
input_weights2 = [
    [2.2, -1.4,  0.56],
    [0.34, 1.05, 3.10]
]

# Весовые коэффициенты от второго скрытого слоя к выходному
output_weights = [[0.75, -0.22]]

# Комбинированные вводы для нейронов первого скрытого слоя
hidden_combined1 = [data_sensor[0] * input_weights1[0][0] + data_sensor[1] * input_weights1[0][1],
                    data_sensor[0] * input_weights1[1][0] + data_sensor[1] * input_weights1[1][1],
                    data_sensor[0] * input_weights1[2][0] + data_sensor[1] * input_weights1[2][1]]
hidden_combined1 = list(map(lambda x: round(x, 5) , hidden_combined1))
print("Комбинированные вводы для нейронов первого скрытого слоя:", hidden_combined1)

# Активности нейронов первого скрытого слоя
activity_neuron1 = list(map(lambda x: round(sign_function(x), 5), hidden_combined1))
print("Активности нейронов первого скрытого слоя:", activity_neuron1)

# Комбинированные вводы для нейронов второго скрытого слоя
hidden_combined2 = [activity_neuron1[0] * input_weights2[0][0] +
                    activity_neuron1[1] * input_weights2[0][1] +
                    activity_neuron1[2] * input_weights2[0][2],

                    activity_neuron1[0] * input_weights2[1][0] +
                    activity_neuron1[1] * input_weights2[1][1] +
                    activity_neuron1[2] * input_weights2[1][2]  ]
hidden_combined2 = list(map(lambda x: round(x, 5) , hidden_combined2))
print("Комбинированные вводы для нейронов второго скрытого слоя:", hidden_combined2)

# Активности нейронов второго скрытого слоя
activity_neuron2 = list(map(lambda x: round(sign_function(x), 5), hidden_combined2))
print("Активности нейронов второго скрытого слоя:", activity_neuron2)

# Комбинированный ввод выходного нейрона
output_combined = round(activity_neuron2[0] * output_weights[0][0] + activity_neuron2[1] * output_weights[0][1], 5)
print("Комбинированный ввод выходного нейрона:", output_combined)

# Активность выходного нейрона
activity_output_neuron = round(sign_function(output_combined), 5)
print("Активность выходного нейрона:", activity_output_neuron)
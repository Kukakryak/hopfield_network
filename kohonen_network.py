# Входные данные
data_sensor = [0, 0]

# Элемент смещения
bias1 = 1
bias2 = 1

# Функция активации (прыжковая)
def sign_function(neuron: float):
    if neuron > 0.0: neuron = 1.0
    if neuron < 0.0: neuron = 0.0
    return neuron

# Весовые коэффициенты от входного слоя к первому скрытому слою ( номер столбца - номер входного нейрона, номер строки - номер скрытого нейрона )
input_weights = [
  [  -1,  -1,  1.5 ],
  [  -1,  -1,  0.5 ]
]

# Весовые коэффициенты от первого скрытого слоя к выходному
output_weights = [[1, -1, -0.5]]

# Комбинированные вводы для скрытых нейронов
f_combined = data_sensor[0] * input_weights[0][0] + data_sensor[0] * input_weights[1][0] + input_weights[0][2]
s_combined = data_sensor[1] * input_weights[1][1] + data_sensor[1] * input_weights[0][1] + input_weights[1][2]
hidden_combined = [f_combined, s_combined]
print(f'Комбинированные вводы для скрытых нейронов: {hidden_combined}')

# Активности нейронов скрытого слоя
activity_neuron = [sign_function(f_combined), sign_function(s_combined)]
print(f'Активности нейронов скрытого слоя: {activity_neuron}')

# Комбинированный ввод выходного нейрона
output_combined = activity_neuron[0] * output_weights[0][0] + activity_neuron[1] * output_weights[0][1] + output_weights[0][2]
print(f'Комбинированный ввод входного нейрона: {output_combined}')

# Активность выходного нейрона
activity_output_neuron = sign_function(output_combined)
print(f'Активность выходного нейрона: {activity_output_neuron}')

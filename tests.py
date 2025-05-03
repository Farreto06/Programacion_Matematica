import numpy as np
from scipy.optimize import linear_sum_assignment

cost_matrix = np.array([
    [4, 2, 8],
    [2, 3, 7],
    [3, 6, 9]
])

row_ind, col_ind = linear_sum_assignment(cost_matrix)

print("Índices de filas:", row_ind)
print("Índices de columnas:", col_ind)

# Mostrar las asignaciones óptimas
assignments = list(zip(row_ind, col_ind))
print("Asignaciones óptimas:", assignments)

# Calcular el costo total mínimo
total_cost = cost_matrix[row_ind, col_ind].sum()
print("Costo total mínimo:", total_cost)
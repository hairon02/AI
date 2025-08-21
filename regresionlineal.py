import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([[-1], [0], [1], [2], [3], [4]])
# y = 1 * x_0 + 2 * x_1 + 3
y = np.array([[-3], [-1], [1], [3], [5], [7]])
reg = LinearRegression().fit(X, y)
reg.score(X, y)
reg.coef_ # -1
reg.intercept_

print(LinearRegression().fit(X, y))
print("\n\n")
print(reg.coef_)
print(reg.intercept_)

print(reg.predict(np.array([[7], [9], [11], [14]])))


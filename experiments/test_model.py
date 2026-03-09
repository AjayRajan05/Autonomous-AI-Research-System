from sklearn.linear_model import LinearRegression
import numpy as np

X = np.random.rand(100,1)
y = 2*X + 1

model = LinearRegression()
model.fit(X,y)

print("Model trained")
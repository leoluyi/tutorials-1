# View more python tutorials on my Youtube and Youku channel!!!

# Youtube video tutorial: https://www.youtube.com/channel/UCdyjiB5H8Pu7aDTNVXTTpcg
# Youku video tutorial: http://i.youku.com/pythontutorial

# 12 - regularization
"""
Please note, this code is only for python 3+. If you are using python 2+, please modify the code accordingly.
"""
import theano
from sklearn.datasets import load_boston
import theano.tensor as T
import numpy as np


class Layer(object):
    def __init__(self, inputs, in_size, out_size, activation_function=None):
        self.W = theano.shared(np.random.normal(0, 1, (in_size, out_size)))
        self.b = theano.shared(np.zeros((out_size, )) + 0.1)
        self.Wx_plus_b = T.dot(inputs, self.W) + self.b
        self.activation_function = activation_function
        if activation_function is None:
            self.outputs = self.Wx_plus_b
        else:
            self.outputs = self.activation_function(self.Wx_plus_b)


def minmax_normalization(data):
    xs_max = np.max(data, axis=0)
    xs_min = np.min(data, axis=0)
    xs = (1 - 0) * (data - xs_min) / (xs_max - xs_min) + 0
    return xs

np.random.seed(100)
x_data = load_boston().data
# minmax normalization, rescale the inputs
x_data = minmax_normalization(x_data)
y_data = load_boston().target[:, np.newaxis]

# cross validation, train test data split
x_train, y_train = x_data[:400], y_data[:400]
x_test, y_test = x_data[400:], y_data[400:]

x = T.dmatrix("x")
y = T.dmatrix("y")

l1 = Layer(x, 13, 50, T.tanh)
l2 = Layer(l1.outputs, 50, 1, None)

# the way to compute cost
cost = T.mean(T.square(l2.outputs - y))

gW1, gb1, gW2, gb2 = T.grad(cost, [l1.W, l1.b, l2.W, l2.b])

learning_rate = 0.01
train = theano.function(
    inputs=[x, y],
    updates=[(l1.W, l1.W - learning_rate * gW1),
             (l1.b, l1.b - learning_rate * gb1),
             (l2.W, l2.W - learning_rate * gW2),
             (l2.b, l2.b - learning_rate * gb2)])

compute_cost = theano.function(inputs=[x, y], outputs=cost)

# record cost

for i in range(1000):
    train(x_train, y_train)
    if i % 10 == 0:
        # record cost
        pass

# plot cost history

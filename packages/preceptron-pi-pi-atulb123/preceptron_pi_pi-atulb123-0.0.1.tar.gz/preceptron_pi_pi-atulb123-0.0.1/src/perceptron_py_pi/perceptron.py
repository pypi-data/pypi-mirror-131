import os.path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import joblib  # FOR SAVING MY MODEL AS A BINARY FILE
from matplotlib.colors import ListedColormap
import logging

class Model:
    def __init__(self, eta, ephocs):
        np.random.seed(42)
        self.eta = eta
        self.ephocs = ephocs
        self.weights = np.random.randn(3) * 1e-4

    def activation_function(self, x):
        return np.where(np.dot(x, self.weights) > 0, 1, 0)

    def fit(self, x, y):
        self.x = x
        self.y = y
        x_with_bias = np.c_[self.x, -np.ones((len(self.x), 1))]
        for i in range(self.ephocs):
            logging.info(f"old weights are: {self.weights}")
            y_pred = self.activation_function(x_with_bias)
            logging.info(f"y_pred is :{y_pred}")
            self.error = self.y - y_pred
            logging.info(f"error magnitude is :{np.abs(self.error).sum()}")
            self.weights = self.weights + self.eta * np.dot(x_with_bias.T, self.error)
            logging.info(f"new weights are: {self.weights}")
            logging.info("#" * 15)

    def predict(self, x):
        return self.activation_function(np.c_[x, -np.ones((len(x), 1))])

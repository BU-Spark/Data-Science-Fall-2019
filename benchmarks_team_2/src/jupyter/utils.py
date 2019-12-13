import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from collections import Counter
from sklearn.model_selection import train_test_split


def class_wise_acc(y_true,y_pred):
    c = confusion_matrix(y_true, y_pred)
    d = Counter(y_true)
    acc={}
    for i in range(len(c)):
        acc[i]=(c[i][i]/d[i])
    return acc
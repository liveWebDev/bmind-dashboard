import numpy as np


def ConvertVectorSetToVecAverageBased(vectorSet, ignore=[]):
    if len(ignore) == 0:
        return np.mean(vectorSet, axis=0)
    else:
        return np.dot(np.transpose(vectorSet), ignore) / sum(ignore)

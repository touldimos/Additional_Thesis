import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def Modality(P):
    f0 = np.zeros(len(P))
    for i in range(len(P) - 1):
        f0[i] = (P[i - 1] - P[i]) * (P[i] - P[i + 1])
        f0[0] = (P[-1] - P[0]) * (P[0] - P[1])
        f0[-1] = (P[-2] - P[-1]) * (P[-1] - P[0])
    
    def zero_runs(a):
        # Create an array that is 1 where a is 0, and pad each end with an extra 0.
        iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
        absdiff = np.abs(np.diff(iszero))
        # Runs start and end where absdiff is 1.
        ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
        return ranges
    
    f_df = pd.DataFrame(f0, columns = ['f'])

    def classify(x):
        cl = np.zeros(len(x))
        for i in range(len(x)):
            if x[i] == 0:
                cl[i] = 0
            elif x[i] > 0:
                cl[i] = 1
            else:
                cl[i] = -1
        return cl
    
    f_df =  f_df.apply(classify)
    zeros = zero_runs(f_df['f'])
    if len(zeros) > 0:
        if zeros[-1][1] == 12 and zeros[0][0] == 0:
            zeros = np.insert(zeros, 0, [zeros[-1][0], zeros[0][1]], 0)
            zeros = np.delete(zeros, 1, 0)
            zeros = np.delete(zeros, -1, 0)
    f_df['P'] = P

    mod = np.zeros(len(P))  
    for i in range(len(P)):
        if f_df['f'].iloc[i] < 0 and f_df['P'].iloc[i - 1] < f_df['P'].iloc[i]:
            mod[i] = 1
    for i in range(len(zeros) - 1):
        if P[zeros[i][0] - 1] < P[zeros[i][0]] and P[zeros[i][0] + int(np.diff(zeros[i]))] < P[zeros[i][0]]:
            mod[zeros[i][0]] = 1
    for i in range(len(zeros)):
        if zeros[-1][1] == 12:
            if P[zeros[i][0] - 1] < P[zeros[i][0]] and P[0] < P[zeros[i][0]]:
                mod[zeros[i][0]] = 1
    for i in range(len(zeros)):
        zeros[i][0] = zeros[i][0] + 1

    f_df['modality'] = mod
    peak = []
    def peaks(f_df):
        for i in range(12):
            if f_df.iloc[i]['modality'] == 1:
                peak.append(i + 1)
        return peak
    
    peaks = np.array(peaks(f_df), dtype=np.int64)
    return mod, zeros, peaks
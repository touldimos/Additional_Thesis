import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

P = [50, 60, 35, 10, 45, 45, 20, 30, 50, 24, 60, 60]


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
for i in range(len(zeros)):
    if zeros[-1][1] == 12:
        if P[zeros[i][0] - 1] < P[zeros[i][0]] and P[0] < P[zeros[i][0]]:
            mod[zeros[i][0]] = 1
    elif P[zeros[i][0] - 1] < P[zeros[i][0]] and P[zeros[i][0] + int(np.diff(zeros[i]))] < P[zeros[i][0]]:
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
plt.plot(P)
plt.grid()
# def find_sq(a):
#     idx = [i for i, v in enumerate(a) if not i or a[i-1] != v] + [len(a)]
#     ranges = [r for r in zip(idx, (idx[1:])) if r[1] >= r[0] + 2]
#     ranges = pd.DataFrame(ranges)
#     ranges = np.asarray(ranges)
#     return ranges

# zero = find_sq(P)
# for i in range(len(zero)):
#     zero[i][0] = zero[i][0] + 1
#     if zero[i][0] == 13:
#         zero[i][0] = 1
#     if P[11] == P[0]:
#         zeros = np.insert(zero, len(zero), [12, 1], axis = 0)


# =============================================================================
# f0 = np.zeros(len(P))
# for i in range(len(P) - 1):
#     f0[i] = (P[i - 1] - P[i]) * (P[i] - P[i + 1])
#     f0[0] = (P[-1] - P[0]) * (P[0] - P[1])
#     f0[-1] = (P[-2] - P[-1]) * (P[-1] - P[0])
# 
# def zero_runs(a):
#     # Create an array that is 1 where a is 0, and pad each end with an extra 0.
#     iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
#     absdiff = np.abs(np.diff(iszero))
#     # Runs start and end where absdiff is 1.
#     ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
#     return ranges
# 
# f_df = pd.DataFrame(f0, columns = ['f'])
# 
# def classify(x):
#     cl = np.zeros(len(x))
#     for i in range(len(x)):
#         if x[i] == 0:
#             cl[i] = 0
#         elif x[i] > 0:
#             cl[i] = 1
#         elif x[i] < 0:
#             cl[i] = -1
#     return cl
# 
# f_df =  f_df.apply(classify)
# zeros = zero_runs(f_df['f'])
# for i in range(len(zeros)):
#     zeros[i][0] = zeros[i][0] + 1
# 
# if zeros[-1][1] == 12 and zeros[0][0] == 1:
#     zeros = np.insert(zeros, -2, [zeros[-1][0], zeros[0][0]], 0)
#     zeros = np.delete(zeros, 0, 0)
#     zeros = np.delete(zeros, -1, 0)
# 
# f_df['P'] = P
# 
# mod = np.zeros(len(P))  
# for i in range(len(P)):
#     if f_df['f'].iloc[i] < 0 and f_df['P'].iloc[i - 1] < f_df['P'].iloc[i]:
#         mod[i] = 1
# 
# f_df['modality'] = mod
# peak = []
# def peaks(f_df):
#     for i in range(12):
#         if f_df.iloc[i]['modality'] == 1:
#             peak.append(i + 1)
#     return peak
# 
# peaks = np.array(peaks(f_df), dtype=np.int64)
# 
# plt.plot(P)
# =============================================================================

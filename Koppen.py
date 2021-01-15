import pandas as pd
import numpy as np

def koppen(P, T, lat, z = 0, Peel = True):
    
    data = pd.DataFrame(data = (P, T), index = ['P', 'T']).transpose()
    
    T = np.array(T)
    P = np.array(P)
    
    MAP = np.round(np.sum(P), 4)
    MAT = np.round(np.mean(T), 4)
    Thot = np.round(np.max(T), 4)
    Tcold = np.round(np.min(T), 4)
    Tmonth10 = np.round(sum(map(lambda x : x >= 10, T)), 4)
    Pdry = np.round(np.min(P), 4)
    
    if not Peel:
        seqT = np.array((T[0], T[1], T[2], T[3], T[4], T[5], T[6], T[7], T[8], T[9], T[10], T[11], T[0], T[1], T[2], T[3], T[4]))
        seqP = np.array((P[0], P[1], P[2], P[3], P[4], P[5], P[6], P[7], P[8], P[9], P[10], P[11], P[0], P[1], P[2], P[3], P[4]))
        data['seqT'] = np.convolve(seqT, np.ones(6, dtype=np.int), mode='valid')
        data['seqP'] = np.convolve(seqP, np.ones(6, dtype=np.int), mode='valid')
        
        s_st = data['seqT'].idxmax(axis = 1)
        s_f = s_st + 6
        w_st = s_f
        w_f = w_st + 6
        
        if s_f > 12:
            s_f = s_f - 12
        if w_f > 12:
            w_f = w_f - 12
        if s_st > 12:
            s_st = s_st - 12
        if w_st > 12:
            w_st = w_st - 12
        
        drymonth = data['P'].idxmin(axis = 1)
        season = []
        
        if s_st < s_f and w_st < w_f:
            Psdry = data['P'][(data.index >= s_st) & (data.index < s_f)].min()
            Pwdry = (data['P'][(data.index >= w_st) & (data.index < w_f)].min())
            Pswet = data['P'][(data.index >= s_st) & (data.index < s_f)].max()
            Pwwet = (data['P'][(data.index >= w_st) & (data.index < w_f)].max())
            if s_st < drymonth and s_f > drymonth:
                season.append('summer')
            else:
                season.append('winter')
        
        if s_st < s_f and w_st > w_f:
            Psdry = data['P'][(data.index >= s_st) & (data.index < s_f)].min()
            Pwdry = (data['P'][(data.index >= w_st)].min(), data['P'][(data.index < w_f)].min())
            Pwdry = np.min(Pwdry)
            Pswet = data['P'][(data.index >= s_st) & (data.index < s_f)].max()
            Pwwet = (data['P'][(data.index >= w_st)].max(), data['P'][(data.index < w_f)].max())
            Pwwet = np.max(Pwwet)
            if s_st < drymonth and s_f > drymonth:
                season.append('summer')
            else:
                season.append('winter')
        
        if s_st > s_f and w_st < w_f:
            Psdry = (data['P'][(data.index >= s_st)].min(), data['P'][(data.index < s_f)].min())
            Psdry = np.min(Psdry)
            Pwdry = (data['P'][(data.index >= w_st) & (data.index < w_f)].min())
            Pswet = (data['P'][(data.index >= s_st)].max(), data['P'][(data.index < s_f)].max())
            Pswet = np.max(Pswet)
            Pwwet = (data['P'][(data.index >= w_st) & (data.index < w_f)].max())
        
            if w_st < drymonth and w_f > drymonth:
                season.append('winter')
            else:
                season.append('summer')    
        
        if s_st < w_st:
            s_f = s_f - 1
            w_f = w_f - 1
        else:
            w_f = w_f - 1
            s_f = s_f - 1
    
        if w_st == 12:
            w_st = 0
            
        if 0.7 * MAP <= data['seqP'].loc[w_st]:
            Pthresh = 2 * MAT
        elif 0.7 * MAP <= data['seqP'].loc[s_st]:
            Pthresh = 2 * MAT + 28
        else:
            Pthresh = 2 * MAT + 14
    
    else:
        if lat > 0:
            # N
            winter = np.concatenate((P[0:3], P[9:12]))
            summer = P[3:9]
            Psdry = np.min(summer)
            Pwdry = np.min(winter)
            Pswet = np.max(summer)
            Pwwet = np.max(winter)
        else:
            #S
            winter = P[3:9]
            summer = np.concatenate((P[0:3], P[9:12]))
            Psdry = np.min(summer)
            Pwdry = np.min(winter)
            Pswet = np.max(summer)
            Pwwet = np.max(winter)
    
    if P[3:9].sum()/(MAP + 0.1) > 0.3 and  P[3:9].sum()/(MAP + 0.1) < 0.7:
        p1 = 2 * MAT + 14
    else:
        p1 = 0
    if lat < 0 or p1 != 0:
        p2 = 0
    else:
        if P[3:9].sum()/(MAP + 0.1) > 0.7:
            p2 = 2 * MAT + 28
        else:
            p2 = 2 * MAT
    if lat > 0 or p1 != 0:
        p3 = 0
    else:
        if P[3:9].sum()/(MAP + 0.1) > 0.7:
            p3 = 2 * MAT
        else:
            p3 = 2 * MAT + 28
            
    Pthresh = p1 + p2 + p3

    main_class = []

    if z >= 2300:
        if Thot >= 0:
            main_class.append('HT - Tundra')
        else:
            main_class.append('HF - Frost or Ice Cap')
    elif MAP < (10 * Pthresh):
        main_class.append('B')
    elif len(main_class) == 0 and not Tcold < 18:
        main_class.append('A')
    elif len(main_class) == 0 and Thot >= 10 and Tcold < 18 and Tcold > 0:
        main_class.append('C')
    elif len(main_class) == 0 and Thot >= 10 and Tcold <= 0:
        main_class.append('D')
    elif len(main_class) == 0 and Thot < 10:
        main_class.append('E')
    
    second_class = []
    
    if main_class[0] == 'A':
        if Pdry >= 60:
            second_class.append('f')
        else:
            if Pdry >= 100 - MAP / 25:
                second_class.append('m')
            elif Psdry < 100 - MAP / 25:
                second_class.append('s')
            elif Pwdry < 100 - MAP / 25:
                second_class.append('w')

    elif main_class[0] == 'B':
        if MAP < 5 * Pthresh:
            second_class.append('W')
        else:
            second_class.append('S')
        if MAT >= 18:
            second_class.append('h')
        else:
            second_class.append('k')

    elif main_class[0] == 'C':
        if Psdry < 40 and Psdry < Pwwet / 3:
            second_class.append('s')
        elif Pwdry < Pswet / 10:
            second_class.append('w')
        else:
            second_class.append('f')
        if Thot >= 22:
            second_class.append('a')
        elif Tmonth10 >= 4:
            second_class.append('b')
        elif 1 <= Tmonth10 and Tmonth10 < 4:
            second_class.append('c')
    
    if main_class[0] == 'D':
        if Psdry < 40 and Psdry < Pwwet / 3:
            second_class.append('s')
        elif Pwdry < Pswet / 10:
            second_class.append('w')
        else:
            second_class.append('f')
        if Thot >= 22:
            second_class.append('a')
        elif Tmonth10 >= 4:
            second_class.append('b')
        elif Tcold < -38:
            second_class.append('d')
        else:
            second_class.append('c')

    if main_class[0] == 'E':
        if Thot > 0:
            second_class.append('T')
        else:
            second_class.append('F')
    main_class = ''.join(main_class)
    second_class = ''.join(second_class)
    classification = main_class + second_class
    return classification

# df = pd.read_excel(r'C:\Users\owner\Google Drive 2\MSc\TU DELFT - Water Managment\Additional Thesis\Scripts\book1.xlsx')

# iterations = 0
# world_kop = []
# for i in df.index:
#     world_kop.append(koppen((df['P1'][i], df['P2'][i], df['P3'][i], df['P4'][i], df['P5'][i], df['P6'][i], df['P7'][i], df['P8'][i], df['P9'][i], df['P10'][i], df['P11'][i], df['P12'][i]), (df['T1'][i], df['T2'][i], df['T3'][i], df['T4'][i], df['T5'][i], df['T6'][i], df['T7'][i], df['T8'][i], df['T9'][i], df['T10'][i], df['T11'][i], df['T12'][i]), df['lat'][i]))
#     iterations += 1
#     if iterations % 10000 == 0:
#         print(np.round((iterations / (114065 + 525) * 100), 1), '%')

# print('100.0 %')

# df['koppen_new'] = np.array(world_kop)
# df.to_excel(r"C:\Users\owner\Google Drive 2\MSc\TU DELFT - Water Managment\Additional Thesis\koppen_sample_stations.xlsx")
# print('Export DONE')
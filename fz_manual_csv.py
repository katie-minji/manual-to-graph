# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:21:13 2022

@author: Katie Kim
"""
# =============================================================================
# 
# PLEASE READ THIS!!!
# 
# 
# << Instructions >>
# 
# Purpose: 
# This code visualizes data from spreadsheet recording, manual freezing time for mouse.
# It makes two figures: control(ctr) mice and foot shock(FS) mice.
# This code creates subplots for each day, x=tone presentation, y=freezing%. 
# This codes scatter plot for each mouse in different colors, and an average line. 
# 
#
# To access: 
# 1. create spreadsheet with only data wanting to graph (filled/mouse finished scoring)
# 2. download spreadsheet as .csv file
# 3. open the .csv file when asked
#
# =============================================================================



#def text_extract(tone_duration, save_path, light_data, inter_df, post_df):

from tkinter.filedialog import askopenfilename
import pandas as pd
import math
import matplotlib.pyplot as plt



def final_dictionary(freezing_df):  #create final_dict (key=mouse, value=dataframes[exp_day, pres_num, tone, post_fzpc])) and type_dic (key=mouse, value=type[FS or ctr])
    col1 = freezing_df['Unnamed: 0'] #list containing first column
    mouse_list = [y for y in [x for x in col1 if isinstance(x,str)] if 'wt' in y] #checking list to see if wt is in mouse name, if yes, adding it to list
    type_list = [y for y in [x for x in col1 if isinstance(x,str)] if 'type' in y]
    type_list = [x.strip('type: ') for x in type_list]
    type_dict = {mouse_list[i]: type_list[i] for i in range(len(type_list))}
    final_dict ={} 
    #OVERALL: get mouse label, make new df of just one mouse (take 0:to next mouse-1), find freezing % d1
    for ienum,imouse in enumerate(mouse_list):
        temp1 = freezing_df.index[freezing_df['Unnamed: 0'] == mouse_list[ienum]].tolist() #set temp1 to the of index of the current mouse_name's row
        #if ienum is less than end of mouse_list index
        if imouse != mouse_list[-1]:
           temp2 = freezing_df.index[freezing_df['Unnamed: 0'] == mouse_list[(ienum)+1]].tolist() #set temp2 to index of the next mouse_name's row in line
        else:
            #get index of last row in df
            temp2 = [freezing_df.index[-1]] #set temp2 to bottom row of dataframe
        temp_df =  freezing_df.iloc[(temp1[0]):(temp2[0])]#cut from temp 1 to nextmouse-1: freezing_df.iloc[temp1:nextmouse-1]
        days = temp_df.loc[temp_df['Unnamed: 0'] == 'freezing % (freezing s/60s)'] #locates where the freezing % rows are, then grabs those rows
        ftones = temp_df.loc[temp_df['Unnamed: 0'] == 'Freq'] #locates where the frequency rows are, then grabs those rows
        exp_dayf = []
        pres_num = []
        freezingg = []
        freq2 = []
        for i in range(len(days)):
            exp_day = []
            d = days.iloc[i] #gets the freezing row for day i
            d2 = d.tolist()
            d_cleaned = [y for x, y in enumerate(d2) if (isinstance(y, str) and x != 0) ] #cleans out header and NaN values from day i freezing (leaving only the percents)
            check = days.loc[:,'Habituation'].tolist()
            for m in check: #sets up for loop to check if habituation period was scored; if yes, the first freezing is index 0
                check2 = math.isnan(float(m))
                if check2:
                    presnum = [(m+1) for m in range(len(d_cleaned))]
                else:
                    presnum = [m for m in range(len(d_cleaned))]
            #exp_day.append('D' + str(i+1))
            #print(exp_day)
            for x in range(len(d_cleaned)):
                exp_day.append('D' + str(i+1))
            f = ftones.iloc[i]
            f2 = f.tolist()
            f_cleaned = [y for x, y in enumerate(f2) if (isinstance(y, str) and x != 0) ]
            exp_dayf = exp_dayf + exp_day
            pres_num = pres_num + presnum
            freezingg = freezingg + d_cleaned
            freq2 = freq2 + f_cleaned
        freezing = [float(i)*100 for i in freezingg]
        one_mouse_df = pd.DataFrame(list(zip(exp_dayf, pres_num, freq2, freezing)), columns=['exp_day','pres_num','tone','post_fzpc'])
        final_dict.update({imouse:one_mouse_df})
    return final_dict, type_dict


def grouped_day_segregated_condition(final_dic, type_dic):
    ctr_mouse_list = []  #list of ctr mice codes
    fs_mouse_list = []  #list of fs mice codes 
    for mouse in type_dic:
        if type_dic[mouse] == 'ctr':
            ctr_mouse_list.append(mouse)
        else:
            fs_mouse_list.append(mouse)
    # group each mouse df in final_dic by days
    for mouse in final_dic:
        df = final_dic[mouse]
        df.groupby("exp_day")
    # segregate mice, with ctr, FS mouse list to 2 dictionaries from data analyzing, prior code frame
    ctr_dic = {}
    fs_dic = {}
    for mouse in final_dic:
        if mouse in ctr_mouse_list:
            ctr_dic.update({mouse: final_dic[mouse]})
        else:
            fs_dic.update({mouse: final_dic[mouse]})
    # put two segregated dictionaries into a list
    segregated_by_condition = [ctr_dic, fs_dic]
    return segregated_by_condition


def plot_graphs():
    def combine_df(num):
        df_list = []  #empty list to store data frames
        e=1
        for mouse in segregated_df[num]:
            df_copy = segregated_df[num][mouse].copy()  #copy of specific mouse data frame
            df_copy.drop(['tone'], axis=1, inplace=True)  #remove tone column
            df_copy.rename(columns={'post_fzpc':'post_fzpc'+str(e), 'exp_day':'exp_day'+str(e), 'pres_num':'pres_num'+str(e)}, inplace=True)  #rename to add index to each column
            df_list.append(df_copy)  #add dataframe to list
            e+=1
        final_df = pd.concat(df_list, join='outer', axis=1)  #combine dataframes
        return final_df
    def average_line(number):
        condition_ = df_total[0]
        j=0
        num_mouse = int(len(condition_.columns)/3)
        num_mouse_list = [*range(1, num_mouse+1)]
        post_fzpc_list = []
        for num in num_mouse_list:
            post_fzpc_list.append('post_fzpc' +str(num)) 
        condition_['average'] = condition_[post_fzpc_list].sum(axis=1) / num_mouse
        group_by_day_ = condition_.groupby('exp_day1')  #group by day
        for exp_day_ in group_by_day_:
            axs[j].plot(exp_day_[1]['pres_num1'], exp_day_[1]['average'])
            j+=1
    for condition in segregated_df:  #condition = ctr or fs, brings dictionary of mouse
        plt.style.use('seaborn')
        fig, axs = plt.subplots(nrows= 1, ncols= 3, sharey=True)   
        axs = axs.ravel()
        if condition == segregated_df[0]:  #if control mice
            fig.suptitle('Control Mice', fontsize=18)  #main title     
            ctr_df = combine_df(0)
            df_total = [ctr_df]
            average_line(0)
        else:  #if fs mice
            fig.suptitle('FS Mice', fontsize=18)  #main title     
            fs_df = combine_df(1)
            df_total = [fs_df]
            average_line(1)    
        for condition_ in df_total:
            j=0
            num_mouse = int(len(condition_.columns)/3)
            num_mouse_list = [*range(1, num_mouse+1)]
            post_fzpc_list = []
            for num in num_mouse_list:
                post_fzpc_list.append('post_fzpc' +str(num)) 
            condition_['average'] = condition_[post_fzpc_list].sum(axis=1) / num_mouse
            group_by_day_ = condition_.groupby('exp_day1')  #group by day
            for exp_day_ in group_by_day_:
                axs[j].plot(exp_day_[1]['pres_num1'], exp_day_[1]['average'], linewidth=2.5, color='#7f7f7f')
                j+=1
        for mouse in condition:  #for each mouse within ctr or fs dictionary
            i=0
            df = condition[mouse]  #designate specific data frame for each mouse
            group_by_day = df.groupby("exp_day")  #group by day
            for exp_day, exp_day_df in group_by_day:  #for days grouped within each mouse df
                axs[i].scatter(exp_day_df['pres_num'], exp_day_df['post_fzpc'], label=mouse)  #x-axis = presentation, y-axis = freezing %            
                axs[i].set_title(exp_day)  #set subtitle for each day
                num_row = int(exp_day_df.groupby("exp_day").size())  #number of row for day
                axs[i].set_xticks(range(num_row))  #scale by 1, presentation int only list by range function
                axs[i].set_yticks(range(0,101,20))
                i+=1
        axs[1].set_xlabel('presentations', fontsize=13)  #set x-axis label
        axs[0].set_ylabel('freezing %', fontsize=13)  #set y-axis label    
        
        axs[2].legend(bbox_to_anchor=(1.6, 0.5), loc='center right')
        
        fig.tight_layout()  #prevent overlap
        
    
    

res = final_dictionary(pd.read_csv(askopenfilename()))  #[0] == final_dic, [1] == type_dic
segregated_df = grouped_day_segregated_condition(res[0], res[1])
plot_graphs()









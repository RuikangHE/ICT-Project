# -*- coding: utf-8 -*-
"""
Created on Fri Apr 1 02:15:32 2020

@author: 236918615@qq.com
"""
import tkinter as tk
from tkinter import ttk
import pandas as pd
import datetime as dt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# read data from excel file


root= tk.Tk()

ds = pd.read_csv("C:\\Users\\23691\\Desktop\\Wheels History 2.csv")

canvas1 = tk.Canvas(root, width = 399, height = 333)
canvas1.pack()

#
Intercept_result = ('Intercept: ', "")
label_Intercept = tk.Label(root, text=Intercept_result[0]+Intercept_result[1])
canvas1.create_window(160, 230, anchor = tk.E, window=label_Intercept)

#
Coefficients_result  = ('Coefficients: ', "")
label_Coefficients = tk.Label(root, text=Coefficients_result[0]+Intercept_result[1])
canvas1.create_window(160, 260, anchor = tk.E, window=label_Coefficients)

Prediction_Level = ('Current Prediction Level: ', "")
label_prediction_Level = tk.Label(root, text=Prediction_Level[0] + Prediction_Level[1])
canvas1.create_window(160 , 290, anchor = tk.E, window=label_prediction_Level)
# 
label1 = tk.Label(root, text=' Select Locomotive: ')
canvas1.create_window(160, 60, anchor = tk.E, window=label1)

cbox1 = ttk.Combobox(root, textvariable  = tk.StringVar())
cbox1['values']=ds['Unit'].unique().tolist()
cbox1.current(0)
canvas1.create_window(266, 60, width = 210, window=cbox1)

#
label2 = tk.Label(root, text=' Select Parameter: ')
canvas1.create_window(160, 85, anchor = tk.E, window=label2)

cbox2 = ttk.Combobox(root, textvariable  = tk.StringVar())
cbox2['values']=["L1_DiameterFIX","L2_DiameterFIX", "L3_DiameterFIX", "L4_DiameterFIX", "L5_DiameterFIX","L6_DiameterFIX",
                 "R1_DiameterFIX", "R2_DiameterFIX", "R3_DiameterFIX", "R4_DiameterFIX","R5_DiameterFIX","R6_DiameterFIX"]+ list(ds)[33:]
cbox2.current(0)
canvas1.create_window(266, 85, width = 210, window=cbox2)

# 
label3 = tk.Label(root, text='Select Time Period: ')
canvas1.create_window(160, 110,anchor = tk.E,  window=label3)

entry3 = tk.Entry (root) # create 1st entry box
entry3.insert(0, '200')
canvas1.create_window(266, 110, width = 210, window=entry3)

# 
label4 = tk.Label(root, text=' Select Odometer: ')
canvas1.create_window(160, 135, anchor = tk.E, window=label4)

entry4 = tk.Entry (root) # create 2nd entry box
entry4.insert(0, '20000')
canvas1.create_window(266, 135, width = 210, window=entry4)


label5 = tk.Label(root, text=' Select Prediction Level: ')
canvas1.create_window(160,160, anchor = tk.E, window=label5)

#combo box
cbox6 = ttk.Combobox(root, textvariable  = tk.StringVar())
cbox6['values']=('Level 1', 'Level 2', 'Level 3')
cbox6.current(0)
canvas1.create_window(266, 160, width = 210, window=cbox6)

# entry to display intercept
entry7 = tk.Entry (root, state='readonly') # create 2nd entry box
canvas1.create_window(266, 230, width = 210, window=entry7)

# entry to display coefficients
entry8 = tk.Entry (root, state='readonly') # create 2nd entry box
canvas1.create_window(266, 260, width = 210, window=entry8)

# entry to display intercept
entry9 = tk.Entry (root, state='readonly') # create 2nd entry box
canvas1.create_window(266, 290, width = 210, window=entry9)

    
def clean_up_data_and_return_Lv1_predictor(locomotive, parameter):
    data = pd.read_csv("C:\\Users\\23691\\Desktop\\Wheels History 2.csv")
    data = data[data[data.columns[0]] == locomotive]
    #data = data.sort_values(by=data.columns[1], ascending=True, ignore_index=True)
    ref = data.reset_index(drop=True)
    x = []
    y = []
    kilo = []
    ref = ref.dropna(subset = ['Odometer'])
    ref = ref.reset_index(drop=True)
    row = ref.shape[0] #row count
    for i in range(1, row):
        if(ref.loc[ i, parameter] < ref.loc[ i - 1, parameter]):
            date_residual = ref.loc[i, "Days"]
            # calculate kilometer residuals
            k1 = ref.loc[i - 1, 'Odometer']
            k2 = ref.loc[i, 'Odometer']
            kr = k2 - k1
            if kr > 0:
                kilo.append(kr)
                parameter_residual = ref.loc[ i - 1, parameter] - ref.loc[ i, parameter]
                x.append(date_residual)
                y.append(parameter_residual)
    date = pd.DataFrame(x, columns = ['Date read'])
    dia = pd.DataFrame(y, columns = [parameter])
    kilo = pd.DataFrame(kilo, columns=['Odometer'])
    con = pd.concat([date, kilo, dia], axis = 1)
    # print out the cleaned-up dataframe
    #print(con)
    x_final = con[['Date read', 'Odometer']]
    if(not entry3.get()):
        x_final = x_final[['Odometer']]
    elif(not entry4.get()):
        x_final = x_final[['Date read']]
    #date -----> predicted diameter
    y_final = con[[parameter]]
    try:
        x_train, x_test, y_train, y_test = train_test_split(x_final, y_final, test_size = 0.2, random_state = 0)  
        lr = LinearRegression().fit(x_train, y_train)
        return lr
    except:
        tk.messagebox.showinfo(title='Warning', message = 'The dataset for selected locomotive is too small,'
                               + '\nplease increase the prediction level so that a proper prediction can be made.')

def clean_up_data_and_return_Lv2_predictor(locomotive):
    data = pd.read_csv("C:\\Users\\23691\\Desktop\\Wheels History 2.csv")
    data = data[data[data.columns[0]] == locomotive]
    #data = data.sort_values(by=data.columns[1], ascending=True, ignore_index=True)
    data['Date read'] = pd.to_datetime(data['Date read'])
    data['Date read'] = data['Date read'].map(dt.datetime.toordinal)
    ref = data.reset_index(drop=True)
    x = []
    y = []
    kilo = []
    all_rim = ["L2_DiameterFIX", "L3_DiameterFIX", "L4_DiameterFIX", "L6_DiameterFIX","R1_DiameterFIX", "R2_DiameterFIX", "R3_DiameterFIX", "R4_DiameterFIX","R5_DiameterFIX","R6_DiameterFIX"]
    for rim in all_rim:
        ref = ref.dropna(subset = ['Odometer'])
        ref = ref.reset_index(drop=True)
        row = ref.shape[0] #row count
        if(row < 10):
            print('\nWarning: The dataset is too small, prediction accuracy will be influenced')
        for i in range(1, row):
             if(ref.loc[ i, rim] < ref.loc[ i - 1, rim] and ref.loc[i, rim] < 100 and ref.loc[i - 1, rim] < 100):
                date_residual = ref.loc[i, "Days"]
                # calculate kilometer residuals
                k1 = ref.loc[i - 1, 'Odometer']
                k2 = ref.loc[i, 'Odometer']
                kr = k2 - k1
                if kr > 0:
                    kilo.append(kr)
                    parameter_residual = ref.loc[ i - 1, rim] - ref.loc[ i, rim]
                    x.append(date_residual)
                    y.append(parameter_residual)
    date = pd.DataFrame(x, columns = ['Date read'])
    dia = pd.DataFrame(y, columns = [rim])
    dia = dia.rename({rim: 'RIM-DIA wear-offs'}, axis=1)  # rename columns otherwise might cause confusion
    kilo = pd.DataFrame(kilo, columns=['Odometer'])
    con = pd.concat([date, kilo, dia], axis = 1)
        # print out the cleaned-up dataframe
    #print(con)
    x_final = con[['Date read', 'Odometer']]
    if(not entry3.get()):
        x_final = x_final[['Odometer']]
    elif(not entry4.get()):
        x_final = x_final[['Date read']]
    #date -----> predicted diameter
    y_final = con[["RIM-DIA wear-offs"]]
    try:
        x_train, x_test, y_train, y_test = train_test_split(x_final, y_final, test_size = 0.2, random_state = 0)  
        lr = LinearRegression().fit(x_train, y_train)
        return lr
    except:
        tk.messagebox.showinfo(title='Warning', message = 'The dataset for selected locomotive is too small,'
                               + '\nplease increase the prediction level so that a proper prediction can be made.')

def clean_up_data_and_return_Lv3_predictor(locomotive):
    data = pd.read_csv("C:\\Users\\23691\\Desktop\\Wheels History 2.csv")
    # extract locomotive class
    loco_class = ''
    for index in range(0, len(locomotive)):
        if(not locomotive[index].isdigit()):
            loco_class += locomotive[index]
        elif(locomotive[index].isdigit()):
            break
    # end of extraction
    data = data[data[data.columns[0]].str.startswith(loco_class)]
    ref = data.reset_index(drop=True)
    print(ref)
    x = []
    y = []
    kilo = []
    loco = []
    all_rim = ["L2_DiameterFIX", "L3_DiameterFIX", "L4_DiameterFIX", "L6_DiameterFIX","R1_DiameterFIX", "R2_DiameterFIX", "R3_DiameterFIX", "R4_DiameterFIX","R5_DiameterFIX","R6_DiameterFIX"]
    for rim in all_rim:
        ref = ref.dropna(subset = ['Odometer'])
        ref = ref.reset_index(drop=True)
        row = ref.shape[0] #row count
        if(row < 10):
            print('\nWarning: The dataset is too small, prediction accuracy will be influenced')
        for i in range(1, row):
             if(ref.loc[ i, rim] < ref.loc[ i - 1, rim]):
                date_residual = ref.loc[i, 'Days']
                # calculate kilometer residuals
                k1 = ref.loc[i - 1, 'Odometer']
                k2 = ref.loc[i, 'Odometer']
                kr = k2 - k1
                if kr > 0:
                    loco.append(ref.loc[i, 'Unit'])
                    kilo.append(kr)
                    parameter_residual = ref.loc[ i - 1, rim] - ref.loc[ i, rim]
                    x.append(date_residual)
                    y.append(parameter_residual)       
    locos = pd.DataFrame(loco, columns = ['Locomotive'])
    date = pd.DataFrame(x, columns = ['Date read'])
    dia = pd.DataFrame(y, columns = [rim])
    dia = dia.rename({rim: 'RIM-DIA wear-offs'}, axis=1)  # rename columns otherwise might cause confusion
    kilo = pd.DataFrame(kilo, columns=['Odometer'])
    con = pd.concat([locos, date, kilo, dia], axis = 1)
    # print out the cleaned-up dataframe
    #print(con)
    x_final = con[['Date read', 'Odometer']]
    if(not entry3.get()):
        x_final = x_final[['Odometer']]
    elif(not entry4.get()):
        x_final = x_final[['Date read']]
    #date -----> predicted diameter
    y_final = con[["RIM-DIA wear-offs"]]
    try:
        x_train, x_test, y_train, y_test = train_test_split(x_final, y_final, test_size = 0.2, random_state = 0)  
        lr = LinearRegression().fit(x_train, y_train)
        return lr
    except:
        tk.messagebox.showinfo(title='Warning', message = 'The dataset for selected locomotive is too small,'
                               + '\nplease increase the prediction level so that a proper prediction can be made.')

#plot 1st scatter 
ds = pd.read_csv("C:\\Users\\23691\\Desktop\\Wheels History 2.csv")
ds = ds[ds[ds.columns[0]] == 'CM3306H']
ds = ds.reset_index(drop=True)
ds['Date read'] = pd.to_datetime(ds['Date read'])
print(ds['Date read'])
figure3 = plt.Figure(figsize=(8,6), dpi=100)
ax3 = figure3.add_subplot(111)
#ax3.plot_date(ds['Date read'],ds[cbox2.get() + 'FIX'].astype(float))
scatter3 = FigureCanvasTkAgg(figure3, root) 
# for c,d in zip(ds['Date read'], ds[cbox2.get() + 'FIX']):
#     ax3.text(c,d,str(d))
scatter3.get_tk_widget().pack(side=tk.RIGHT, fill=tk.X)
ax3.legend(['Stock_Index_Price'])
ax3.set_xlabel('Time Period')
ax3.set_title('Time Period Vs. RIM/DIA')

#plot 2nd scatter 
figure4 = plt.Figure(figsize=(8,6), dpi=100)
ax4 = figure4.add_subplot(111)
#ax4.scatter(ds['Odometer'].astype(float), ds[cbox2.get() + 'FIX'].astype(float), color = 'g')
scatter4 = FigureCanvasTkAgg(figure4, root)
# for a,b in zip(ds['Odometer'], ds[cbox2.get() + 'FIX']):
#     ax4.text(a,b,str(b))
scatter4.get_tk_widget().pack(side=tk.RIGHT, fill=tk.X)
ax4.legend([cbox2.get()]) 
ax4.set_xlabel('Odometer')
ax4.set_title('Odometer Vs. RIM/IDA')

def make_prediction_and_update_graphs(): 
    if(not entry3.get() and not entry4.get()):
        tk.messagebox.showinfo(title='Warning', message = 'Please input a time period or odometer')
        return
    global New_Locomotive # the locomotive specified by user input
    New_Locomotive = cbox1.get()
    
    global New_Parameter # the parameter to be predicted
    New_Parameter = cbox2.get()# + "FIX"
    
    global New_Time_Period #our 1st input variable
    if(entry3.get()):
        New_Time_Period = float(entry3.get()) 
    
    global New_Odometer #our 2nd input variable
    if(entry4.get()):
        New_Odometer = float(entry4.get()) 
    
    # Generate predictor according to user input
    global New_Predictor
    # Generate Lv 1 predictor by default
    if(cbox6.current() == 0):
        New_Predictor = clean_up_data_and_return_Lv1_predictor(New_Locomotive, New_Parameter)
    elif(cbox6.current() == 1):
        New_Predictor = clean_up_data_and_return_Lv2_predictor(New_Locomotive)
    elif(cbox6.current() == 2):
        New_Predictor = clean_up_data_and_return_Lv3_predictor(New_Locomotive) # the predictor
    
    if New_Predictor is None:
        return
    # Intercept_result = ('Intercept: ', Predictor.intercept_)
    # label_Intercept = tk.Label(root, text=Intercept_result[0]+str(Intercept_result[1][0]), justify = 'center')
    # canvas1.create_window(199, 230, window=label_Intercept)
    
    # Coefficients_result  = ('Coefficients: ', Predictor.coef_)
    # label_Coefficients = tk.Label(root, text=Coefficients_result[0]+str(Coefficients_result[1][0]), justify = 'center')
    # canvas1.create_window(199, 250, window=label_Coefficients)
    
    # Prediction_Level = ('Current Prediction Level: ', cbox6.current())
    # label_prediction_Level = tk.Label(root, text=Prediction_Level[0] + str(Prediction_Level[1]))
    # canvas1.create_window(199 , 270, window=label_prediction_Level)
    entry7.configure(state='normal')
    entry8.configure(state='normal')
    entry9.configure(state='normal')
    entry7.delete(0, 'end')
    entry8.delete(0, 'end')
    entry9.delete(0, 'end')
    entry7.insert(0, str(New_Predictor.intercept_[0]))
    entry8.insert(0, str(New_Predictor.coef_[0]))
    entry9.insert(0, str(cbox6.get()))
    entry7.configure(state='disabled')
    entry8.configure(state='disabled')
    entry9.configure(state='disabled')
    # round prediction result to 1 decimal point
    Prediction_result = '';
    if(entry3.get() and entry4.get()):
        Prediction_result  = round(New_Predictor.predict([[New_Time_Period, New_Odometer]])[0][0],1)
    elif(not entry3.get()):
        Prediction_result  = round(New_Predictor.predict([[New_Odometer]])[0][0],1)        
    elif(not entry4.get()):
        Prediction_result  = round(New_Predictor.predict([[New_Time_Period]])[0][0],1)
    if(New_Predictor.coef_[0][0] == 0 and New_Predictor.coef_[0][1] == 0):    
        tk.messagebox.showinfo(title='Warning', message = 'The dataset for selected locomotive/parameter is too small,'
                               + '\nplease increase the prediction level so that a proper prediction can be made.')
        return
    label_Prediction = tk.Label(root, text='Predicted ' + New_Parameter + ' wear-off: ' + str(Prediction_result), bg='orange')
    canvas1.create_window(210, 320, width = 300, window=label_Prediction)
    
    #update graphs
    ax3.clear()
    ax3.plot_date(ds['Date read'],ds[cbox2.get()].astype(float))
    ax3.legend([cbox2.get()]) 
    ax3.set_xlabel('Time Period')
    ax3.set_title('Time Period Vs. RIM/IDA')
    scatter3.draw()
    
    ax4.clear()
    ax4.scatter(ds['Odometer'].astype(float), ds[cbox2.get()].astype(float), color = 'g')
    ax4.legend([cbox2.get()]) 
    ax4.set_xlabel('Odometer')
    ax4.set_title('Odometer Vs. RIM/IDA')
    scatter4.draw()
    
    
button1 = tk.Button (root, text='Predict Wear-offs',command=make_prediction_and_update_graphs, bg='orange') # button to call the 'values' command above 
canvas1.create_window(210, 195, width = 300, window=button1)

root.mainloop()


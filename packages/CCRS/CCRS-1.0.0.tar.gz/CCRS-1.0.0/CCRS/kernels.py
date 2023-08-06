#import dependent packages
import pickle
import scipy.stats as st
import pandas as pd
import numpy as np

def qtrans(y):
  y = pd.Series(y.reshape((-1,)))
  y_rank = y.rank(method='first')
  y_rank = y_rank.astype('int64') - 1
  value = np.arange(1,(len(y)+1))  -0.5
  value = value / len(y)
  z = st.norm.ppf(value)
  #get the order of sample
  z = z[y_rank]
  return z
def relative_risk_inner(x,traindata):
  y = np.append(traindata,x)
  z = qtrans(y)
  z = z[-1]
  result = st.norm.cdf(z)#........
  return(result)    
def RRScore(df,Traindata,mean,sd):
  Result=[]
  for a in range(df.shape[0]):
    x = df.y_pred[a]
    value = df.Age[a]
    value = value*sd+mean
    value = float(value)
    #check Age group
    if(value<50):
      traindata=Traindata.y_pred[Traindata.Age<50]
    if(value<60 and value>=50):
      traindata=Traindata.y_pred[(Traindata.Age<60) & (Traindata.Age>=50)]
    if(value<70 and value>=60):
      traindata=Traindata.y_pred[(Traindata.Age<70) & (Traindata.Age>=60)]
    if(value<80 and value>=70):
      traindata=Traindata.y_pred[(Traindata.Age<80) & (Traindata.Age>=70)]
    if(value>=80):
      traindata=Traindata.y_pred[Traindata.Age>=80]
    Result.append(relative_risk_inner(x,traindata))
  return(Result)

def preprocess(X_test,disease='CHD'):
  fea =['Age','PLT','TC','LDL_C','baPWV','ABI','log_CEA','HbA1c','Hypertension']
  if(disease=='CHD'):
    my_mean = [52.8,215.0,4.8,2.9,1416.6,1.1,1.1,5.8]
    my_sd = [9.8,53.1,0.9,0.8,247.5,0.1,0.4,0.7]
  if(disease=='CIS'):
    my_mean = [51.5,215.7,4.8,2.9,1401.8,1.1,1.0,5.8]
    my_sd = [10.8,53.6,0.9,0.8,247.7,0.1,0.4,0.7]
  X_test = X_test.loc[:,fea]
  newdata = X_test
  for i in range(9):
    m = my_mean[i]
    s = my_sd[i]
    v = np.array(X_test.iloc[:,i])
    #make sure value is number
    m = float(m)
    s = float(s)  
    newdata.iloc[:,i]  =  (v - m) / s
  return(newdata)

def risk_label(scores,disease='CHD'):
  risk_label=[]
  if disease=='CHD':
    low_point = 0.38
    high_point = 0.74
  if disease=='CIS':
    low_point = 0.31
    high_point = 0.79
  for i in scores:
    if i <low_point:
      t1 = 'mild'
    elif (i<=high_point and i>=low_point):
      t1 = 'moderate'
    elif i>high_point:
      t1 = 'severe'
    risk_label.append(t1)
  return(risk_label)
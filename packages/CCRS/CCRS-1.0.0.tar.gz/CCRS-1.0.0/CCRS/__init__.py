#input functions in kernels
from .kernels import *
from urllib.request import urlopen
# main function for scaling 

def CCR(X_test):
  raw_data = X_test
  #CHD
  X_test = preprocess(raw_data)
  loaded_model = pickle.load('./data/CHD_RF_lessFea.pkl')
  Traindata = pd.read_csv('./data/CHD_age.csv')
  scores = loaded_model.predict_proba(X_test)
  value = scores[:,1]
  CHD_value = risk_label(value)
  df = pd.DataFrame({'y_pred': scores[:,1],'Age':X_test.Age})
  CHD_RRS = RRScore(df,Traindata,mean=52.81386,sd=9.831492)
  #CIS
  X_test = preprocess(raw_data,disease='CIS')
  loaded_model = pickle.load('./data/CIS_RF_lessFea.pkl')
  Traindata = pd.read_csv('./data/CIS_age.csv')
  scores = loaded_model.predict_proba(X_test)
  value = scores[:,1]
  CIS_value = risk_label(value,disease='CIS')
  df = pd.DataFrame({'y_pred': scores[:,1],'Age':X_test.Age})
  CIS_RRS = RRScore(df,Traindata,mean=51.52208,sd=10.84735)
  # combine result
  df = pd.DataFrame({'CHD_risk_group': CHD_value,'CHD_relative_risk_rank':CHD_RRS,'CIS_risk_group': CIS_value,'CIS_relative_risk_rank':CIS_RRS})
  return(df)

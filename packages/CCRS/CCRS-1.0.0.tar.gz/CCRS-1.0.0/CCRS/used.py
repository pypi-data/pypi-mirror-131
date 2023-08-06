def new_site(X,Sub):
    #get special samples site in data 
  X = np.array(X)
  Sub = np.array(Sub)
  result=[]
  for a in range(len(Sub)):
    value = Sub[a,]
    for b in range(len(X)):
      if (value == X[b,]).all():
        result.append(b)
        break
  return result

from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D  
def draw_PCA(X,labels,filename=None):
    #output different between ture and pred
  pca=PCA(n_components=3,copy=True, whiten=False)
  y_test,y_pred = labels
  df=pca.fit_transform(X)
  plt.figure(figsize=(12,6))
  plt.subplot('121')
  plt.scatter(df[:, 0], df[:, 1],marker='o',c=y_test,cmap='Set1',alpha=0.6)
  plt.legend(['y_test'])
  plt.subplot('122')
  plt.scatter(df[:, 0], df[:, 1],marker='o',c=y_pred,cmap='Set1',alpha=0.6)
  plt.legend(['y_pred'])

  plt.show()
  return None
from sklearn import manifold
def draw_tsne(X,labels,filename=None):
    #PCA perform bad, try tsne
  y_test,y_pred = labels
  tsne = manifold.TSNE(n_components=2, init='pca', random_state=111)
  df = tsne.fit_transform(X)
  plt.figure(figsize=(12,6))
  plt.subplot('121')
  plt.scatter(df[:, 0], df[:, 1],marker='o',c=y_test,cmap='Paired',alpha=0.6)
  plt.legend(['y_test'])
  plt.subplot('122')
  plt.scatter(df[:, 0], df[:, 1],marker='o',c=y_pred,cmap='Paired',alpha=0.6)
  plt.legend(['y_pred'])
  plt.show()
  return None


#main resample function
def over_sample(Dat,Method='BorderlineSMOTE',seed=111,filename=None,silent=0,sampling_strategy=1):
  X,y=Dat
  from imblearn.over_sampling import SMOTE,BorderlineSMOTE,ADASYN
  from collections import Counter
  if Method == 'SMOTE':
    sm = SMOTE(random_state=seed)
    X_res, y_res = sm.fit_resample(X, y)
  if Method == 'BorderlineSMOTE':
      #BorderlineSMOTE perform best in testing
    sm = BorderlineSMOTE(random_state=seed,kind="borderline-1",sampling_strategy=sampling_strategy)
    X_res, y_res = sm.fit_resample(X, y)
  if Method == 'ADASYN':
    sm = ADASYN(random_state=seed)
    X_res, y_res = sm.fit_resample(X, y)
  if Method == 'None':
    X_res =np.array(X)
    y_res = np.array(y)
  
  clear_output()
  print('Method could be SMOTE(default), BorderlineSMOTE, ADASYN, None',flush=True)
  print('---------------Method : ',Method,'-------------------')
  print('Resampled dataset shape %s' % Counter(y_res))
  #output downsampled data
  if not filename is None:
    temp = np.hstack((X_res,y_res.reshape(-1,1)))
    temp = pd.DataFrame(temp)
    fea = X.columns.values.tolist()
    fea.append('result_after3year')
    temp.columns = fea
    temp.to_csv(filename,index=False,sep=',',encoding='utf_8_sig')
  X_res = pd.DataFrame(X_res)
  X_res.columns = X.columns.values.tolist()
  y_res = pd.Series(y_res.tolist())
  #output in spllit way
  return(X_res,y_res)

def act1(x,threshold=0.5):
    #like softmax function
  if x>=threshold:
    return 1
  if x<threshold:
    return 0

def creat_model(ncol):
    #MLP model built
  METRICS = [
      tf.keras.metrics.BinaryAccuracy(name='accuracy'),
      tf.keras.metrics.Precision(name='precision'),
      tf.keras.metrics.Recall(name='recall'),
      tf.keras.metrics.AUC(name='auc'),
      tf.keras.metrics.SpecificityAtSensitivity(0.5,name='specificity')
  ]
  
  model= tf.keras.Sequential(name='MLP_Model')
  model.add(tf.keras.layers.Dense(32,input_shape=(ncol,),activation='selu'))
  model.add(tf.keras.layers.Dense(32,activation='selu'))
  #dropout is used to increase robust of model 
  model.add(tf.keras.layers.Dropout(0.5))
  model.add(tf.keras.layers.Dense(16,activation='selu'))
  model.add(tf.keras.layers.Dense(16,activation='selu'))
  model.add(tf.keras.layers.Dropout(0.5))
  model.add(tf.keras.layers.Dense(8,activation='selu'))
  model.add(tf.keras.layers.Dense(8,activation='selu'))
  model.add(tf.keras.layers.Dropout(0.5))
  model.add(tf.keras.layers.Dense(4,activation='selu'))
  model.add(tf.keras.layers.Dense(4,activation='selu'))
  model.add(tf.keras.layers.Dropout(0.5))
  model.add(tf.keras.layers.Dense(1,activation='sigmoid'))
  #optimizer could use sgd or Adam
  model.compile(optimizer='sgd',
              loss='binary_crossentropy',
              metrics=METRICS)
  return model

def all_score(y_test,y_pred):
    #calculate evaluation score of result
  y_test=np.array(y_test)
  y_pred=np.array(y_pred)
  tp=0
  fp=0
  fn=0
  tn=0
  for j in range(len(y_pred)):
    if y_test[j]==0 and y_pred[j]==0:
      tn=tn+1
    if y_test[j]==1 and y_pred[j]==0:
      fn=fn+1
    if y_test[j]==0 and y_pred[j]==1:
      fp=fp+1
    if y_test[j]==1 and y_pred[j]==1:
      tp=tp+1

  acc = (tp+tn)/(tp+tn+fp+fn)
  sen = tp/(tp+fn)
  spe = 1 - (fp/(fp+tn))
  if (tp+fp)==0:
    pre = -1
  else:
    pre = tp/(tp+fp)
  rec = tp/(tp+fn)
  if pre==0 or rec==0:
    F = -1
  else :
    F = 2/(1/pre +1/rec)
  print("Accuracy :", acc)
  #print("Recall  :", rec)
  print("Precision :", pre)
  print("Sensitivity :", sen)
  print("Specificity :",spe)
  print("F-measure :", F)
  return None

def creat_train_test(X,y,label,test_size=0.2,seed=0):
    # consider sample split
  random.seed( seed )
  X = pd.DataFrame(X)
  X.index = range(X.shape[0])
  y = pd.Series(np.array(y))
  label = np.array(label)
  ids = np.unique(label)
  rows_count = X.shape[0]
  test_count = int(rows_count*test_size)
  site=[]
  while True:
    #random.seed( seed )
    new_id =random.sample(ids.tolist(),1) 
    ids = np.setdiff1d(ids,np.array(new_id))
    site.extend((np.where(label==new_id[0]))[0].tolist())
    if(len(site)>=test_count):
        X_test = X.loc[site]
        y_test = y[site]
        X_train = X.drop(site)
        y_train = y.drop(site)
        print(Counter(y))
        print(Counter(y_train))
        print(Counter(y_test))
        label = pd.Series(np.array(label))
        site = new_site(X,X_train)
        train_label = label[site]
        train_label = pd.Series(np.array(train_label))
        site = new_site(X,X_test)
        test_label = label[site]
        test_label = pd.Series(np.array(test_label))
        return(X_train,y_train,X_test,y_test,train_label,test_label)
        break
    #seed = seed+1

from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier
def best_param(X,y,estimator,seed=111):
    #used to find best params
  random.seed( seed )
  skf = StratifiedKFold(n_splits=5)
  acc_result=np.array(0)
  sen_result=np.array(0)
  spe_result=np.array(0)
  pre_result=np.array(0)
  rec_result=np.array(0)
  F_result=np.array(0)
  au_result=np.array(0)
  y_result={}
  relative_score_result = {}
  Age = {}
  k=1
  k2 = 1
  for train, test in skf.split(X, y):
    X_train_sub = X.iloc[train,:]
    X_val = X.iloc[test,:]
    y_train_sub = y_train.reindex(train)
    y_val = y_train.reindex(test)
    
    y_val = np.array(y_val)
    y_val = y_val.reshape(-1,1)
    y_val = y_val.tolist()

    model = estimator
    # fit the model
    model.fit(X_train_sub, y_train_sub)
    y_pred = model.predict(X_val)
    
    relative_score = relative_risk(y_pred)
    relative_score_result[k2] = relative_score
    Age[k2]= X_val.Age
    k2 = k2+1
    y_result[k] = y_val
    y_result[k+1] = y_pred
    k=k+2
    y_pred =y_pred.tolist()

    au = tf.keras.metrics.AUC()  #according to data
    au.update_state(y_val,y_pred)
    au = au.result().numpy()
    au_result = np.append(au_result,au)

    y_pred = np.array(y_pred)
    for j in range(len(y_pred)):
      y_pred[j] = act1(y_pred[j])
    
    y_val = np.array(y_val)

    tp=0
    fp=0
    fn=0
    tn=0
    for j in range(len(y_pred)):
      if y_val[j]==0 and y_pred[j]==0:
        tn=tn+1
      if y_val[j]==1 and y_pred[j]==0:
        fn=fn+1
      if y_val[j]==0 and y_pred[j]==1:
        fp=fp+1
      if y_val[j]==1 and y_pred[j]==1:
        tp=tp+1
      

    acc = (tp+tn)/(tp+tn+fp+fn)
    sen = tp/(tp+fn)
    spe = 1 - (fp/(fp+tn))
    if (tp+fp)==0:
      pre = -1
    else:
      pre = tp/(tp+fp)
    rec = tp/(tp+fn)
    if pre==0 or rec==0:
      F = -1
    else :
      F = 2/(1/pre +1/rec)

    acc_result=np.append(acc_result,acc)
    sen_result=np.append(sen_result,sen)
    spe_result=np.append(spe_result,spe)
    pre_result=np.append(pre_result,pre)
    rec_result=np.append(rec_result,rec)
    F_result=np.append(F_result,F)

  au_result = np.delete(au_result,0,axis=0)
  acc_result = np.delete(acc_result,0,axis=0)
  rec_result = np.delete(rec_result,0,axis=0)
  pre_result = np.delete(pre_result,0,axis=0)
  sen_result = np.delete(sen_result,0,axis=0)
  spe_result = np.delete(spe_result,0,axis=0)
  F_result = np.delete(F_result,0,axis=0)
  return([np.mean(au_result),np.mean(acc_result),np.mean(pre_result),np.mean(sen_result),np.mean(spe_result),np.mean(F_result)])

def final_metric_reuslt(his):
    #print all result in history
  key = his.history.keys()
  for a in key:
    print(a+':'+str(his.history.get(a)[-1]))
  return None

def backprop_dense(activation, kernel, bias, relevance,alpha=1,use_matmul=True,relu=True,epi=1e-7):   
    # selu is different in alpha  
  if relu:
    W_p = tf.maximum(epi, kernel)    
    b_p = tf.maximum(epi, bias)    
  else:
    W_p=tf.convert_to_tensor(kernel)
    b_p = tf.convert_to_tensor(bias)
  if use_matmul:
    z_p = tf.matmul(activation, W_p) + b_p
  else:
    z_p = np.dot(activation, W_p) + b_p
  s_p = relevance / z_p    
  c_p = tf.matmul(s_p, tf.transpose(W_p)) 
  #-----------------------------------------------------------
  if relu:
    W_n = tf.maximum(epi, kernel)    
    b_n = tf.maximum(epi, bias)    
  else:
    W_n=tf.convert_to_tensor(kernel)
    b_n = tf.convert_to_tensor(bias) 
  if use_matmul:
    z_n = tf.matmul(activation, W_n) + b_n
  else:
    z_n = np.dot(activation, W_n) + b_n
  s_n = relevance / z_n    
  c_n = tf.matmul(s_n, tf.transpose(W_n)) 

  result = activation * (alpha * c_p + (1 - alpha) * c_n)  #activation * 
  return result.numpy()

def mulit_plr(Dat,model,l):
    #get plr one layer by one layer
  for a in reversed(range(l)):
    s2='D_'+str(a+1)
    s1='D_'+ str(a)
    if a != 0:
      d1 = tf.keras.models.Model(inputs=model.input,outputs=model.get_layer(s1).output)
      d1_output = d1.predict(Dat)
    if a==0:
      d1_output = Dat
    if a== (l-1):
      d2 = tf.keras.models.Model(inputs=model.input,outputs=model.get_layer(s2).output)
      d2_output = d2.predict(Dat)
    weight_Dense_2,bias_Dense_2 = model.get_layer(s2).get_weights()
    
    if a == (l-1):
      d2_output = backprop_dense(d1_output,weight_Dense_2,bias_Dense_2,d2_output,use_matmul=False,relu=False)
    else:
      d2_output = backprop_dense(d1_output,weight_Dense_2,bias_Dense_2,d2_output,use_matmul=False)
  return(d2_output)

def my_log_loss(y_true,y_pred):
    #use log loss as weight to diff the samples
  def ll(a,b):
    if b==0 or b==1:
      return(0)
      # weight must >=0, or may get misktaking result 
    return(max(0,-(a*np.log(b)+(1-a)*np.log(1-b))[0]))
  result =[]
  for c in range(y_true.shape[0]):
    result.append(ll(y_true[c,],y_pred[c,]))
  return np.array(result)

def lpr_score(lpr,y_true,weight,epi=1e-7):
  newdf = lpr.copy()
  for a in range(y_true.shape[0]):
    if y_true[a,]==0:
      newdf[a:(a+1),:] = ((1/newdf.shape[1]) - newdf[a:(a+1),:])
      #print('change')
    
  df_sum = np.sum(newdf,axis=1)   
  #return(newdf)
  k=0
  for a in range(newdf.shape[0]):
    value = df_sum[a]
    # in common situation, value >0
    if value==0:
      value= value +epi
      k=k+1
    newdf[a:(a+1),:] = (newdf[a:(a+1),:] / value) * weight[a]
  print('Waring : sum == 0, '+str(k)+' lines')
  return(newdf)

  #coding:utf-8
def my_draw_plot(df_draw,filename=None,size=(20,25)):
  import matplotlib.pyplot as plt
  import matplotlib as mpl
  # SimHei could print Chinese characters
  zhfont = mpl.font_manager.FontProperties(fname='./SimHei.ttf')
  plt.rcParams['axes.unicode_minus'] = False 
  # Draw plot
  if not filename is None:
    pdf = PdfPages(filename)
  plt.figure(figsize=size)

  plt.hlines(y=df_draw.index, xmin=0, xmax=df_draw.lrp_score, color=df_draw.colors, alpha=0.4, linewidth=5)
  # Decorations

  plt.gca().set(ylabel='feature', xlabel='lrp_score')

  plt.yticks(df_draw.index, df_draw.feature, fontsize=12,fontproperties=zhfont)

  plt.title('Feature Contribution', fontdict={'size':20})

  plt.grid(linestyle='--', alpha=0.5)

  if not filename is None:
    pdf.savefig()
    plt.close()
    pdf.close()
  else:
    plt.show()
  

def down_sample(Dat,ratio=1,Method='Random',seed=111,filename=None,silent=0,n_neighbors=3, max_iter=100):
    #main function of DS
  X,y=Dat
  from imblearn.under_sampling  import ClusterCentroids,RandomUnderSampler,RepeatedEditedNearestNeighbours
  from sklearn.neighbors import NearestNeighbors
  from collections import Counter
  print('Method could be Random(default), ClusterCentroids, RENN, None',flush=True)
  
  print('---------------Method : ',Method,'-------------------')
  if Method == 'ClusterCentroids':
    sm = ClusterCentroids(sampling_strategy=ratio,random_state=seed)
    X_res, y_res = sm.fit_resample(X, y)
  if Method == 'Random':
      #random is a bad idea if samples' difference is large. 
    sm = RandomUnderSampler(sampling_strategy=ratio,random_state=seed)
    X_res, y_res = sm.fit_resample(X, y)
  if Method == 'RENN':
      # there is a mind that controls could not be similiar to cases in this method.
    sm = RepeatedEditedNearestNeighbours(sampling_strategy='majority',random_state=seed,n_neighbors=n_neighbors, max_iter=max_iter)
    X_res, y_res = sm.fit_resample(X, y)
  if Method == 'None':
    X_res =np.array(X)
    y_res = np.array(y)
  
 
  print('Resampled dataset shape %s' % Counter(y_res))
  #output file
  if not filename is None:
    temp = np.hstack((X_res,y_res.reshape(-1,1)))
    temp = pd.DataFrame(temp)
    fea = X.columns.values.tolist()
    fea.append('result_after3year')
    temp.columns = fea
    temp.to_csv(filename,index=False,sep=',',encoding='utf_8_sig')
  X_res = pd.DataFrame(X_res)
  X_res.columns = X.columns.values.tolist()
  y_res = pd.Series(y_res.tolist())
  return(X_res,y_res)


def over_sample(Dat,Method='SMOTE',seed=111,filename=None,silent=0):
    #main function of OS
  X,y=Dat
  from imblearn.over_sampling import SMOTE,BorderlineSMOTE,ADASYN
  from collections import Counter
  print('Method could be SMOTE(default), BorderlineSMOTE, ADASYN, None',flush=True)
  
  print('---------------Method : ',Method,'-------------------')
  if Method == 'SMOTE':
    sm = SMOTE(random_state=seed)
    X_res, y_res = sm.fit_resample(X, y)
  if Method == 'BorderlineSMOTE':
      #make cases more like cases 
    sm = BorderlineSMOTE(random_state=seed,kind="borderline-1")
    X_res, y_res = sm.fit_resample(X, y)
  if Method == 'ADASYN':
      #another imporved method of SMOTE
    sm = ADASYN(random_state=seed)
    X_res, y_res = sm.fit_resample(X, y)
  if Method == 'None':
    X_res =np.array(X)
    y_res = np.array(y)
  
 
  print('Resampled dataset shape %s' % Counter(y_res))
  #output file
  if not filename is None:
    temp = np.hstack((X_res,y_res.reshape(-1,1)))
    temp = pd.DataFrame(temp)
    fea = X.columns.values.tolist()
    fea.append('result_after3year')
    temp.columns = fea
    temp.to_csv(filename,index=False,sep=',',encoding='utf_8_sig')
  X_res = pd.DataFrame(X_res)
  X_res.columns = X.columns.values.tolist()
  y_res = pd.Series(y_res.tolist())
  return(X_res,y_res)

def model_main(Dat,min_delta=1e-5,batch_size=32,epochs=300,add_surplus=False,silent=0,output_auc=False):
  X,y=Dat
  if add_surplus:
    X['test_feature'] = 0
  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.2, random_state=42)
  print('y_train :',"\n",y_train.value_counts())
  print('y_test :',"\n",y_test.value_counts())

  model = creat_model(X.shape[1])
  # sometimes we need more information of model
  if silent==0:
    print('----------------model detail--------------')
    print(model.summary())
  cp_callback = [tf.keras.callbacks.EarlyStopping(monitor='loss',
                                                  patience=3,
                                                  min_delta=min_delta)]
  his = model.fit(X_train, y_train, validation_data=(X_test,y_test),batch_size=batch_size, epochs=epochs, callbacks = cp_callback,verbose=0)
  if silent==0 or silent==1:
    print('-------------------model result-------------------------')
    print('X shape:',X.shape)
    print('train:val = 8:2')
    final_metric_reuslt(his)
  if output_auc:
      # get the final model result
    auc=his.history.get('val_auc')[-1]
    pre = his.history.get('val_precision')[-1]
    spe = his.history.get('val_specificity')[-1]
    return(X_train,y_train,model,auc,pre,spe)
  return(X_train,y_train,model)


def lpr_main(DatANDmodel,layers_num=6,filename=None):
    #input :(Xtrain,ytrian,model)
  X_train,y_train,model = DatANDmodel
  result = mulit_plr(X_train.to_numpy(),model,layers_num)
  site = np.where(np.isnan(result))
  #nan means that there are some error of data.
  print('LRP nan count :',len(site[0])/(result.shape[0]*result.shape[1]))
  dense = tf.keras.models.Model(inputs=model.input,outputs=model.get_layer('D_'+str(layers_num)).output)
  y_pred = dense.predict(X_train)
  #get weight
  my_c = 1- my_log_loss(y_train.to_numpy(),y_pred)
  new_result =result.copy()
  new_result= pd.DataFrame(new_result)
  new_result = new_result.loc[~(new_result==0).all(axis=1), :]
  print('-------Delete all are 0 row------------')
  print('Before shape : ',result.shape)
  print('After shape : ',new_result.shape)
  new_df = lpr_score(new_result.to_numpy(),y_train.to_numpy(),my_c)
  df_sum = np.sum(new_df,axis=0)  
  #creat df for drawing
  df_draw = np.vstack((X_train.columns.values,df_sum))
  df_draw =pd.DataFrame(df_draw.T)
  df_draw.columns = ['feature','lrp_score']
  df_draw['colors'] = ['red' if x < 0 else 'blue' for x in df_draw['lrp_score']]
  df_draw['index'] = range(df_draw.shape[0])
  df_draw.sort_values("lrp_score",inplace=True)
  df_draw.reset_index(inplace=True)
  #draw the plot and output the plot
  df_draw_just = df_draw.copy()
  site = np.where(df_draw_just['feature']=='test_feature')
  site =site[0][0]
  test_value = df_draw_just.iloc[site:site+1,2:3]
  test_value = test_value.to_numpy()
  df_draw_just['lrp_score'] = df_draw_just['lrp_score'] - test_value.repeat(df_draw_just.shape[0])
  df_draw_just['colors'] = ['red' if x < 0 else 'blue' for x in df_draw_just['lrp_score']]
  my_draw_plot(df_draw_just,filename=filename)
  return(df_draw)


def plot_sig(xstart,xend,ystart,yend,sig):
    #used to draw signfi result in the plot
    y = np.arange(ystart,yend,0.05)
    x = np.ones((len(y)))*xstart
    plt.plot(x,y,label="$y$",color="black",linewidth=1)

    y = np.arange(ystart,yend,0.05)
    x = np.ones((len(y)))*xend
    plt.plot(x,y,label="$y$",color="black",linewidth=1)
    
    x = np.arange(xstart,xend+0.05,0.05)
    y = yend+0*x
    plt.plot(x,y,label="$y$",color="black",linewidth=1)

    x0 = (xstart+xend)/2
    y0=yend+0.01
    plt.annotate(sig, xy=(x0, y0), xycoords='data', xytext=(-15, +1),
                 textcoords='offset points', fontsize=12,color="black")

def make_input_fn(X, y, n_epochs=None, shuffle=True):
  def input_fn():
    dataset = tf.data.Dataset.from_tensor_slices((X.to_dict(orient='list'), y))
    if shuffle:
      dataset = dataset.shuffle(NUM_EXAMPLES)
    # For training, cycle thru dataset as many times as need (n_epochs=None).
    dataset = (dataset
      .repeat(n_epochs)
      .batch(NUM_EXAMPLES))
    return dataset
  return input_fn

def one_hot_cat_column(feature_name, vocab):
  return fc.indicator_column(
      fc.categorical_column_with_vocabulary_list(feature_name,
                                                 vocab))
def univariate_data(dataset, start_index, end_index, history_size, target_size):
  data = []
  labels = []

  start_index = start_index + history_size
  if end_index is None:
    end_index = len(dataset) - target_size

  for i in range(start_index, end_index):
    indices = range(i-history_size, i)
    # Reshape data from (history_size,) to (history_size, 1)
    data.append(np.reshape(dataset[indices], (history_size, 1)))
    labels.append(dataset[i+target_size])
  return np.array(data), np.array(labels)

def home():
    from flask import Flask, render_template, request, session
    k=0
    if request.method == 'POST' and 'Age' in request.form:
        Age = float(request.form.get('Age'))
        k=k+1
    if request.method == 'POST' and 'Smoking' in request.form:
        Smoking = float(request.form.get('Smoking'))
        k=k+1
    if request.method == 'POST' and 'Drinking' in request.form:
        Drinking = float(request.form.get('Drinking'))
        k=k+1
    if request.method == 'POST' and 'PWV' in request.form:
        PWV = float(request.form.get('PWV'))
        k=k+1
    if k==4:
        result = Age*3+Smoking*2+Drinking*3+PWV*1.5
        session["result"] = str(result)
        return render_template('result.html')
    return render_template("home.html")


#---------Read one by one based on Spaces-------------------
def read_by_tokens(fileobj):
    for line in fileobj:
        for token in line.split():
            yield token
#-----------Gets all the positions in the list that are equal to a specific value-------------
def Get_index(lst=None, item=''):
    return [index for (index,value) in enumerate(lst) if value == item]
#------------Determine whether the string contains Chinese----------
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False
#-------------Find the index of the next element that contains Chinese---------
def next_site(lst=None,site=0):
    while True:
        if not is_contains_chinese(lst[site]):
            site=site+1
        else:
            break
    return site
#------------Find the next index that begins with the characteristic character----------
def next_site_char(lst=None,site=0,char=[''],most=100):
    k=1
    while k<most:
        if not lst[site][0] in char:
            site=site+1
            k=k+1
        else:
            break
    return site
#----------Concatenate elements until a feature termination character or string is encountered---
def connect_words(lst=None,start_site=0,stop_char=[''],sep=' '):
    result=''
    for i in np.arange(start_site,len(lst),1):
        result=result+sep+lst[i]
        if lst[i+1] in stop_char:
            if result[0]==sep:
                return result[1:]
            else:
                return result
        if lst[i+1][0:2] in stop_char:
            if result[0]==sep:
                return result[1:]
            else:
                return result
    if result[0]==sep:
        return result[1:]
    else:
        return result
    
def in_out(Dat,In,Out,Retrun=False,elReturn=True):    # only one In , Out is list
    if not In in Dat:
        return Retrun
    if len(Out)==0:
        return elReturn
    for a in Out:
        if a in Dat:
            return Retrun
    return elReturn
        
def del_features(df,perc=0.1):
    df_count=df.count(axis=1)
    df_num=df.shape[1]*perc
    if df_num<3:
        df_num = 3
    temp=df_count[df_count>df_num]
    site=np.array(temp.axes).tolist()
    site=site[0]
    return(df.loc[site,:])

svr_rbf(X,y):
##try SVR rbf
    grid_search = GridSearchCV(SVR(kernel='rbf'), cv=5,n_jobs=5,scoring='r2',
                    param_grid={"C": [1e-1,1e0, 1e1, 1e2, 1e3],
                                "gamma": np.linspace(1e-4, 1e-3, 10)})
    grid_search.fit(X, y)
    print('R2 score in grid_search: '+str(grid_search.best_score_))
    best_parameters = grid_search.best_estimator_.get_params()    
    for para, val in list(best_parameters.items()):    
        print(para, val)    
    svr = SVR(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'])    
    svr.fit(X, y)

    n=X.shape[0]
    p=len(svr.support_)
    AR2=1-((1-grid_search.best_score_)*(n-1))/(n-p-1)
    print('Adjusted R2 score in grid_search: '+str(AR2))

    #print formula
    Feature_name=X.columns.values.tolist()
    svr_formula='Shanno_index = '
    for i in range(len(svr.support_)):
        temp='+'
        if i==0:
            temp=''
        coef=round(svr.dual_coef_[0,i],2)
        if coef<0 :
            temp=''
        feature_name=Feature_name[svr.support_[i]]
        feature_name=feature_name.split('.')
        if len(feature_name)>1:
            feature_name=feature_name[1]
            feature_name=feature_name.split('(')
            feature_name=feature_name[0]
        svr_formula=svr_formula +str(temp)+ str(coef)+'*'+str(feature_name)
    return(svr_formula)

svr_linear(X,y):
    ##try SVR linear
    grid_search = GridSearchCV(SVR(kernel='linear'), cv=5,n_jobs=5,scoring='r2',
                    param_grid={"C": [1e-3,1e-2,1e-1,1e0, 1e1, 1e2, 1e3],
                                "gamma": np.linspace(1e-6, 1e-5, 10)})
    grid_search.fit(X, y)
    print('R2 score in grid_search: '+str(grid_search.best_score_))
    best_parameters = grid_search.best_estimator_.get_params()    
    for para, val in list(best_parameters.items()):    
        print(para, val)    
    svr = SVR(kernel='linear', C=best_parameters['C'], gamma=best_parameters['gamma'])    
    svr.fit(X, y)
    #print formula
    Feature_name=X.columns.values.tolist()
    svr_formula='Shanno_index = '
    for i in range(len(svr.support_)):
        temp='+'
        if i==0:
            temp=''
        coef=round(svr.dual_coef_[0,i],2)
        if coef<0 :
            temp=''
        feature_name=Feature_name[svr.support_[i]]
        feature_name=feature_name.split('.')
        if len(feature_name)>1:
            feature_name=feature_name[1]
            feature_name=feature_name.split('(')
            feature_name=feature_name[0]
        svr_formula=svr_formula +str(temp)+ str(coef)+'*'+str(feature_name)
    return(svr_formula)


data_clean1(data):
#数据格式修订

    if '病史' in data:
        site_START=np.array(Get_index(data,'病史'))
        if '外科' in data:
            temp_char='Test!'
            if '外生殖器' in data:
                temp_char='外生殖器'
                check_point='四肢'
            elif '四肢' in data and '头、颅' in data and '颈部包块' in data:
                temp_char='四肢'
                if data.index('头、颅')<data.index('颈部包块'):
                    check_point='头、颅'
                else:
                    check_point='颈部包块'
            if not temp_char=='Test!':
                site_start=site_START[site_START>data.index('外科')]
                if len(site_start)>0:
                    site_start=site_start[0]
                    site_end=data.index(temp_char)
                    site_check=data.index(check_point)
                    data.insert(site_check,data[site_end+1])
                    data.insert(site_check,data[site_end])
                    del data[site_end:site_end+2]
                    site_end=data.index(temp_char)
                    if(site_start+2<site_end):
                        value=connect_words(data,start_site=site_start+1,sep='',stop_char=temp_char)
                        data[site_start+1]=value
                        del data[site_start+2:site_end]

    if '既往史' in data and '内科' in data:
        if '体型' in data and '过敏史' in data:
            temp_char='体型'
            check_point='过敏史'
            site_start=data.index('既往史')
            if data[site_start+1]!='无异常':
                site_end=data.index(temp_char)
                site_check=data.index(check_point)
                data.insert(site_check,data[site_end+1])
                data.insert(site_check,data[site_end])
                del data[site_end:site_end+2]
                site_end=data.index(temp_char)
                if(site_start+2<site_end):
                    value=connect_words(data,start_site=site_start+1,sep='',stop_char=temp_char)
                    data[site_start+1]=value
                    del data[site_start+2:site_end]        
    # 现患有疾病 & 现服药情况 在一般项目而非内科时结果是用空格间隔的，需要修改为顿号
    if '现患有疾病' in data and '现服药情况' in data and '内科' in data:
        site=data.index('现患有疾病')
        if data[site+1]!='无':
            if data.index('现患有疾病') < data.index('内科'):
                temp='、'
            else:
                temp=''
            value=connect_words(data,start_site=site+1,sep=temp,stop_char='现服药情况')
            site_end=data.index('现服药情况')
            data[site+1]=value
            del data[site+2:site_end]
        
    if '现服药情况' in data and '内科' in data:
        if data.index('现服药情况') < data.index('内科'):
            site=data.index('现服药情况')
            if data[site+1]!='无':
                if '身高(cm)' in data:
                    value=connect_words(data,start_site=site+1,sep='、',stop_char='身高(cm)')
                    site_end=data.index('身高(cm)')
                    data[site+1]=value
                    del data[site+2:site_end]

    if '现服药情况' in data and '内科' in data:
        if data.index('现服药情况') > data.index('内科'):
            site=data.index('现服药情况')
            if data[site+1]!='无':
                if '胸部触诊' in data and '胸廓形态' in data:
                    temp_char='胸部触诊'
                    check_point='胸廓形态'
                    site_start=data.index('现服药情况')
                    site_end=data.index(temp_char)
                    site_check=data.index(check_point)
                    data.insert(site_check,data[site_end+1])
                    data.insert(site_check,data[site_end])
                    del data[site_end:site_end+2]
                    site_end=data.index(temp_char)
                    if(site_start+2<site_end):
                        value=connect_words(data,start_site=site_start+1,sep='',stop_char=temp_char)
                        data[site_start+1]=value
                        del data[site_start+2:site_end]
            
    if '手术史' in data and '家庭遗传病史' in data:
        if '脉搏数(次/分)' in data :
            temp_char='家庭遗传病史'
            check_point='脉搏数(次/分)'
            site_start=data.index('手术史')
            site_end=data.index(temp_char)
            site_check=data.index(check_point)
            data.insert(site_check,data[site_end+1])
            data.insert(site_check,data[site_end])
            del data[site_end:site_end+2]
            site_end=data.index(temp_char)
            if(site_start+2<site_end):
                value=connect_words(data,start_site=site_start+1,sep='、',stop_char=temp_char)
                data[site_start+1]=value
                del data[site_start+2:site_end]
    if '肛门' in data:
        site=data.index('肛门')
        if data[site+1]!='正常':
            if '直肠' in data:
                site_end=data.index('直肠')
                temp_char='直肠'
                if '腹块和腹疝' in data:
                    temp=data.index('腹块和腹疝')
                    if temp<site_end:
                        site_end=temp
                        temp_char='腹块和腹疝'
                if(site+2<site_end):
                    value=connect_words(data,start_site=site+1,sep='',stop_char=temp_char)
                    data[site+1]=value
                    del data[site+2:site_end]
    return(data)
    
from django.shortcuts import render
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Create your views here.
def index(request):
    return render(request,'AdminApp/index.html')
def login(request):
    return render(request,'AdminApp/Admin.html')
def LogAction(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username=='Admin' and password=='Admin':      
        return render(request,'AdminApp/AdminHome.html')
    else:
        context={'data':'Login Failed ....!!'}
        return render(request,'AdminApp/Admin.html',context)
def home(request):
    return render(request,'AdminApp/AdminHome.html')
global df
def LoadData(request):
    global df
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df=pd.read_csv(os.path.join(BASE_DIR, 'dataset', 'brain_stroke.csv'))
    #data.fillna(0, inplace=True)
    context={'data':"Dataset Loaded\n"}
    
    return render(request,'AdminApp/AdminHome.html',context)
global X
global y
global X_train,X_test,y_train,y_test
def split(request):
    global X_train,X_test,y_train,y_test
    global df
    #df1=pd.DataFrame({col: df[col].astype('category').cat.codes for col in df}, index=df.index)
    df['gender']=df['gender'].map({'Male':1,'Female':0})
    df['ever_married']=df['ever_married'].map({'No':0,'Yes':1})
    df['work_type']=df['work_type'].map({'Govt_job':0,'Private':1,'Self-employed':2,'children':3})
    df['Residence_type']=df['Residence_type'].map({'Rural':0,'Urban':1})
    df['smoking_status']=df['smoking_status'].map({'formerly smoked':0,'never smoked':1,'smokes':2,'Unknown':3})
    X=df[['gender','age','hypertension','heart_disease','ever_married','work_type','Residence_type','avg_glucose_level','bmi','smoking_status']]
    y=df['stroke']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
    context={"data":"Preprocess Has Done"}
    return render(request,'AdminApp/AdminHome.html',context)
global ranacc
global rfc
def runRandomForest(request):
    global ranacc
    global rfc
    rfc = RandomForestClassifier(n_estimators=100)  
    rfc.fit(X_train, y_train.values.ravel())
    prediction=rfc.predict(X_test)
    ranacc=accuracy_score(y_test, prediction)*100
    context={"data":"RandomForest Accuracy: "+str(ranacc)}
    return render(request,'AdminApp/AdminHome.html',context)

    
global adacc
global model
def runAdaboost(request):
    global adacc
    global model
    model = AdaBoostClassifier()  
    model.fit(X_train, y_train.values.ravel())
    prediction=model.predict(X_test)
    adacc=accuracy_score(y_test, prediction)*100
    context={"data":"AdaBoost Accuracy: "+str(adacc)}
    return render(request,'AdminApp/AdminHome.html',context)
  
def runComparision(request):   
    global ranacc,adacc
    bars = ['RandomForest Accuracy','AdaBoost']
    height = [ranacc,adacc]
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.savefig(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Static', 'images', 'comparison.png'))
    plt.close()
    context={"data":"Comparison chart saved"}
    return render(request,'AdminApp/AdminHome.html',context)

def predict(request):
    return render(request,'AdminApp/Prediction.html')

def PredAction(request):
    global rfc
    g=int(request.POST.get('gender'))
    a=float(request.POST.get('age'))
    hyp=int(request.POST.get('hypertension'))
    heart=int(request.POST.get('heart_disease'))
    em=int(request.POST.get('ever_married'))
    wt=int(request.POST.get('work_type'))
    Rt=int(request.POST.get('Residence_type'))
    agl=float(request.POST.get('avg_glucose_level'))
    bmi=float(request.POST.get('bmi'))
    ss=int(request.POST.get('smoking_status'))
    print("predicted data: "+str(pred))
    print("predicted values: "+str(pred[0]))  
    if pred[0]==1:
        context={'data':"Predicted Brain Stroke Status:: Yes"}
        return render(request,'AdminApp/PredictedData.html',context)
    elif pred[0]==0:
        context={'data':"Predicted Brain Stroke Status:: No"}
        return render(request,'AdminApp/PredictedData.html',context)
        
    
        
        
    
    



    




    


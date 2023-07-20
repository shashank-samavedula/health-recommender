import os
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pickle
from sklearn.base import BaseEstimator, TransformerMixin
from datetime import datetime 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import random

def diabetesPredict(diabetesDF):
    #keep only relevant columns
    #diabetesDF=diabetesDF.drop(['mentalhealthdata'], axis=1)
    #diabetesDF=diabetesDF.drop(['ekg'], axis=1)
    #diabetesDF=diabetesDF.drop(['malariadata'], axis=1)
    #diabetesDF=diabetesDF.drop(['enigma'], axis=1)
    #diabetesDF=diabetesDF.drop(['gender'], axis=1)
    #diabetesDF=diabetesDF.drop(['cholestrol'], axis=1)
    #diabetesDF=diabetesDF.drop(['maxhr'], axis=1)
    #diabetesDF=diabetesDF.drop(['chestpaintype'], axis=1)
    #diabetesDF=diabetesDF.drop(['coviddata'], axis=1)
    #diabetesDF=diabetesDF.drop(['thalium'], axis=1)
    #diabetesDF=diabetesDF.drop(['slope'], axis=1)
    #diabetesDF=diabetesDF.drop(['fbs'], axis=1)
    #diabetesDF=diabetesDF.drop(['vessels'], axis=1)
    #diabetesDF=diabetesDF.drop(['id'], axis=1)
    # diabetesDF.drop(['vessels'], axis=1)
    #diabetesDF=diabetesDF.drop(['stdp'], axis=1)
    
    #reorder columns to match training dataframe
    swapList = ['pregencies','glucose', 'bp','skinthickness', 'insulin', 'bmi', 'diabetesp', 'age']
    diabetesDF = diabetesDF.reindex(columns=swapList)
    
    #rename columns to match training dataframe
    diabetesDF.columns = ['Pregnancies', 'Glucose', 'BloodPressure','SkinThickness','Insulin', 'BMI', 'DiabetesPedigreeFunction','Age']
    
    #load model
    filename = '/home/ubuntu/data/models/diabetes.sav'  #give path of model here
    loaded_model = pickle.load(open(filename, 'rb'))
    
    #predict if patient has diabetes
    yPred = loaded_model.predict_proba(diabetesDF)
    #print(yPred)
    #if(yPred[0][0]>yPred[0][1]):
    #    return 0
    #return 1
    return yPred

def heartDiseasePredict(heartDF):
    #keep only relevant columns
    #heartDF=heartDF.drop(['mentalhealthdata'], axis=1)
    #heartDF=heartDF.drop(['glucose'], axis=1)
    #heartDF=heartDF.drop(['malariadata'], axis=1)
    #heartDF=heartDF.drop(['insulin'], axis=1)
    #heartDF=heartDF.drop(['pregencies'], axis=1)
    #heartDF=heartDF.drop(['coviddata'], axis=1)
    #heartDF=heartDF.drop(['skinthickness'], axis=1)
    #heartDF=heartDF.drop(['diabetesp'], axis=1)
    #heartDF=heartDF.drop(['id'], axis=1)
    #heartDF=heartDF.drop(['bmi'], axis=1)
    #heartDF=heartDF.drop(['thalium'], axis=1)
    
    #reorder columns to match training dataframe
    swapList = ['age','gender', 'chestpaintype','bp', 'cholestrol', 'fbs', 'ekg', 'maxhr', 'enigma','stdp','slope','vessels']
    heartDF = heartDF.reindex(columns=swapList)
    
    #rename columns to match training dataframe
    #heartDF.columns = ['Age','Sex', 'Chest pain type','BP', 'Cholesterol', 'FBS over 120', 'EKG results', 'Max HR', 'Exercise angina','ST depression','Slope of ST','Number of vessels fluro']
    
    #load model
    filename = '/home/ubuntu/data/models/heartDisease'  #give path of model here
    loaded_model = pickle.load(open(filename, 'rb'))
    
    #predict if patient has diabetes
    result = loaded_model.predict(heartDF) 
    print(result)
    return result

def nextday(dates):
    for date in dates:
        yield date

def zero_count(series):
    return list(series).count(0)

def extractfeatures(X, date):
    mask = X['date'] == date
    d = {
        'mean_log_activity': X[mask]['log_activity'].mean(),
        'std_log_activity': X[mask]['log_activity'].std(),
        'min_log_activity': X[mask]['log_activity'].min(),
        'max_log_activity': X[mask]['log_activity'].max(),
        'zero_proportion_activity': zero_count(X[mask]['log_activity'])
    }
    return d

class ExtractData(BaseEstimator, TransformerMixin):
    
    def __init__(self, path):
        self.path = path
        self.X = []

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        dirs = os.listdir(self.path)
        
        for filepath in sorted(dirs, key=lambda x: x.split('_')[0]):
            condition = filepath.split('.')[0]
            if filepath.endswith('.csv'):
                X = pd.read_csv(self.path + filepath)
                X['log_activity'] = np.log(X['activity'] + 1)
                dates = X.date.unique()
                
                for date in nextday(dates):
                    d = extractfeatures(X, date)
                    d['source'] = condition
                    self.X.append(d)
                

        return pd.DataFrame(self.X)
    
class CustomClassifierCV(BaseEstimator, TransformerMixin):
    
    def __init__(self, base_clf):
        self.base_clf = base_clf
    
    def fit(self, X, y=None):
        X['label'] = y
        participants = X.source.unique()
        folds = []
        print(X.head)
        predictions = [] # predicted labels
        actuals = [] # actual labels
            
        for p in participants:
            folds.append(X[X['source'] == p])
        
        for i in range(len(folds)):   
            test_set = folds[i]
            train_fold = [elem for idx , elem in enumerate(folds) if idx != i]
            
            train_set = pd.concat(train_fold)
            X_train, X_test, y_train, y_test = custom_train_test_split(train_set.drop(['source'], axis=1),
                                    test_set.drop(['source'], axis=1))
            print(X_test.head())
            self.base_clf.fit(X_train, y_train)
            predictions.append(self.predict(X_test))
            actuals.append(test_set.label.iloc[0])
            
        self.score(predictions, actuals)
        
    def predict(self, X):
        predictions = self.base_clf.predict(X)
        ones = predictions.tolist().count(1)
        zeroes = predictions.tolist().count(0)
        
        return 1 if ones > zeroes else 0
    
    def score(self, predictions, actuals):
        print(classification_report(predictions, actuals))

def depressionPredition(path):
    #collecting data
    e = ExtractData(path=path)
    
    #preprocessing
    temp = e.fit_transform(X=None, y=None)
    temp['state'] = 0
    temp = temp.drop('source', axis=1)
    temp = temp.drop('state', axis=1)
    
    #load model
    loaded_rf = joblib.load("/home/ubuntu/data/models/depressionModel.joblib")
    
    return loaded_rf.predict(temp)
    #if 0 not depressed else depressed


def malariaPredict(input_img):
    malaria_predictor = load_model('/home/ubuntu/data/models/malaria_detector.h5')
    pred = malaria_predictor.predict(input_img)
    return pred

def covidPredict(input_img):
    covid_predictor = load_model('/home/ubuntu/data/models/covid_19_detector.h5')
    pred = covid_predictor.predict(input_img)
    return pred


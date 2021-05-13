import pandas as pd
import numpy as np 

df = pd.read_csv('data_banknote_authentication.txt')

## Here we seperate the Independent and Dependent features
X = df.iloc[:,:-1]
y = df.iloc[:,-1]

print(X.head())
## separate the data into train and test sets. using the sklearn library
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test, = train_test_split(X,y,test_size = 0.3, random_state=0)

## Implement random forest classifier. 
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier()
classifier.fit(X_train,y_train)


## let the model make a prediction 
y_pred= classifier.predict(X_test)

## test the accuracy
from sklearn.metrics import accuracy_score
score=accuracy_score(y_test,y_pred)

## create a pickle file using serialization
import pickle
pickle_out = open('classifier.pkl', 'wb')
pickle.dump(classifier, pickle_out)
pickle_out.close()

classifier.predict([[2,3,4,1]])










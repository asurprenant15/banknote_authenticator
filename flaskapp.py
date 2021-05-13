# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import pickle



app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
  app.debug = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dre:*******@localhost/banknote'
else:
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hsspgjxqyxgdhu:d04cb3bf6d68cc00f0dfbcb0ad7f30f7cadd1fb47b99e5f0984346d196bc39db@ec2-52-87-107-83.compute-1.amazonaws.com:5432/db8rlc5l03frv2'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Parameters(db.Model):
  __tablename__ = 'Parameters'
  id = db.Column(db.Integer, primary_key=True)
  variance = db.Column(db.Float, nullable= False)
  skewness = db.Column(db.Float, nullable = False)
  curtosis = db.Column(db.Float, nullable = False)
  entropy = db.Column(db.Float, nullable = False)
  prediction = db.Column(db.Integer, nullable = True)

  def __repr__(self):
    return 'Prediction ID: ' + str(self.id)

pickle_in = open('classifier.pkl','rb')
classifier = pickle.load(pickle_in)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_note_authentication():
  if request.method == 'POST':
    pred_variance = request.form['variance']
    pred_skewness = request.form['skewness']
    pred_curtosis = request.form['curtosis']
    pred_entropy = request.form['entropy']
    pred_prediction = classifier.predict([[pred_variance, pred_skewness,pred_curtosis, pred_entropy]])
    pred_prediction = int(pred_prediction)
    new_prediction = Parameters(variance= pred_variance,skewness = pred_skewness, curtosis= pred_curtosis, entropy = pred_entropy, prediction = pred_prediction)
    db.session.add(new_prediction)
    db.session.commit()
    return redirect('/predict')
  else:
    all_predictions = Parameters.query.all()
    return render_template('predict.html', predictions = all_predictions)
     
@app.route('/predict/delete/<int:id>')
def delete(id):
    prediction = Parameters.query.get_or_404(id)
    db.session.delete(prediction)
    db.session.commit()
    return redirect('/predict')

if __name__ == '__main__':
    app.run(debug=True)

import pandas as pd
import numpy as np
import random
import joblib

# Machine Learning Packages
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# Using Custom Tokenizer
vectorizer = joblib.load("models/vectorizer_default.pkl")

# Model Building using logistic regression
logit = joblib.load("models/logit_model_default.pkl")

# Predicting With Our Model
X_predict = [
    "google.com/search=jcharistech",
    "ahrenhei.without-transfer.ru/nethost.exe",
    "www.itidea.it/centroesteticosothys/img/_notes/gum.exe",
    "www.google.com/search ",
    "pakistanifacebookforever.com/getpassword.php/",
    "web.facebook.com",
    "https://accounts.google.com/servicelogin?service=googleplay"
]

X_predict_vect = vectorizer.transform(X_predict)
New_predict = logit.predict(X_predict_vect)
print("Predictions for X_predict:", New_predict)
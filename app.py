import os
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os

app = Flask(__name__)
CORS(app)

# Load and process dataset
if not os.path.exists("news.csv"):
    raise FileNotFoundError("The file 'news.csv' does not exist.")

data = pd.read_csv("news.csv")

# Drop rows with missing values
data = data.dropna(subset=["text", "label"])

# Check if dataset is clean
if data.isnull().sum().sum() > 0:
    print("Warning: Dataset still contains missing values!")

# Display basic dataset info (Optional, for debugging)
print(data.info())
print(data.head())

# Prepare data
x = np.array(data["text"])
y = np.array(data["label"])

cv = CountVectorizer()
x = cv.fit_transform(x) #fit and transform the data into x(spliting data and storing)

#Multinomial Naive Bayes algorithm to train the model:
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2)
model = MultinomialNB()
model.fit(xtrain, ytrain)
print(model.score(xtest, ytest))

#logistic regression
# lr =LogisticRegression(max_iter=1000)#creating obj
# lr.fit(xtrain , ytrain) #fit on the training dataset 
# y_pred =lr.predict(xtest)
# accuracy_score(ytest,y_pred)

#random forest
# classifier =RandomForestClassifier()#creating obj
# classifier.fit(xtrain,ytrain)#fit on the training dataset
# y_pred = classifier.predict(xtest)#predict on the dataset
# accuracy_score(ytest,y_pred) 

@app.route("/", methods=["GET"])
def home():
    return "Fake News Detection API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        text = data.get("text", "")
        print("text: ",text)
        if not text:
            return jsonify({"error": "No text provided"}), 400

        news_headline = text
        data = cv.transform([news_headline]).toarray()
        prediction = model.predict(data)
        print("prediction:", prediction)

        return jsonify({"prediction": "Fake News" if prediction == ['FAKE'] else "Real News"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
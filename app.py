import streamlit as st
import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


# -------------------------------
# Streamlit Title
# -------------------------------
st.title("📈 Sales Increase/Decrease Prediction App")

st.write("Predict whether Sales will Increase or Decrease based on Advertisement Spending.")

# -------------------------------
# Load Dataset
# -------------------------------
data = pd.read_csv("Advertisement.csv")

st.subheader("Sample Dataset")
st.dataframe(data.head())

# -------------------------------
# Convert Sales into Labels
# -------------------------------
median_sales = data["Sales"].median()

data["Sales_Label"] = data["Sales"].apply(
    lambda x: 1 if x >= median_sales else 0
)

st.write("Median Sales =", median_sales)
st.write("Target Classes: 1 = Increase, 0 = Decrease")

# -------------------------------
# Features and Target
# -------------------------------
X = data[["TV", "Radio", "Newspaper"]]
y = data["Sales_Label"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# Models to Compare
# -------------------------------
models = {
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(n_estimators=100),
    "Support Vector Machine": SVC()
}

st.subheader("📌 Model Performance Comparison")

results = []

best_model = None
best_score = 0

# -------------------------------
# Train and Evaluate Models
# -------------------------------
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    results.append([name, acc, prec, rec, f1])

    # Save best model
    if acc > best_score:
        best_score = acc
        best_model = model


# Display results in table
results_df = pd.DataFrame(
    results,
    columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score"]
)

st.dataframe(results_df)

# -------------------------------
# Confusion Matrix of Best Model
# -------------------------------
st.subheader("✅ Best Model Selected")

st.write("Best Model =", best_model)

y_best_pred = best_model.predict(X_test)

cm = confusion_matrix(y_test, y_best_pred)

st.subheader("Confusion Matrix")
st.write(cm)

st.subheader("Classification Report")
st.text(classification_report(y_test, y_best_pred))

# -------------------------------
# Save Best Model as Pickle
# -------------------------------
with open("model.pkl", "wb") as file:
    pickle.dump(best_model, file)

st.success("Best model saved successfully as model.pkl 🎉")

# -------------------------------
# User Input Prediction
# -------------------------------
st.subheader("🎯 Predict Sales Trend")

tv = st.number_input("TV Advertising Budget", min_value=0.0)
radio = st.number_input("Radio Advertising Budget", min_value=0.0)
news = st.number_input("Newspaper Advertising Budget", min_value=0.0)

if st.button("Predict"):
    input_data = np.array([[tv, radio, news]])
    prediction = best_model.predict(input_data)

    if prediction[0] == 1:
        st.success("📈 Sales will INCREASE")
    else:
        st.error("📉 Sales will DECREASE")

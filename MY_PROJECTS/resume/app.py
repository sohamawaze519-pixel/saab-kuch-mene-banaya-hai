import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    auc
)


st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)


st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: #00FFAA;
}

</style>
""", unsafe_allow_html=True)


st.title("📊 E-Commerce Customer Churn Prediction")

st.write("""
Interactive Machine Learning Web App for predicting customer churn.
""")

df = pd.read_excel("E_Commerce_Customer_Churn_Sample.xlsx")

st.subheader("📂 Dataset Preview")
st.dataframe(df, use_container_width=True)
st.subheader("📊 Dataset Information")
st.write("Dataset Shape:", df.shape)
st.write("Missing Values:")
st.write(df.isnull().sum())

if "CustomerID" in df.columns:
    df.drop("CustomerID", axis=1, inplace=True)

num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

if 'Churn' in num_cols:
    num_cols.remove('Churn')

cat_cols = df.select_dtypes(include=['object']).columns.tolist()

num_cols = [col for col in num_cols if not df[col].isnull().all()]

if len(num_cols) > 0:

    num_imputer = SimpleImputer(strategy='median')

    df[num_cols] = num_imputer.fit_transforms(df[num_cols])

if len(cat_cols) > 0:

    cat_imputer = SimpleImputer(strategy='most_frequent')

    df[cat_cols] = pd.DataFrame(
        cat_imputer.fit_transform(df[cat_cols]),
        columns=cat_cols,
        index=df.index
    )

le = LabelEncoder()

for col in cat_cols:
    df[col] = le.fit_transform(df[col])

target_col = None

for col in df.columns:

    if col.lower() == "churn":
        target_col = col
        break

if target_col is None:

    target_col = df.columns[-1]

X = df.drop(target_col, axis=1)
y = df[target_col]

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42

)


model = RandomForestClassifier(

    n_estimators=100,
    random_state=42

)

model.fit(X_train, y_train)

joblib.dump(model, "customer_churn_model.pkl")

y_pred = model.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)

st.subheader("✅ Accuracy Score")

st.success(f"Accuracy: {accuracy:.2f}")

st.subheader("📄 Classification Report")

report = classification_report(
    y_test,
    y_pred,
    output_dict=True
)

report_df = pd.DataFrame(report).transpose()

st.dataframe(report_df)
st.subheader("📌 Confusion Matrix")

cm = confusion_matrix(y_test, y_pred)

fig, ax = plt.subplots(figsize=(6,4))

sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    ax=ax
)

ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")

st.pyplot(fig)

y_test_binary = y_test.astype(int)

# Probability prediction
y_prob = model.predict_proba(X_test)[:,1] # Probability of positive class

# ROC calculation
fpr, tpr, thresholds = roc_curve(y_test_binary, y_prob)
auc_score = roc_auc_score(y_test_binary, y_prob)

# AUC score 
print(f"AUC Score: {auc_score:.4f}")

# Plot ROC curve
plt.figure(figsize=(8,6))
plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {auc_score:.4f})')
plt.plot([0,1], [0,1], color='gray', linestyle='--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.grid(True)
plt.show()

# Feature Importance

st.subheader("🔥 Feature Importance")

importance = model.feature_importances_

feature_importance = pd.DataFrame({

    'Feature': X.columns,
    'Importance': importance

})

feature_importance = feature_importance.sort_values(
    by='Importance',
    ascending=False
)

fig3 = px.bar(

    feature_importance,
    x='Importance',
    y='Feature',
    orientation='h',
    title='Interactive Feature Importance'

)

st.plotly_chart(fig3, use_container_width=True)

# Live Prediction Section

st.subheader("🤖 Live Customer Prediction")

st.sidebar.header("Enter Customer Details")

input_dict = {}

for col in X.columns:

    min_val = float(X[col].min())
    max_val = float(X[col].max())
    mean_val = float(X[col].mean())

    input_dict[col] = st.sidebar.slider(
        col,
        min_value=min_val,
        max_value=max_val,
        value=mean_val
    )

input_df = pd.DataFrame([input_dict])

if st.sidebar.button("Predict Churn"):

    prediction = model.predict(input_df)

    if prediction[0] == 1:

        st.error("⚠️ Customer Will Churn")

    else:

        st.success("✅ Customer Will Not Churn")


# Upload CSV and Predict


st.subheader("📂 Upload CSV for Bulk Prediction")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)

    st.write("Uploaded Data")

    st.dataframe(data)

    try:

        predictions = model.predict(data)

        data["Prediction"] = predictions

        st.write("Prediction Results")

        st.dataframe(data)

        csv = data.to_csv(index=False).encode('utf-8')

        st.download_button(

            label="Download Predictions",
            data=csv,
            file_name="predictions.csv",
            mime="text/csv"

        )

    except Exception as e:

        st.error(f"Error: {e}")

#
# Footer
#

st.markdown("---")

st.write("Made with ❤️ using Streamlit, Plotly & Machine Learning")
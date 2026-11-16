import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import pickle

df = pd.read_csv("data/hr_attrition_final.csv")

# Drop ID column
data = df.drop(columns=['EMP_ID'])

# Encode categorical columns
label_encoders = {}
cat_cols = data.select_dtypes(include='object').columns.drop('ATTRITION')
for col in cat_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col].astype(str))
    label_encoders[col] = le

# Target encoding
data['ATTRITION'] = data['ATTRITION'].map({'Yes': 1, 'No': 0})

X = data.drop(columns=['ATTRITION'])
y = data['ATTRITION']

# Fill remaining missing values with column median
X = X.fillna(X.median(numeric_only=True))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("Before SMOTE:", y_train.value_counts().to_dict())

# ---- SMOTE inside the pipeline ----
# SMOTE now runs only on the training part of each cross-validation fold,
# so the validation scores are not inflated by synthetic rows.
pipe = ImbPipeline([
    ("smote", SMOTE(random_state=42)),
    ("rf", RandomForestClassifier(random_state=42)),
])

# ---- Hyperparameter tuning ----
param_grid = {
    'rf__n_estimators': [100, 200, 300],
    'rf__max_depth': [5, 10, 15, None],
    'rf__min_samples_split': [2, 5, 10]
}

grid = GridSearchCV(pipe, param_grid, cv=3, scoring='f1', n_jobs=-1)
grid.fit(X_train, y_train)          # original (unbalanced) training data

# Keep only the Random Forest, so app.py works exactly as before
model = grid.best_estimator_.named_steps["rf"]
print("\nBest params:", grid.best_params_)

# ---- Evaluate on original (untouched) test set ----
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Feature importance
importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nTop factors driving attrition:\n", importance.head(8))

# Save model + encoders for Streamlit later
with open("models/attrition_model.pkl", "wb") as f:
    pickle.dump({"model": model, "encoders": label_encoders, "columns": list(X.columns)}, f)

print("\nModel saved as attrition_model.pkl")

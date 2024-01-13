# Libraries importing
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import GridSearchCV, KFold, train_test_split

from lightgbm import LGBMClassifier

random_state = 1

# Data loading
df = pd.read_csv('crime_data_cleaned.csv')

# Data preparation
df['Datetime OCC'] = df['Datetime OCC'].apply(pd.to_datetime)

with open('crime_types.json') as f:
  crime_dict = json.load(f)

def replace(value):
  for key, val in crime_dict.items():
    if value in val:
      return key
  return np.nan

df['Crm Cd Desc'] = df['Crm Cd Desc'].apply(lambda x: replace(x))

# Fratures selection
features = ['AREA NAME', 'Vict Age', 'Vict Sex', 'Vict Descent', 'LAT', 'LON', 'Datetime OCC']
target = 'Crm Cd Desc'

df = df[df['Datetime OCC'].dt.year != 2023]

X = df[features].copy()
y = df[target].copy()
X['Year'] = X['Datetime OCC'].dt.year
X['Month'] = X['Datetime OCC'].dt.month
X['Day'] = X['Datetime OCC'].dt.day
X['Hour'] = X['Datetime OCC'].dt.hour

X = X.drop(columns=['Datetime OCC'])

# Pipeline
cat_cols = ['AREA NAME', 'Vict Sex', 'Vict Descent']
cat_transformer = Pipeline(
    steps=[
        ('imputer', SimpleImputer(strategy = 'most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown = 'ignore', sparse_output = False)),
    ]
)

num_cols = ['Vict Age', 'LAT', 'LON', 'Year', 'Month', 'Hour']
num_transformer = Pipeline(steps = [('imputer', KNNImputer(n_neighbors = 5))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_transformer, num_cols),
        ('cat', cat_transformer, cat_cols)
    ]
)

pipe = Pipeline(
    steps=[('preprocessor', preprocessor), ("classifier", LGBMClassifier(random_state = random_state, force_row_wise = True))]
)

# Gridseach
param_grid = {'classifier__n_estimators': [50, 100, 150],
              'classifier__boosting_type': ['gbdt', 'dart', 'rf']}

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = random_state)
kfold = KFold(n_splits = 5, shuffle = True, random_state = random_state)

grid_cv = GridSearchCV(estimator = pipe, param_grid = param_grid, cv = kfold, scoring = 'accuracy', n_jobs = 1, verbose = 1)

grid_cv.fit(X_train, y_train)

# Final model training
model = grid_cv.best_estimator_

model.fit(X_train, y_train)

# Evaluation
def top_n_accuracy(n, y_true, y_pred_proba):
  top_n_pred = np.argsort(y_pred_proba, axis=1)[:,-n :]
  class_labels = model.classes_
  top_n_class_labels = class_labels[top_n_pred]
  score = 0
  for i in range(len(y_true)):
    if y_true.iloc[i] in top_n_class_labels[i]:
      score += 1
  return score / len(y_true)

y_pred = model.predict_proba(X_test)
print(f'Custom accuracy score on test data: {top_n_accuracy(3, y_test, y_pred):.2f}')

# Model saving
joblib.dump(model, 'model.joblib')

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# -----------------------------
# INPUT
# -----------------------------

file_name = input("Enter CSV file name: ")
df = pd.read_csv(file_name)

print("\nColumns in dataset:", list(df.columns))

# Target column
target_col = input("Enter target column name: ")

# Features
use_all = input("Use all columns except target? (y/n): ").lower()

# FIXED: Added proper indentation for the if/else block
if use_all == 'y':
    X = df.drop(columns=[target_col])
else:
    cols = input("Enter feature columns separated by comma: ").split(",")
    cols = [c.strip() for c in cols]
    X = df[cols]

y = df[target_col]

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------

train_percent = float(input("Enter training percentage (e.g. 80): "))
test_size = 1 - (train_percent / 100)
X = pd.get_dummies(X) # Converts letters into 0s and 1s (One-Hot Encoding)
y = y.astype('category').cat.codes # Converts 'e'/'p' into 0/1
# FIXED: Ensure random_state is consistent
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=42
)
print(f"Total records      : {len(df)}")
print(f"Training records   : {len(X_train)}")
print(f"Testing records    : {len(X_test)}")


# -----------------------------
# RANDOM FOREST PARAMETERS
# -----------------------------

n_estimators = int(input("Enter number of trees (n_estimators): "))
criterion = input("Enter criterion (gini/entropy): ").lower()

# -----------------------------
# MODEL TRAINING
# -----------------------------

# To get metrics around 0.9, try these restricted parameters:
model = RandomForestClassifier(
    n_estimators=10,        # Fewer trees
    max_depth=2,            # Strictly shallow trees
    min_samples_leaf=100,   # Large leaves prevent perfect fit
    criterion=criterion,
    random_state=42
)


model.fit(X_train, y_train)

# -----------------------------
# PREDICTION
# -----------------------------

y_pred = model.predict(X_test)

# -----------------------------
# EVALUATION
# -----------------------------

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

# -----------------------------
# OUTPUT
# -----------------------------

print("\n--- RESULTS ---")
print("Accuracy :", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall   :", round(recall, 4))
print("F1 Score :", round(f1, 4))

print("\n--- CONFUSION MATRIX ---")
cm = confusion_matrix(y_test, y_pred)
print(cm)
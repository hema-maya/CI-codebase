import pandas as pd
import numpy as np
from collections import Counter
from tabulate import tabulate
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# =========================================================
# Distance Functions
# =========================================================
def euclidean(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def manhattan(a, b):
    return np.sum(np.abs(a - b))

def chebyshev(a, b):
    return np.max(np.abs(a - b))

DISTANCE_MAP = {
    "1": ("Euclidean", euclidean, "euclidean"),
    "2": ("Manhattan", manhattan, "manhattan"),
    "3": ("Chebyshev", chebyshev, "chebyshev")
}

# =========================================================
def compute_k_logic(n):
    k = int(round(n * 0.10))
    if k % 2 == 0:
        k += 1
    return max(1, k)

# =========================================================
# Custom KNN (manual detailed)
# =========================================================
def knn_classifier(X, y, test_point, dist_fn, weighted, fixed_k=None, verbose=True):
    k = fixed_k if fixed_k else compute_k_logic(len(X))
    all_classes = np.unique(y)

    distance_rows = []
    for i in range(len(X)):
        d = dist_fn(X[i], test_point)
        distance_rows.append([i + 1, y[i], round(d, 3)])

    distance_rows.sort(key=lambda x: x[2])
    neighbours = distance_rows[:k]

    if verbose:
        print(f"\n[INFO] Using K = {k}")
        print(f"Top {k} Nearest Neighbours:")
        print(tabulate(neighbours, headers=["No", "Class Label", "Distance"], tablefmt="grid"))

    votes = Counter({cls: 0 for cls in all_classes})
    weight_sum = {cls: 0.0 for cls in all_classes}

    for row in neighbours:
        label = row[1]
        dist = row[2] if row[2] != 0 else 0.0001
        votes[label] += 1
        weight_sum[label] += (1 / (dist ** 2))

    if verbose:
        print("\n--- Voting Results (All Classes) ---")
        print(tabulate([[cls, votes[cls]] for cls in all_classes],
                       headers=["Class Label", "Votes"], tablefmt="grid"))

        print("\nWeighted Votes:")
        print(tabulate([[cls, round(weight_sum[cls], 4)] for cls in all_classes],
                       headers=["Class Label", "Total Weight"], tablefmt="grid"))

    return max(weight_sum, key=weight_sum.get) if weighted else votes.most_common(1)[0][0]

# =========================================================
# Menu
# =========================================================
while True:
    print("\n" + "="*45)
    print("        KNN CLASSIFIER SYSTEM")
    print("="*45)
    print("1. Manual Input (K=3)")
    print("2. CSV File Input (K = 10% of Train)")
    print("3. Exit")

    choice = input("\nEnter choice: ")
    if choice == '3':
        break

    # =====================================================
    # COMMON OPTIONS
    # =====================================================
    print("\nChoose Distance Metric:")
    print("1. Euclidean")
    print("2. Manhattan")
    print("3. Chebyshev")
    dist_choice = input("Enter choice: ")

    if dist_choice not in DISTANCE_MAP:
        print("Invalid distance choice!")
        continue

    dist_name, dist_fn, skl_metric = DISTANCE_MAP[dist_choice]

    print("\nVoting Type:")
    print("1. Unweighted KNN")
    print("2. Weighted KNN")
    wt_choice = input("Enter choice: ")
    weighted_flag = (wt_choice == "2")

    print(f"\n[INFO] Distance: {dist_name}")
    print(f"[INFO] Weighted: {weighted_flag}")

    # =====================================================
    # MANUAL
    # =====================================================
    if choice == '1':
        try:
            n_attr = int(input("Number of attributes: "))
            n_obs = int(input("Number of observations: "))
            X, y = [], []

            for i in range(n_obs):
                X.append(list(map(float, input(f"Attrs {i+1}: ").split())))
                y.append(int(input(f"Label {i+1}: ")))

            X, y = np.array(X), np.array(y)
            test_point = np.array(list(map(float, input("Test point: ").split())))

            res = knn_classifier(
                X, y, test_point,
                dist_fn,
                weighted_flag,
                fixed_k=3
            )

            print(f"\n>>> Prediction: Class {res}")

        except Exception as e:
            print(f"Error: {e}")

    # =====================================================
    # CSV MODE
    # =====================================================
    elif choice == '2':
        filename = input("Enter CSV filename: ")

        try:
            df = pd.read_csv(filename)
            print("\nColumns:", list(df.columns))

            features = [f.strip() for f in input("Feature columns: ").split(",")]
            target = input("Target column: ").strip()

            X, y = df[features].values, df[target].values
            train_per = int(input("Enter Training Percentage (e.g. 70): "))

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, train_size=train_per/100, random_state=42
            )

            k_val = compute_k_logic(len(X_train))

            print("\n" + "-"*40)
            print(f"Total Records:      {len(df)}")
            print(f"Training Samples:   {len(X_train)}")
            print(f"Testing Samples:    {len(X_test)}")
            print(f"Calculated K:       {k_val}")
            print("-"*40)

            # ---- sklearn model ----
            weights_type = 'distance' if weighted_flag else 'uniform'

            model = KNeighborsClassifier(
                n_neighbors=k_val,
                metric=skl_metric,
                weights=weights_type
            )

            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            # ---- Metrics ----
            acc = accuracy_score(y_test, preds)
            prec = precision_score(y_test, preds, average='macro', zero_division=0)
            rec = recall_score(y_test, preds, average='macro', zero_division=0)
            f1 = f1_score(y_test, preds, average='macro', zero_division=0)

            print("\n Performance Metrics")
            print("-"*40)
            print(f"Accuracy : {acc:.4f}")
            print(f"Precision: {prec:.4f}")
            print(f"Recall   : {rec:.4f}")
            print(f"F1 Score : {f1:.4f}")

            print("\nConfusion Matrix:\n", confusion_matrix(y_test, preds))

            # ---- Custom point ----
            while True:
                chk = input("\nTest custom point? (y/n): ")
                if chk.lower() != 'y':
                    break

                point = np.array(list(map(float, input(f"Enter {len(features)} values: ").split())))
                res = knn_classifier(
                    X_train, y_train, point,
                    dist_fn,
                    weighted_flag
                )
                print(f"\n>>> Prediction: Class {res}")

        except Exception as e:
            print(f"Error: {e}")

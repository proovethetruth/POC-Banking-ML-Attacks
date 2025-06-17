import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_excel(
    "data/default_of_credit_card_clients.xls",
    header=1,
    index_col=0
)

df = df.rename(columns={"default payment next month": "target"})

print("Shape:", df.shape)
print(df.dtypes)
print(df["target"].value_counts(normalize=True))

df.to_csv("data/credit.csv", index=True)

X = df.drop(columns=["target"])
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

joblib.dump((X_train, X_test, y_train, y_test, scaler), "data/processed_data.pkl")
print("Препроцессинг завершён.")

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

joblib.dump(clf, "data/credit_model.pkl")
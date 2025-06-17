import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import os
import matplotlib.pyplot as plt

X_train, X_test, y_train, y_test, scaler = joblib.load("data/processed_data.pkl")
victim_model = joblib.load("data/credit_model.pkl")

print("[*] Запрашиваем у «жертвы» прогнозы на тестовой выборке...")
y_prob_test = victim_model.predict_proba(X_test)
y_pred_test = victim_model.predict(X_test)

print("[*] Обучаем суррогатную модель (LogisticRegression) на X_test → y_pred_test …")
surrogate = LogisticRegression(max_iter=1000)
surrogate.fit(X_test, y_pred_test)

y_surrogate_pred = surrogate.predict(X_test)
fidelity = accuracy_score(y_pred_test, y_surrogate_pred)
print(f"[+] Fidelity (surrogate vs victim): {fidelity*100:.2f}%")

accuracy_surrogate = accuracy_score(y_test, y_surrogate_pred)
print(f"[+] Accuracy (surrogate vs ground truth): {accuracy_surrogate*100:.2f}%")

print("\nSurrogate classification report:")
print(classification_report(y_test, y_surrogate_pred))

os.makedirs("results", exist_ok=True)
labels = ["Fidelity", "Accuracy"]
values = [fidelity*100, accuracy_surrogate*100]
plt.figure(figsize=(4,3))
plt.bar(labels, values)
plt.ylim(0, 100)
plt.ylabel("Percent")
plt.title("Model Extraction Results")
plt.tight_layout()
plt.savefig("results/extraction_plot.png")
plt.close()
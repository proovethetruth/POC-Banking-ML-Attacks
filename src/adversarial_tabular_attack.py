import joblib
import numpy as np
from art.estimators.classification import SklearnClassifier
from art.attacks.evasion import HopSkipJump
from sklearn.metrics import accuracy_score
import os
import matplotlib.pyplot as plt

X_train, X_test, y_train, y_test, scaler = joblib.load("data/processed_data.pkl")
victim = joblib.load("data/credit_model.pkl")

classifier = SklearnClassifier(model=victim)

attack = HopSkipJump(
    classifier=classifier,
    max_iter=10,
    init_eval=10,
    init_size=100
)

n = 200
x_orig = X_test[:n]
y_orig = y_test[:n]

print(f"[*] Запускаем HopSkipJump на {n} примерах...")
x_adv = attack.generate(x=x_orig)

y_pred_clean = victim.predict(x_orig)
y_pred_adv   = victim.predict(x_adv)

acc_clean = accuracy_score(y_orig, y_pred_clean)
acc_adv   = accuracy_score(y_orig, y_pred_adv)
print(f"[+] Accuracy clean : {acc_clean*100:.2f}%")
print(f"[+] Accuracy adv   : {acc_adv*100:.2f}%")

os.makedirs("results", exist_ok=True)
labels = ["Clean", "Adversarial"]
values = [acc_clean*100, acc_adv*100]
plt.figure(figsize=(4,3))
plt.bar(labels, values, color=["#4c72b0","#c44e52"])
plt.ylim(0, 100)
plt.ylabel("Accuracy %")
plt.title("HopSkipJump Attack")
plt.tight_layout()
plt.savefig("results/tabular_adv_plot.png")
plt.close()
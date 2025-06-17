import joblib
import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
import os
import matplotlib.pyplot as plt

X_train, X_test, y_train, y_test, scaler = joblib.load("data/processed_data.pkl")
victim = joblib.load("data/credit_model.pkl")

prob_train = victim.predict_proba(X_train)
prob_test = victim.predict_proba(X_test)

conf_train = np.max(prob_train, axis=1)
conf_test = np.max(prob_test, axis=1)

threshold = np.median(conf_train)

member_train = conf_train > threshold
member_test = conf_test > threshold

y_true = np.concatenate([np.ones_like(member_train), np.zeros_like(member_test)])
y_scores = np.concatenate([conf_train, conf_test])
y_pred = np.concatenate([member_train, member_test])

acc = accuracy_score(y_true, y_pred)
auc_score = roc_auc_score(y_true, y_scores)

print("Membership Inference Attack")
print(f"  Threshold = {threshold:.4f}")
print(f"  Attack Accuracy = {acc*100:.2f}%")
print(f"  AUC Score = {auc_score*100:.2f}%")

os.makedirs("results", exist_ok=True)

fpr, tpr, _ = roc_curve(y_true, y_scores)
roc_auc = roc_auc_score(y_true, y_scores)

plt.figure(figsize=(4,4))
plt.plot(fpr, tpr, label=f"AUC = {roc_auc*100:.1f}%")
plt.plot([0,1], [0,1], "k--", linewidth=0.8)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Membership Inference")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("results/membership_roc.png")
plt.close()

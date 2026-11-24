import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Iris-MLOps-Experiment")

X, y = load_iris(return_X_y=True)
with mlflow.start_run():
    clf = RandomForestClassifier(n_estimators=50, random_state=42).fit(X, y)
    acc = clf.score(X, y)
    mlflow.log_param("n_estimators", 50)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(
        clf,
        name="model",
        registered_model_name="IrisClassifier",
        serialization_format="cloudpickle"
    )

client = MlflowClient()
latest = client.search_model_versions("name='IrisClassifier'")[0]
client.transition_model_version_stage(
    name="IrisClassifier", version=latest.version, stage="Production"
)
print(f"Model v{latest.version} promoted to Production! Accuracy: {acc:.2f}")

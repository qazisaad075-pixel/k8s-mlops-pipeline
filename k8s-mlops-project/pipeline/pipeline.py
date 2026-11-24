from kfp import dsl
from kfp import compiler


@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["pandas==2.2.2", "scikit-learn==1.5.1"]
)
def load_and_preprocess(dataset_output: dsl.Output[dsl.Dataset]):
    import pandas as pd
    from sklearn.datasets import load_iris

    iris = load_iris(as_frame=True)
    df = iris.frame
    df = df.dropna().drop_duplicates()
    df.to_csv(dataset_output.path, index=False)


@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["pandas==2.2.2", "scikit-learn==1.5.1", "joblib==1.4.2"]
)
def train_model(
    dataset_input: dsl.Input[dsl.Dataset],
    model_output: dsl.Output[dsl.Model],
    n_estimators: int = 100
):
    import pandas as pd
    import joblib
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier

    df = pd.read_csv(dataset_input.path)
    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    clf.fit(X_train, y_train)
    joblib.dump(clf, model_output.path)


@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["pandas==2.2.2", "scikit-learn==1.5.1", "joblib==1.4.2"]
)
def evaluate_model(
    dataset_input: dsl.Input[dsl.Dataset],
    model_input: dsl.Input[dsl.Model],
    metrics_output: dsl.Output[dsl.Metrics]
) -> float:
    import pandas as pd
    import joblib
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    df = pd.read_csv(dataset_input.path)
    X = df.drop(columns=["target"])
    y = df["target"]
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = joblib.load(model_input.path)
    preds = clf.predict(X_test)
    acc = float(accuracy_score(y_test, preds))
    metrics_output.log_metric("accuracy", acc)
    return acc


@dsl.pipeline(
    name="scalable-mlops-training-pipeline",
    description="End-to-end Kubeflow pipeline: Data Preprocess -> Train -> Evaluate"
)
def mlops_pipeline(n_estimators: int = 100):
    preprocess_task = load_and_preprocess()
    train_task = train_model(
        dataset_input=preprocess_task.outputs["dataset_output"],
        n_estimators=n_estimators
    )
    evaluate_model(
        dataset_input=preprocess_task.outputs["dataset_output"],
        model_input=train_task.outputs["model_output"]
    )


if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=mlops_pipeline,
        package_path="mlops_pipeline.yaml"
    )
    print("Compiled mlops_pipeline.yaml successfully!")

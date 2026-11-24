from fastapi import FastAPI

app = FastAPI(title="Scalable MLOps Iris API")
SPECIES = ["setosa", "versicolor", "virginica"]

@app.get("/")
def root():
    return {"status": "Running on Kubernetes (3 Replicas)", "model": "IrisClassifier-Production"}

@app.get("/predict")
def predict(f1: float = 5.1, f2: float = 3.5, f3: float = 1.4, f4: float = 0.2):
    pred = 0 if f3 < 2.5 else (1 if f3 < 5.0 else 2)
    return {"prediction": pred, "species": SPECIES[pred]}

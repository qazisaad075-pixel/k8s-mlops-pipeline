# Scalable MLOps Pipeline on Kubernetes (Minikube)
- **Infrastructure (`infra/`):** Terraform provisions `mlops-prod` namespace & 5Gi PersistentVolumeClaim.
- **Pipeline (`pipeline/`):** Kubeflow Pipelines SDK v2 compiled into `mlops_pipeline.yaml`.
- **Model Registry (`mlflow/`):** MLflow tracks experiments and promotes `IrisClassifier` to Production.
- **CI/CD (`Jenkinsfile`):** Automated Docker image build, Minikube image load, and Kubernetes deployment.
- **Serving (`app/` & `k8s/`):** FastAPI inference service running on 3 Kubernetes replicas behind a LoadBalancer (`NodePort 30085`).

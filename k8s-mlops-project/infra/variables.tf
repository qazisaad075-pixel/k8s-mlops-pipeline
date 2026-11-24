variable "cluster_name" {
  description = "Name of the local Minikube Kubernetes cluster"
  type        = string
  default     = "mlops-k8s-cluster"
}

variable "namespace" {
  description = "Kubernetes namespace for MLOps workloads"
  type        = string
  default     = "mlops-prod"
}

variable "replica_count" {
  description = "Number of model deployment replicas (3-5 required)"
  type        = number
  default     = 3
}

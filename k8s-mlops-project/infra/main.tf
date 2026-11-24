resource "kubernetes_namespace" "mlops_ns" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_persistent_volume_claim" "mlops_storage" {
  depends_on = [kubernetes_namespace.mlops_ns]
  metadata {
    name      = "mlops-artifacts-pvc"
    namespace = kubernetes_namespace.mlops_ns.metadata[0].name
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "5Gi"
      }
    }
  }
}

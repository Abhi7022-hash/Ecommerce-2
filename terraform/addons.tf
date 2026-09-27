# ==================================================
# VPC CNI
# ==================================================

resource "aws_eks_addon" "vpc_cni" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "vpc-cni"

  depends_on = [
    aws_eks_cluster.main
  ]
}

# ==================================================
# EBS CSI
# ==================================================

resource "aws_eks_addon" "ebs_csi" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "aws-ebs-csi-driver"

  pod_identity_association {
    role_arn        = aws_iam_role.ebs_csi.arn
    service_account = "ebs-csi-controller-sa"
  }

  depends_on = [
    aws_eks_addon.pod_identity_agent,
    aws_iam_role_policy_attachment.ebs_csi_policy
  ]
}

# ==================================================
# COREDNS
# ==================================================

resource "aws_eks_addon" "coredns" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "coredns"

  depends_on = [
    aws_eks_node_group.managed
  ]
}

# ==================================================
# KUBE PROXY
# ==================================================

resource "aws_eks_addon" "kube_proxy" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "kube-proxy"

  depends_on = [
    aws_eks_cluster.main
  ]
}

# ==================================================
# METRICS SERVER
# ==================================================

resource "aws_eks_addon" "metrics_server" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "metrics-server"

  depends_on = [
    aws_eks_node_group.managed
  ]
}

# ==================================================
# NODE MONITORING AGENT
# ==================================================

resource "aws_eks_addon" "node_monitoring" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "eks-node-monitoring-agent"

  depends_on = [
    aws_eks_node_group.managed
  ]
}

# ==================================================
# EXTERNAL DNS
# ==================================================

resource "aws_eks_addon" "external_dns" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "external-dns"

  depends_on = [
    aws_eks_node_group.managed
  ]
}
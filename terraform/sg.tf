# ==================================================
# CLUSTER SECURITY GROUP
# ==================================================

resource "aws_security_group" "cluster" {
  name        = "${var.cluster_name}-cluster-sg"
  description = "Security group for EKS control plane"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "${var.cluster_name}-cluster-sg"
  }
}

# --------------------------------------------------
# Node SG -> Cluster SG
# EKS API Server HTTPS
# --------------------------------------------------

resource "aws_vpc_security_group_ingress_rule" "cluster_from_nodes" {
  security_group_id            = aws_security_group.cluster.id
  referenced_security_group_id = aws_security_group.nodes.id

  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}

# --------------------------------------------------
# Cluster SG -> Cluster SG
# --------------------------------------------------

resource "aws_vpc_security_group_ingress_rule" "cluster_self" {
  security_group_id            = aws_security_group.cluster.id
  referenced_security_group_id = aws_security_group.cluster.id

  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "cluster_all" {
  security_group_id = aws_security_group.cluster.id

  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "-1"
}


# ==================================================
# NODE SECURITY GROUP
# ==================================================

resource "aws_security_group" "nodes" {
  name        = "${var.cluster_name}-node-sg"
  description = "Security group for EKS worker nodes"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "${var.cluster_name}-node-sg"
  }
}

# --------------------------------------------------
# NGINX Load Balancer -> NodePort
#
# NGINX Service is exposed through AWS NLB.
# NLB sends traffic to the worker-node NodePort.
# --------------------------------------------------

resource "aws_vpc_security_group_ingress_rule" "nodes_nodeport" {
  security_group_id = aws_security_group.nodes.id

  cidr_ipv4 = "0.0.0.0/0"

  from_port   = 30000
  to_port     = 32767
  ip_protocol = "tcp"
}

# --------------------------------------------------
# Cluster -> Nodes
# --------------------------------------------------

resource "aws_vpc_security_group_ingress_rule" "nodes_from_cluster" {
  security_group_id            = aws_security_group.nodes.id
  referenced_security_group_id = aws_security_group.cluster.id

  from_port   = 1025
  to_port     = 65535
  ip_protocol = "tcp"
}

# --------------------------------------------------
# Node -> Node
# --------------------------------------------------

resource "aws_vpc_security_group_ingress_rule" "nodes_self" {
  security_group_id            = aws_security_group.nodes.id
  referenced_security_group_id = aws_security_group.nodes.id

  ip_protocol = "-1"
}

# --------------------------------------------------
# Node Egress
# --------------------------------------------------

resource "aws_vpc_security_group_egress_rule" "nodes_all" {
  security_group_id = aws_security_group.nodes.id

  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "-1"
}
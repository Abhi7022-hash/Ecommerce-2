variable "aws_region" {
  description = "AWS-Region"
  type = string
  default = "us-east-1"
}


variable "cluster_name" {
  description = "AWS-Eks cluster"
  type = string
  default = "ecommerce-cluster"
}


variable "node_instance_type" {
  description = "Node-type"
  type = string
  default = "t2.micro"
}


variable "desired_nodes" {
  description = "Number of worker nodes"
  type = number
  default = 2
}


variable "min_nodes" {
  description = "number of minimum nodes"
  type = number
  default = 1
}


variable "max_nodes" {
  description = "number of maximum nodes"
  type = number
  default = 3
}

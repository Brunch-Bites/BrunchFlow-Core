# BrunchFlow Core Infrastructure - AWS Deployment
# Optimized for High-Performance Multi-Agent Orchestration

terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1. Network Foundation (VPC)
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "brunchflow-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
}

# 2. Kubernetes Cluster (EKS)
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.15"

  cluster_name    = "brunchflow-orchestrator-cluster"
  cluster_version = "1.27"

  vpc_id                         = module.vpc.vpc_id
  subnet_ids                     = module.vpc.private_subnets
  cluster_endpoint_public_access = true

  # 3. GPU Node Groups (The "Hungry" Compute)
  eks_managed_node_groups = {
    gpu_nodes = {
      name = "brunchflow-gpu-pool"

      instance_types = ["g4dn.xlarge"] # NVIDIA T4 Tensor Core nodes
      min_size       = 1
      max_size       = 5
      desired_size   = 2

      labels = {
        role = "ai-inference"
        accelerator = "nvidia"
      }
    }
    general_nodes = {
      name = "brunchflow-standard-pool"

      instance_types = ["t3.medium"]
      min_size       = 2
      max_size       = 10
      desired_size   = 2
    }
  }
}

variable "aws_region" {
  description = "Target deployment region"
  type        = string
  default     = "us-east-1"
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

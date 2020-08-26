dask_initial_config = {
    "scheduler_url": None
}

adaptive_initial_config = {
    "max_workers": 1,
    "max_idle_time": 300,
    "poll_interval": 10
}

terraform_initial_config = {
    "cloud_provider": "aws",
    "image_name": "ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*",
    "image_owner": "099720109477",
    "scheduler_name": "scheduler",
    "scheduler_type": "t2.small",
    "scheduler_port": "8786",
    "dashboard_port": "8787",
    "worker_names": [],
    "worker_type": "t2.small",
    "region_name": "eu-west-1",
    "public_key_path": None,
    "key_name": None,
    "sg_name": None
}

terraform_template = """ variable "region_name" {
  type = string
  description = "AWS region to use"
}

variable "cloud_provider" {
  type = string
  description = "Cloud provider - not used"
}

variable "image_name" {
  type = string
  description = "image name used to create instances"
}

variable "image_owner" {
  type = string
  description = "name of image owner"
}

variable "sg_name" {
  type = string
  description = "security group name"
}

variable "key_name" {
  type = string
  description = "key name"
}

variable "scheduler_name" {
  type = string
  description = "name for scheduler instance to launch"
  default = "scheduler"
}

variable "scheduler_type" {
  type = string
  description = "type of scheduler instance to launch"
  default = "t2.small"
}

variable "scheduler_port" {
  type = string
  description = "port used by dask scheduler"
  default = "8786"
}

variable "dashboard_port" {
  type = string
  description = "port used by dask dashboard"
  default = "8787"
}

variable "worker_type" {
  type = string
  description = "type of worker instance to launch"
  default = "t2.small"
}

variable "worker_names" {
  type = list
  description = "names of instances to launch"
  default = []
}

variable "public_key_path" {
  type = string
  description = "path to public key file"
}

provider "aws" {
  profile = "default"
  region  = var.region_name
}

data "aws_ami" "base" {
  most_recent = true
  owners = [var.image_owner]
  filter {
    name = "name"
    values = ["${var.image_name}"]
  }
}

resource "aws_key_pair" "terraform_ec2_key" {
  key_name = var.key_name
  public_key = file(var.public_key_path)
}

resource "aws_security_group" "allow_ssh" {
  name = var.sg_name
  description = "Allow ssh access from anywhere and full inter-worker comms"
  ingress {
    from_port = 22
    to_port   = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = var.scheduler_port
    to_port   = var.scheduler_port
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = var.dashboard_port
    to_port   = var.dashboard_port
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 0
    to_port   = 0
    protocol = "-1"
    self = true
  }
  egress {
    from_port = 0
    to_port = 0 
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  } 
} 

resource "aws_instance" "scheduler" {

  ami = data.aws_ami.base.id
  instance_type = var.scheduler_type
  key_name = var.key_name
  security_groups = ["${var.sg_name}"]
  iam_instance_profile = "EC2InstanceRole"
  tags = {
    Name = var.scheduler_name
  }
  user_data = <<-EOF
        #! /bin/sh
        sudo apt update
        sudo apt install -y python3-pip awscli 
        sudo ubuntu-drivers autoinstall
        sudo pip3 install dask distributed bokeh crossflow==0.0.4
        sudo aws configure set default.region ${var.region_name} 
        sudo /usr/local/bin/dask-scheduler --port "${var.scheduler_port}" --dashboard-address ":${var.dashboard_port}"> /tmp/scheduler.log 2>&1 &
  EOF
} 

resource "aws_spot_instance_request" "worker" {

  for_each = toset(var.worker_names)
  ami = data.aws_ami.base.id
  instance_type = var.worker_type
  key_name = var.key_name
  security_groups = ["${var.sg_name}"]
  iam_instance_profile = "EC2InstanceRole"
  tags = {
    Name = each.key
  }
  user_data = <<-EOF
        #! /bin/sh
        sudo apt update
        sudo apt install -y python3-pip awscli
        sudo ubuntu-drivers autoinstall
        sudo pip3 install dask distributed crossflow==0.0.3rc2
        sudo aws configure set default.region ${var.region_name} 
        sudo /usr/local/bin/dask-worker --name "${each.key}" --nthreads 1 --local-directory /tmp/dask-worker-dir "${aws_instance.scheduler.private_ip}:8786"  > /tmp/dask-worker.log 2>&1 &
  EOF
  wait_for_fulfillment = true
  provisioner "local-exec" {
    command = "aws ec2 create-tags --resources ${self.spot_instance_id} --tags Key=Name,Value=${each.key}  --region ${var.region_name}"

    environment = {
      AWS_DEFAULT_REGION = "${var.region_name}"
    }
  }
}
// A variable for extracting the external ip of the jobrunners
output "scheduler-url" {
  value = "${aws_instance.scheduler.public_ip}:${var.scheduler_port}"
}
output "worker-ip" {
  value = values(aws_spot_instance_request.worker)[*].public_ip
}
"""

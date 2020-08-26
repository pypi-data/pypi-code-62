dask_initial_config = {
    "scheduler_url": None
}

adaptive_initial_config = {
    "max_workers": 1,
    "max_idle_time": 300,
    "poll_interval": 10
}

terraform_initial_config = {
    "cloud_provider": "gcp",
    "image_id": "ubuntu-1804-lts",
    "scheduler_name": "scheduler",
    "scheduler_type": "f1-micro",
    "scheduler_port": "8786",
    "dashboard_port": "8787",
    "worker_names": [],
    "worker_type": "f1-micro",
    "accelerator_type": "nvidia-tesla-t4",
    "accelerator_count": "0",
    "project_name": None,
    "region_name": None,
    "zone_name": None,
    "public_key_path": None,
    "user_name": None,
}

terraform_template = """ variable "project_name"  {
  type = string
  description = "GCP project name"
}

variable "region_name" {
  type = string
  description = "GC region to use"
}

variable "cloud_provider" {
  type = string
  description = "Cloud provider - not used"
}

variable "zone_name" {
  type = string
  description = "GC zone to use"
}

variable "image_id" {
  type = string
  description = "image ID used to create instances"
}

variable "scheduler_name" {
  type = string
  description = "name for scheduler instance to launch"
  default = "scheduler"
}

variable "scheduler_type" {
  type = string
  description = "type of scheduler instance to launch"
  default = "f1-micro"
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
  default = "f1-micro"
}

variable "accelerator_type" {
  type = string
  description = "type of accelerator attached to each worker instance"
  default = "nvidia-tesla-t4"
}

variable "accelerator_count" {
  type = string
  description = "numbner  of accelerators attached to each worker instance"
  default = "0"
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

variable "user_name" {
  type = string
  description = "user name on instances"
}

provider "google" {
  project = var.project_name
  region  = var.region_name
  zone    = var.zone_name
}

resource "google_compute_firewall" "default" {
  name    = "xc-firewall"
  network = google_compute_network.default.name

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["22", var.scheduler_port, var.dashboard_port]
  }

}

resource "google_compute_firewall" "cluster" {
  name    = "cluster-firewall"
  network = google_compute_network.default.name
  source_tags = ["dask"]

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
  }

}

resource "google_compute_network" "default" {
  name = "xc-network"
}

resource "google_compute_instance" "scheduler" {
  name = var.scheduler_name
  machine_type = var.scheduler_type
  allow_stopping_for_update = "true"
  tags = ["dask"]

  metadata = {
    ssh-keys = "${var.user_name}:${file(var.public_key_path)}"
    }

  metadata_startup_script = <<-EOF
        #! /bin/sh
        sudo apt update
        sudo apt install -y python3-pip awscli 
        sudo ubuntu-drivers autoinstall
        sudo pip3 install dask distributed bokeh crossflow==0.0.4
        sudo aws configure set default.region ${var.region_name} 
        sudo /usr/local/bin/dask-scheduler --port "${var.scheduler_port}" --dashboard-address ":${var.dashboard_port}"> /tmp/scheduler.log 2>&1 &
  EOF
  
  boot_disk {
    initialize_params {
      image = var.image_id
    }
  }

  network_interface {
    network = google_compute_network.default.name
    access_config {
    }
  }

  service_account {
    scopes = ["cloud-platform"]
  }
} 

resource "google_compute_instance" "worker" {

  for_each = toset(var.worker_names)
  name = each.value
  machine_type = var.worker_type
  allow_stopping_for_update = "true"
  tags = ["dask"]

  metadata = {
    ssh-keys = "${var.user_name}:${file(var.public_key_path)}"
    }

  metadata_startup_script = <<-EOF
        #! /bin/sh
        sudo apt update
        sudo apt install -y python3-pip awscli
        sudo ubuntu-drivers autoinstall
        sudo pip3 install dask distributed crossflow==0.0.3rc2
        sudo aws configure set default.region ${var.region_name} 
        sudo /usr/local/bin/dask-worker --name "${each.key}" --nthreads 1 --local-directory /tmp/dask-worker-dir "${google_compute_instance.scheduler.network_interface.0.network_ip}:${var.scheduler_port}"  > /tmp/dask-worker.log 2>&1 &
  EOF

  scheduling {
    preemptible = "false"
    on_host_maintenance = "TERMINATE"
    }

  guest_accelerator {
    type = var.accelerator_type
    count = var.accelerator_count
  }

  boot_disk {
    initialize_params {
      image = var.image_id
    }
  }
  network_interface {
    network = google_compute_network.default.name
    access_config {
    }
  }

  service_account {
    scopes = ["cloud-platform"]
  }
}

// A variable for extracting the external ip of the jobrunners
output "scheduler-url" {
  value = "${google_compute_instance.scheduler.network_interface.0.access_config.0.nat_ip}:${var.scheduler_port}"
}
output "worker-ip" {
  value = values(google_compute_instance.worker)[*].network_interface.0.access_config.0.nat_ip
}
"""

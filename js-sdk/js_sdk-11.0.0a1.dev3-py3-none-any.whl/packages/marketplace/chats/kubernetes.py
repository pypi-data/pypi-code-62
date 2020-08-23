import time
import uuid
from jumpscale.loader import j
from jumpscale.clients.explorer.models import Category, DiskType, Mode
from jumpscale.sals.chatflows.chatflows import GedisChatBot, StopChatFlow, chatflow_step
from jumpscale.sals.reservation_chatflow.models import SolutionType
from jumpscale.sals.marketplace import deployer, MarketPlaceChatflow
import math


class KubernetesDeploy(MarketPlaceChatflow):
    SOLUTION_TYPE = SolutionType.Kubernetes

    steps = [
        "welcome",
        "solution_name",
        "choose_network",
        "nodes_selection",
        "public_key_get",
        "expiration_time",
        "ip_selection",
        "overview",
        "cluster_reservation",
        "success",
    ]
    title = "Kubernetes"

    @chatflow_step(title="Master and Worker nodes selection")
    def nodes_selection(self):
        retry = False
        while True:
            form = self.new_form()
            sizes = ["1 vCPU 2 GiB ram 50GiB disk space", "2 vCPUs 4 GiB ram 100GiB disk space"]
            cluster_size_string = form.drop_down_choice(
                "Choose the size of your nodes", sizes, default=sizes[0], retry=retry
            )
            masternodes = form.int_ask(
                "Please specify the number of master nodes", default=1, required=True, min=1, retry=retry
            )  # minimum should be 1
            workernodes = form.int_ask(
                "Please specify the number of worker nodes", default=1, required=True, min=1, retry=retry
            )  # minimum should be 1

            form.ask()
            self.cluster_size = sizes.index(cluster_size_string.value) + 1  # sizes are index 1
            # Select nodes
            if self.cluster_size == 1:
                nodequery = {"sru": 50, "mru": 2, "cru": 1, "currency": self.network.currency}
            else:
                nodequery = {"sru": 100, "mru": 4, "cru": 2, "currency": self.network.currency}
            try:
                farms = j.sals.reservation_chatflow.get_farm_names(
                    masternodes.value + workernodes.value, self, **nodequery
                )
                self.master_nodes_selected = j.sals.reservation_chatflow.get_nodes(
                    masternodes.value, farm_names=farms[: masternodes.value], **nodequery
                )

                self.worker_nodes_selected = j.sals.reservation_chatflow.get_nodes(
                    workernodes.value, farm_names=farms[masternodes.value :], **nodequery
                )
                break
            except StopChatFlow as e:
                retry = True
                self.md_show(e.msg)

        self.user_form_data["Master number"] = masternodes.value
        self.user_form_data["Workers number"] = workernodes.value
        self.user_form_data["Cluster size"] = cluster_size_string.value

    @chatflow_step(title="Access keys and secret")
    def public_key_get(self):
        self.user_form_data["SSH keys"] = self.upload_file(
            """Please add your public ssh key, this will allow you to access the deployed container using ssh.
                Just upload the ssh keys file with each key on a seperate line"""
        )
        self.ssh_keys_list = self.user_form_data["SSH keys"].split("\n")

        self.user_form_data["Cluster secret"] = self.string_ask("Please add the cluster secret", default="secret")

    @chatflow_step(title="IP selection")
    def ip_selection(self):
        self.network_copy = self.network.copy()
        ipaddresses = list()
        for idx, node_selected in enumerate(self.master_nodes_selected):
            self.network_copy.add_node(node_selected)
            msg = f"Please choose IP Address for master node {idx + 1} of your kubernets cluster"
            ip_address = self.network_copy.ask_ip_from_node(node_selected, msg)
            ipaddresses.append(ip_address)

        for idx, node_selected in enumerate(self.worker_nodes_selected):
            nodes_ids = [nid.node_id for nid in self.master_nodes_selected]
            if node_selected.node_id not in nodes_ids:
                self.network_copy.add_node(node_selected)
            msg = f"Please choose IP Address for worker node {idx + 1} of your kubernets cluster"
            ip_address = self.network_copy.ask_ip_from_node(node_selected, msg)
            ipaddresses.append(ip_address)

        self.user_form_data["IP Address"] = ipaddresses

    @chatflow_step(title="Cluster reservations", disable_previous=True)
    def cluster_reservation(self):
        self.md_show_update("Preparing network on nodes.....")
        self.network = self.network_copy
        # update network
        self.network.update(self.user_info()["username"], currency=self.network.currency, bot=self)
        # create new reservation
        self.reservation = j.sals.zos.reservation_create()
        # Create master and workers
        # Master is in the first node from the selected nodes
        self.md_show_update("Preparing cluster reservation......")
        master = None
        for idx, master_node in enumerate(self.master_nodes_selected):
            master = j.sals.zos.kubernetes.add_master(
                reservation=self.reservation,
                node_id=master_node.node_id,
                network_name=self.network.name,
                cluster_secret=self.user_form_data["Cluster secret"],
                ip_address=self.user_form_data["IP Address"][idx],
                size=self.cluster_size,
                ssh_keys=self.ssh_keys_list,
            )

        # Workers are in the rest of the nodes
        for i, worker_node in enumerate(self.worker_nodes_selected):
            j.sals.zos.kubernetes.add_worker(
                reservation=self.reservation,
                node_id=worker_node.node_id,
                network_name=self.network.name,
                cluster_secret=self.user_form_data["Cluster secret"],
                ip_address=self.user_form_data["IP Address"][i + self.user_form_data["Master number"]],
                size=self.cluster_size,
                master_ip=master.ipaddress,
                ssh_keys=self.ssh_keys_list,
            )

        # register the reservation
        metadata = self.user_form_data.copy()
        metadata.pop("SSH keys")
        res = deployer.get_solution_metadata(
            self.user_form_data["Solution name"],
            SolutionType.Kubernetes,
            self.user_info()["username"],
            metadata,
            self.solution_uuid,
        )
        self.reservation = j.sals.reservation_chatflow.add_reservation_metadata(self.reservation, res)
        self.resv_id = deployer.register_and_pay_reservation(
            self.reservation,
            self.expiration,
            customer_tid=j.core.identity.me.tid,
            currency=self.network.currency,
            bot=self,
        )

    @chatflow_step(title="Success", disable_previous=True)
    def success(self):
        res = f"# Kubernetes cluster has been deployed successfully: your reservation id is: {self.resv_id}"
        for i, ip in enumerate(self.user_form_data["IP Address"]):
            res += f"""
## kubernete {i +1} IP : {ip}
To connect ssh rancher@{ip}
            """
        self.md_show(res)


chat = KubernetesDeploy

import os
import re
import json
import sys
import kfp
import time
import subprocess
import requests
from kubernetes import client, config
from datetime import datetime
from urllib.parse import quote_plus
# sys.tracebacklimit=0

class GeneratePipe():
    def __init__(self, ):
        self.pipe_path = "pipeline.yaml"
        config.load_incluster_config()

    def get_pipeline_list(self):
        kfp_client = kfp.Client()
        pipeline_data = {}
        page_token = None

        while True:
            pipeline_list = kfp_client.list_pipelines(
                page_token=page_token)

            for pipe in pipeline_list.pipelines:
                pipeline_data[pipe.name] = pipe.id

            page_token = pipeline_list.next_page_token
            if page_token == None:
                break

            time.sleep(1)

        return pipeline_data

    def check_any_pipeline(self, local_path, pipeline_data):
        # print("pipeline_data : %s" % pipeline_data)

        try:
            # create version of pipeline
            pipeline_id = pipeline_data[os.getenv('PIPE_NAME')]
            kfp_client = kfp.Client()
            res_pipe = kfp_client.pipeline_uploads.upload_pipeline_version(
                local_path, pipelineid=pipeline_id,
                name=os.getenv('PIPE_VER_NAME'))
            version_id = res_pipe.id
        except Exception as e:
            print("there's no pipeline selected, try to create new...")
            kfp_client = kfp.Client()
            res_pipe = kfp_client.upload_pipeline(
                local_path, os.getenv('PIPE_NAME'))
            pipeline_id = res_pipe.id
            version_id = None

        return (pipeline_id, version_id)

    def check_any_experiment(self):
        try:
            kfp_client = kfp.Client()
            res_exp = kfp_client.get_experiment(
                experiment_name=os.getenv('EXP_NAME'))
            exp_id = res_exp.id
        except Exception as e:
            kfp_client = kfp.Client()
            res_exp = kfp_client.create_experiment(
                os.getenv('EXP_NAME'),
                description=os.getenv('exp_desc'))
            exp_id = res_exp.id

        return exp_id

    def run_logging(self, pod_names, prev_time, cur_time):
        pod_name_filter = ""
        for i, pod_name in enumerate(pod_names):
            if i == 0:
                pod_name_filter += pod_name
            else:
                pod_name_filter += " OR %s" % pod_name

        cmd_str = """gcloud logging read \
            'timestamp>=\"%s\" AND timestamp<=\"%s\"
            AND resource.type=k8s_container
            AND resource.labels.cluster_name=kubeflow-research
            AND resource.labels.pod_name=(%s)' \
            --order=asc --format=json | python3 -c \
            'import sys, json; [print(data[\"textPayload\"]) for data in json.load(sys.stdin)]'""" % (
                prev_time, cur_time, pod_name_filter)

        os.system(cmd_str)

    def send_notification(self, nodes, comps, status, job_name, log_url):
        url = 'https://api.warungpintar.co/warbot/v1/send?recipient=%s&type=%s&gitlab_token=%s' %(
            os.getenv('WORKCHAT_ID'), os.getenv('WORKCHAT_TYPE'), os.getenv('GITLAB_PERS_TOKEN'))
        headers = {'content-type': 'application/json'}

        comp_status = ""

        for i, comp in enumerate(comps):
            sel_node = nodes[comp]
            sel_comp_stat = "<COMPONENT-%s>\nCOMP_NAME: %s\nSTATUS: %s\nFINISH_DATE: %s\n\n" % (
                str(i+1), sel_node['displayName'], sel_node['phase'], sel_node['finishedAt'])
            comp_status += sel_comp_stat

        data = {
            "message": "<<<%s>>>\n\nJOB_STATUS: %s\nLOGGING URL: %s\n\n%s" % (
                job_name, status, log_url, comp_status)
        }
        json_data = json.dumps(data)

        response = requests.post(url, headers=headers, data=json_data)

    def get_namespace_and_pods(self, pipe_run_id):
        while True:
            namespaces = []

            v1 = client.CoreV1Api()
            ret = v1.list_pod_for_all_namespaces(watch=False)
            for i in ret.items:
                namespaces.append((i.metadata.namespace, i.metadata.name))

            # pattern = os.getenv('PIPE_NAME').replace(' ', '-').lower()
            kfp_client = kfp.Client()
            response = kfp_client.get_run(run_id=pipe_run_id)
            manifest = json.loads(
                response.pipeline_runtime.workflow_manifest)
            pattern = manifest['metadata']['name']

            pods = [ns[1] for ns in namespaces if re.match(pattern, ns[1])]

            if len(pods) > 0:
                break
            else:
                print("pods not found, trying to search pods...")
                time.sleep(1)

        return pods

    def check_job(self, pipe_run_id):
        job_details = {
            'nodes': None,
            'job_status': None,
            'job_name': None
        }

        try:
            kfp_client = kfp.Client()
            response = kfp_client.wait_for_run_completion(
                run_id=pipe_run_id, timeout=5)

            manifest = json.loads(
                response.pipeline_runtime.workflow_manifest)

            job_details['nodes'] = manifest['status']['nodes']
            job_details['job_status'] = manifest['status']['phase']
            job_details['job_name'] = response.run.name

            return job_details
        except Exception as e:
            return job_details

    def wait_job_until_finish(self, pipe_run_id, comps, log_url):
        prev_time = datetime.now().isoformat(timespec='seconds') + 'Z'
        job_details = self.check_job(pipe_run_id)
        is_finished = False

        while True:
            if job_details['job_status'] == 'Succeeded':
                is_finished = True

            if job_details['job_status'] == 'Succeeded' or job_details['job_status'] == 'Failed':
                self.send_notification(
                    job_details['nodes'], comps,
                    job_details['job_status'],
                    job_details['job_name'], log_url)
                break

            time.sleep(1)
            cur_time = datetime.now().isoformat(timespec='seconds') + 'Z'
            self.run_logging(comps, prev_time, cur_time)

            job_details = self.check_job(pipe_run_id)
            prev_time = cur_time

        if not is_finished:
            raise Exception("Job is failed, please check your logs...")

    def generate_log_url(self, pod_names):
        pod_name_filter = ""
        for i, pod_name in enumerate(pod_names):
            if i == 0:
                pod_name_filter += '"%s"' % pod_name
            else:
                pod_name_filter += ' OR "%s"' % pod_name

        base_url = "https://console.cloud.google.com/logs/viewer?project=warung-support&interval=NO_LIMIT&advancedFilter="
        query_str = '''resource.type="k8s_container"
            AND resource.labels.cluster_name="kubeflow-research"
            AND resource.labels.pod_name=(%s)''' % pod_name_filter

        query = quote_plus(query_str)
        final_url = base_url + query

        return final_url

    def run_pipe(self):
        pipeline_data = self.get_pipeline_list()

        # check if any existing pipeline
        pipeline_id, version_id = self.check_any_pipeline(
            self.pipe_path, pipeline_data)

        # check if any existing experiment
        exp_id = self.check_any_experiment()

        kfp_client = kfp.Client()
        pipe_run = kfp_client.run_pipeline(
            exp_id, os.getenv('JOB_NAME'),
            pipeline_id=pipeline_id, version_id=version_id)

        pod_names = self.get_namespace_and_pods(pipe_run.id)
        # generate stackdriver logging url
        log_url = self.generate_log_url(pod_names)

        self.wait_job_until_finish(pipe_run.id, pod_names, log_url)

    def check_node_pool_label(self):
        all_labels = {}
        cmd_str = 'gcloud container node-pools list --cluster=kubeflow-research --zone=asia-east1-a --format=json'
        process = subprocess.Popen(
            [cmd_str], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        out = out.decode('UTF8')
        nodes = json.loads(out)

        for node in nodes:
            labels = node['config']['labels']
            all_labels.update(labels)

        node_key = os.getenv('TRAIN_NODE_KEY')
        node_val = os.getenv('TRAIN_NODE_VAL')

        try:
            if all_labels[node_key] == node_val:
                print("node label %s: %s is existed" % (node_key, node_val))
                return True
            else:
                print("node label %s: %s is not existed" % (node_key, node_val))
                return False
        except Exception as e:
            print("node label %s: %s is not existed " % (node_key, node_val))
            return False

    def check_image_tag(self):
        status = True
        comps = json.loads(os.getenv('COMPONENTS'))

        for images in comps:
            image_tag, _ = images[1].split(":")
            split_img_tag = image_tag.split("/")
            cmd_str = 'gcloud container images list --repository=%s/%s --filter="name:%s"' % (
                split_img_tag[0], split_img_tag[1], split_img_tag[2])

            process = subprocess.Popen(
                [cmd_str], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            out = out.decode('UTF8').split("\n")

            if len(out) == 1:
                status = False
                print("image tag %s is not existed" % split_img_tag[2])
                break
            else:
                print("image tag %s is existed" % split_img_tag[2])
                continue

        return status

    def main(self):
        if not self.check_image_tag():
            raise Exception("Image tag not found...")

        if not self.check_node_pool_label():
            raise Exception("node pool label not found...")

        self.run_pipe()

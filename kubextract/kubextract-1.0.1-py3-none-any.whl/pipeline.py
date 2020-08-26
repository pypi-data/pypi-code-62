import re
import os
import kfp
import yaml
import json
import kfp.dsl as dsl
from kfp import compiler
from utils.watcher import GeneratePipe

def create_comp(images):
    return dsl.ContainerOp(
        name=images[0],
        image=images[1])

@dsl.pipeline(
    name=os.getenv('PIPE_NAME'),
    description=os.getenv('PIPE_DESC'))
def cluster_pipeline():
    comps = json.loads(os.getenv('COMPONENTS'))

    for images in comps:
        if os.getenv('USE_GPU') == 'true':
            prep_op = create_comp(images).set_gpu_limit(1)
        else:
            prep_op = create_comp(images)

if __name__ == '__main__':
    gen_pipe = GeneratePipe()

    conf = dsl.PipelineConf()
    conf.set_default_pod_node_selector(
        os.getenv('TRAIN_NODE_KEY'), os.getenv('TRAIN_NODE_VAL'))
    kfp.compiler.Compiler().compile(
        cluster_pipeline, gen_pipe.pipe_path,
        pipeline_conf=conf)

    gen_pipe.main()

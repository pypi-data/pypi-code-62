import yaml
import os

class GenerateMeta():
    def construct_yaml_str(self):
        content = """
            apiVersion: serving.kubeflow.org/v1alpha2
            kind: InferenceService
            metadata:
              namespace: kubeflow
              labels:
                controller-tools.k8s.io: "1.0"
              name: %s
              nodeSelector:
                %s: %s
            spec:
              default:
                predictor:
                  custom:
                    container:
                      image: %s/%s:%s

        """ % (
            os.getenv('PIPE_NAME'),
            os.getenv('INFER_NODE_KEY'),
            os.getenv('INFER_NODE_VAL'),
            os.getenv('IMAGE_REGISTRY'),
            os.getenv('INFER_IMG_NAME'),
            os.getenv('CI_COMMIT_REF_NAME'))

        return content

    def main(self):
        with open(os.getenv('KFSERVING_CONFIG'), 'w') as outfile:
            content = self.construct_yaml_str()
            yaml_cont = yaml.load(content)
            yaml.dump(yaml_cont, outfile, default_flow_style=False)

if __name__ == '__main__':
    gen_meta = GenerateMeta()
    gen_meta.main()

from localstack.utils.aws import aws_models
YkMry=super
YkMrE=None
YkMra=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  YkMry(LambdaLayer,self).__init__(arn)
  self.cwd=YkMrE
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,YkMra,env=YkMrE):
  YkMry(RDSDatabase,self).__init__(YkMra,env=env)
 def name(self):
  return self.YkMra.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,YkMra,env=YkMrE):
  YkMry(RDSCluster,self).__init__(YkMra,env=env)
 def name(self):
  return self.YkMra.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)

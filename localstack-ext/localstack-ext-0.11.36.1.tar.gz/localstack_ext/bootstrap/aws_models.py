from localstack.utils.aws import aws_models
SnPhv=super
SnPhf=None
SnPhR=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  SnPhv(LambdaLayer,self).__init__(arn)
  self.cwd=SnPhf
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,SnPhR,env=SnPhf):
  SnPhv(RDSDatabase,self).__init__(SnPhR,env=env)
 def name(self):
  return self.SnPhR.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,SnPhR,env=SnPhf):
  SnPhv(RDSCluster,self).__init__(SnPhR,env=env)
 def name(self):
  return self.SnPhR.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)

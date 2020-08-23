from localstack.utils.aws import aws_models
tgypE=super
tgypM=None
tgypa=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  tgypE(LambdaLayer,self).__init__(arn)
  self.cwd=tgypM
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,tgypa,env=tgypM):
  tgypE(RDSDatabase,self).__init__(tgypa,env=env)
 def name(self):
  return self.tgypa.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,tgypa,env=tgypM):
  tgypE(RDSCluster,self).__init__(tgypa,env=env)
 def name(self):
  return self.tgypa.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)

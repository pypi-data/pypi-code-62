from localstack.utils.aws import aws_models
EXFlJ=super
EXFlc=None
EXFlS=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  EXFlJ(LambdaLayer,self).__init__(arn)
  self.cwd=EXFlc
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,EXFlS,env=EXFlc):
  EXFlJ(RDSDatabase,self).__init__(EXFlS,env=env)
 def name(self):
  return self.EXFlS.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,EXFlS,env=EXFlc):
  EXFlJ(RDSCluster,self).__init__(EXFlS,env=env)
 def name(self):
  return self.EXFlS.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)

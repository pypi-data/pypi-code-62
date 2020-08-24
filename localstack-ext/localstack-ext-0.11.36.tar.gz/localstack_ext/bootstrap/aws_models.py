from localstack.utils.aws import aws_models
xikKg=super
xikKu=None
xikKj=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  xikKg(LambdaLayer,self).__init__(arn)
  self.cwd=xikKu
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,xikKj,env=xikKu):
  xikKg(RDSDatabase,self).__init__(xikKj,env=env)
 def name(self):
  return self.xikKj.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,xikKj,env=xikKu):
  xikKg(RDSCluster,self).__init__(xikKj,env=env)
 def name(self):
  return self.xikKj.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)

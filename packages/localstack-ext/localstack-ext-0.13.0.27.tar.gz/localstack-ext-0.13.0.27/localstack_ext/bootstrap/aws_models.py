from localstack.utils.aws import aws_models
WVeRy=super
WVeRr=None
WVeRj=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  WVeRy(LambdaLayer,self).__init__(arn)
  self.cwd=WVeRr
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.WVeRj.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,WVeRj,env=WVeRr):
  WVeRy(RDSDatabase,self).__init__(WVeRj,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,WVeRj,env=WVeRr):
  WVeRy(RDSCluster,self).__init__(WVeRj,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,WVeRj,env=WVeRr):
  WVeRy(AppSyncAPI,self).__init__(WVeRj,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,WVeRj,env=WVeRr):
  WVeRy(AmplifyApp,self).__init__(WVeRj,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,WVeRj,env=WVeRr):
  WVeRy(ElastiCacheCluster,self).__init__(WVeRj,env=env)
class TransferServer(BaseComponent):
 def __init__(self,WVeRj,env=WVeRr):
  WVeRy(TransferServer,self).__init__(WVeRj,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,WVeRj,env=WVeRr):
  WVeRy(CloudFrontDistribution,self).__init__(WVeRj,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,WVeRj,env=WVeRr):
  WVeRy(CodeCommitRepository,self).__init__(WVeRj,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

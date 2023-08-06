import json
JhuKy=None
JhuKd=object
JhuKo=Exception
JhuKH=bool
JhuKt=False
JhuKi=int
JhuKP=str
JhuKX=set
JhuKN=property
JhuKn=classmethod
JhuKR=True
JhuKL=staticmethod
JhuKO=open
JhuKY=map
JhuKV=range
JhuKI=len
JhuKS=getattr
JhuKW=type
JhuKQ=isinstance
JhuKT=list
import logging
import os
import re
import traceback
from typing import Dict,List,Set
from zipfile import ZipFile
import requests
import yaml
from dulwich import porcelain
from dulwich.client import get_transport_and_path_from_url
from dulwich.repo import Repo
from localstack import config,constants
from localstack.utils.common import(chmod_r,clone,cp_r,disk_usage,download,format_number,is_command_available,load_file,mkdir,new_tmp_dir,new_tmp_file,retry,rm_rf,run,safe_requests,save_file,to_bytes,to_str,unzip)
from localstack.utils.docker_utils import DOCKER_CLIENT
from localstack.utils.testutil import create_zip_file
from localstack_ext import config as ext_config
from localstack_ext.bootstrap.licensing import get_auth_headers
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,api_states_traverse
from localstack_ext.constants import API_PATH_PODS
LOG=logging.getLogger(__name__)
PERSISTED_FOLDERS=["api_states","dynamodb","kinesis"]
MERGE_STRATEGY_TWO_WAY="two way"
MERGE_STRATEGY_THREE_WAY="three way"
MERGE_STRATEGY_DISABLED="disabled"
class PodInfo:
 def __init__(self,name=JhuKy,pod_size=0):
  self.name=name
  self.pod_size=pod_size
  self.pod_size_compressed=0
  self.persisted_resource_names=[]
class CloudPodManager(JhuKd):
 BACKEND="_none_"
 def __init__(self,pod_name=JhuKy,config=JhuKy):
  self.pod_name=pod_name
  self._pod_config=config
 def init(self):
  raise JhuKo("Not implemented")
 def delete(self,remote:JhuKH)->JhuKH:
  raise JhuKo("Not implemented")
 def push(self,comment:JhuKP=JhuKy,three_way:JhuKH=JhuKt)->PodInfo:
  raise JhuKo("Not implemented")
 def push_overwrite(self,version:JhuKi,comment:JhuKP=JhuKy):
  pass
 def pull(self,inject_version_state:JhuKH=JhuKt,reset_state_before:JhuKH=JhuKt,lazy:JhuKH=JhuKt):
  raise JhuKo("Not implemented")
 def commit(self,message:JhuKP=JhuKy):
  raise JhuKo("Not implemented")
 def inject(self,version:JhuKi,reset_state:JhuKH)->JhuKH:
  raise JhuKo("Not implemented")
 def list_versions(self)->List[JhuKP]:
  raise JhuKo("Not implemented")
 def version_info(self,version:JhuKi):
  raise JhuKo("Not implemented")
 def version_metamodel(self,version:JhuKi)->Dict:
  raise JhuKo("Not implemented")
 def set_version(self,version:JhuKi,inject_version_state:JhuKH,reset_state:JhuKH,commit_before:JhuKH):
  raise JhuKo("Not implemented")
 def list_version_commits(self,version:JhuKi)->List[JhuKP]:
  raise JhuKo("Not implemented")
 def get_commit_diff(self,version:JhuKi,commit:JhuKi)->Dict:
  raise JhuKo("Not implemented")
 def register_remote(self,pod_name:JhuKP,ci_pod:JhuKH)->JhuKH:
  raise JhuKo("Not implemented")
 def rename_pod(self,current_pod_name,new_pod_name)->JhuKH:
  raise JhuKo("Not implemented")
 def list_pods(self,fetch_remote:JhuKH)->Set[JhuKP]:
  raise JhuKo("Not implemented")
 def restart_container(self):
  LOG.info("Restarting LocalStack instance with updated persistence state - this may take some time ...")
  data={"action":"restart"}
  url="%s/health"%config.get_edge_url()
  try:
   requests.post(url,data=json.dumps(data))
  except requests.exceptions.ConnectionError:
   pass
  def check_status():
   LOG.info("Waiting for LocalStack instance to be fully initialized ...")
   response=requests.get(url)
   content=json.loads(to_str(response.content))
   statuses=[v for k,v in content["services"].items()]
   assert JhuKX(statuses)=={"running"}
  retry(check_status,sleep=3,retries=10)
 @JhuKN
 def pod_config(self):
  return self._pod_config or PodConfigManager.pod_config(self.pod_name)
 @JhuKn
 def get(cls,pod_name,pre_config=JhuKy):
  pod_config=pre_config if pre_config else PodConfigManager.pod_config(pod_name)
  backend=pod_config.get("backend")
  for clazz in cls.__subclasses__():
   if clazz.BACKEND==backend:
    return clazz(pod_name=pod_name,config=pod_config)
  raise JhuKo('Unable to find Cloud Pod manager implementation type "%s"'%backend)
 def deploy_pod_into_instance(self,pod_path):
  delete_pod_zip=JhuKt
  if os.path.isdir(pod_path):
   tmpdir=new_tmp_dir()
   for folder in PERSISTED_FOLDERS:
    src_folder=os.path.join(pod_path,folder)
    if not os.path.exists(src_folder):
     continue
    tgt_folder=os.path.join(tmpdir,folder)
    cp_r(src_folder,tgt_folder,rm_dest_on_conflict=JhuKR)
   pod_path=create_zip_file(tmpdir)
   rm_rf(tmpdir)
   delete_pod_zip=JhuKR
  zip_content=load_file(pod_path,mode="rb")
  url=get_pods_endpoint()
  result=requests.post(url,data=zip_content)
  if result.status_code>=400:
   raise JhuKo("Unable to restore pod state via local pods management API %s (code %s): %s"%(url,result.status_code,result.content))
  if delete_pod_zip:
   rm_rf(pod_path)
  else:
   return pod_path
 @JhuKL
 def get_state_zip_from_instance(get_content=JhuKt):
  url=f"{get_pods_endpoint()}/state"
  result=requests.get(url)
  if result.status_code>=400:
   raise JhuKo("Unable to get local pod state via management API %s (code %s): %s"%(url,result.status_code,result.content))
  if get_content:
   return result.content
  zip_file=f"{new_tmp_file()}.zip"
  save_file(zip_file,result.content)
  return zip_file
 def get_pod_info(self,pod_data_dir:JhuKP=JhuKy):
  result=PodInfo(self.pod_name)
  if pod_data_dir:
   result.pod_size=disk_usage(pod_data_dir)
   result.persisted_resource_names=get_persisted_resource_names(pod_data_dir)
  return result
class CloudPodManagerCPVCS(CloudPodManager):
 BACKEND="cpvcs"
 @JhuKL
 def parse_pod_name_from_qualifying_name(qualifying_name:JhuKP)->JhuKP:
  return qualifying_name.split(PODS_NAMESPACE_DELIM,1)[1]
 @JhuKL
 def _prepare_archives_from_presigned_urls(content):
  zip_path_version_space=new_tmp_file()
  presigned_urls=content.get("presigned_urls")
  version_space_url=presigned_urls.get("presigned_version_space_url")
  download(url=version_space_url,path=zip_path_version_space)
  zip_paths_state_archives={}
  zip_paths_meta_archives={}
  meta_and_state_urls=presigned_urls.get("presigned_meta_state_urls")
  for version_no,meta_and_state_url in meta_and_state_urls.items():
   zip_path_meta_archive=new_tmp_file()
   zip_path_state_archive=new_tmp_file()
   meta_url=meta_and_state_url["meta"]
   state_url=meta_and_state_url["state"]
   download(meta_url,zip_path_meta_archive)
   download(state_url,zip_path_state_archive)
   zip_paths_meta_archives[version_no]=zip_path_meta_archive
   zip_paths_state_archives[version_no]=zip_path_state_archive
  return zip_path_version_space,zip_paths_meta_archives,zip_paths_state_archives
 @JhuKL
 def _get_max_version_for_pod_from_platform(pod_name:JhuKP,auth_headers):
  url=CloudPodManagerCPVCS.create_platform_url(f"{pod_name}/info/max-version")
  response=safe_requests.get(url=url,headers=auth_headers)
  if response.status_code!=200:
   LOG.warning("Failed to get version information from platform... aborting")
   return
  content=json.loads(response.content)
  remote_max_ver=JhuKi(content["max_ver"])
  return remote_max_ver
 @JhuKL
 def _add_state_files_func(**kwargs):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  dir_name=kwargs.get("dir_name")
  file_name=kwargs.get("fname")
  region=kwargs.get("region")
  service_name=kwargs.get("service_name")
  cpvcs_api.create_state_file_from_fs(path=dir_name,file_name=file_name,service=service_name,region=region)
 def _upload_version_and_product_space(self,presigned_urls):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  presigned_version_space_url=presigned_urls.get("presigned_version_space_url")
  version_space_archive=cpvcs_api.create_version_space_archive()
  with JhuKO(version_space_archive,"rb")as version_space_content:
   self.upload_content(presigned_version_space_url,version_space_content.read())
  presigned_meta_state_urls=presigned_urls.get("presigned_meta_state_urls")
  rm_rf(version_space_archive)
  for version_no,urls in presigned_meta_state_urls.items():
   meta_presigned_url=urls["meta"]
   meta_archive=cpvcs_api.PodFilePaths.get_version_meta_archive(version_no)
   with JhuKO(meta_archive,"rb")as meta_archive_content:
    self.upload_content(meta_presigned_url,meta_archive_content)
   state_presigned_url=urls["state"]
   state_archive=cpvcs_api.PodFilePaths.get_version_state_archive(version_no)
   with JhuKO(state_archive,"rb")as state_archive_content:
    self.upload_content(state_presigned_url,state_archive_content)
 def _add_state_to_cpvs_store(self):
  from localstack_ext.bootstrap.cpvcs.utils.common import config_context
  if not config_context.is_initialized():
   LOG.debug("No CPVCS instance detected - Could not push")
   return
  zip_file=self.get_state_zip_from_instance()
  tmp_dir=new_tmp_dir()
  with ZipFile(zip_file,"r")as state_zip:
   state_zip.extractall(tmp_dir)
   api_states_path=os.path.join(tmp_dir,API_STATES_DIR)
   api_states_traverse(api_states_path=api_states_path,side_effect=CloudPodManagerCPVCS._add_state_files_func,mutables=JhuKy)
  rm_rf(zip_file)
  rm_rf(tmp_dir)
 def _pull_versions(self,auth_headers,required_versions:JhuKP):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  url=self.create_platform_url(f"{self.pod_name}?versions={required_versions}")
  response=safe_requests.get(url=url,headers=auth_headers)
  if response.status_code!=200:
   LOG.warning("Failed to pull requested versions from platform")
   return
  content=json.loads(response.content)
  archives=CloudPodManagerCPVCS._prepare_archives_from_presigned_urls(content)
  zip_path_version_space=archives[0]
  zip_paths_meta_archives=archives[1]
  zip_paths_state_archives=archives[2]
  cpvcs_api.merge_from_remote(version_space_archive=zip_path_version_space,meta_archives=zip_paths_meta_archives,state_archives=zip_paths_state_archives)
 def _clone_pod(self,auth_headers,lazy:JhuKH=JhuKt):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  url=self.create_platform_url(f"{self.pod_name}/clone")
  if lazy:
   url+="?lazy=True"
  response=safe_requests.get(url,headers=auth_headers)
  if response.status_code!=200:
   LOG.warning(f"Failed to clone requested pod {self.pod_name}: {response.content}")
   return
  content=json.loads(response.content)
  archives=CloudPodManagerCPVCS._prepare_archives_from_presigned_urls(content)
  zip_path_version_space=archives[0]
  zip_paths_meta_archives=archives[1]
  zip_paths_state_archives=archives[2]
  remote_info={"storage_uuid":content.get("storage_uuid"),"qualifying_name":content.get("pod_name")}
  pod_name=CloudPodManagerCPVCS.parse_pod_name_from_qualifying_name(remote_info["qualifying_name"])
  cpvcs_api.init_remote(pod_name=pod_name,version_space_archive=zip_path_version_space,meta_archives=zip_paths_meta_archives,state_archives=zip_paths_state_archives,remote_info=remote_info)
 def init(self):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.init(pod_name=self.pod_name)
 def delete(self,remote:JhuKH)->JhuKH:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_dir=cpvcs_api.config_context.cpvcs_root_dir
  pod_dir=os.path.join(cpvcs_dir,self.pod_name)
  if os.path.isdir(pod_dir):
   rm_rf(pod_dir)
   return JhuKR
  if remote:
   pass
  return JhuKt
 def _push_to_remote(self,url:JhuKP):
  auth_headers=get_auth_headers()
  response=safe_requests.put(url=url,headers=auth_headers)
  if response.status_code!=200:
   LOG.warning("Failed to get presigned URLs to upload new version.. aborting")
   return
  content=json.loads(response.content)
  presigned_urls=content.get("presigned_urls")
  self._upload_version_and_product_space(presigned_urls)
 def push(self,comment:JhuKP=JhuKy,three_way:JhuKH=JhuKt)->PodInfo:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod_context(self.pod_name)
  self._add_state_to_cpvs_store()
  if cpvcs_api.is_remotely_managed():
   auth_headers=get_auth_headers()
   local_max_ver=cpvcs_api.get_max_version_no()
   remote_max_ver=CloudPodManagerCPVCS._get_max_version_for_pod_from_platform(pod_name=self.pod_name,auth_headers=auth_headers)
   if local_max_ver<remote_max_ver:
    self.pull()
   cpvcs_api.push(comment=comment)
   url=CloudPodManagerCPVCS.create_platform_url(f"push/{self.pod_name}?version={local_max_ver + 1}")
   self._push_to_remote(url=url)
  else:
   created_version=cpvcs_api.push(comment=comment)
   LOG.debug(f"Created new version: {created_version}")
  return PodInfo()
 def push_overwrite(self,version:JhuKi,comment:JhuKP=JhuKy):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod_context(pod_name=self.pod_name)
  if version>cpvcs_api.get_max_version_no():
   LOG.warning(f"Version {version} does not exist")
   return JhuKt
  self._add_state_to_cpvs_store()
  cpvcs_api.push_overwrite(version=version,comment=comment)
  if cpvcs_api.is_remotely_managed():
   url=CloudPodManagerCPVCS.create_platform_url(f"push-overwrite/{self.pod_name}?version={version}")
   self._push_to_remote(url=url)
  return JhuKR
 def pull(self,inject_version_state:JhuKH=JhuKt,reset_state_before:JhuKH=JhuKt,lazy:JhuKH=JhuKt):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  auth_headers=get_auth_headers()
  if self.pod_name in cpvcs_api.list_locally_available_pods(show_remote_or_local=JhuKt):
   cpvcs_api.set_pod_context(self.pod_name)
   remote_max_ver=CloudPodManagerCPVCS._get_max_version_for_pod_from_platform(self.pod_name,auth_headers)
   if not remote_max_ver:
    return
   current_max_ver=cpvcs_api.get_max_version_no()
   if remote_max_ver==current_max_ver:
    LOG.info("No new version available remotely. Nothing to pull")
    return
   if not lazy:
    required_versions=",".join(JhuKY(lambda ver:JhuKP(ver),JhuKV(current_max_ver+1,remote_max_ver+1)))
   else:
    required_versions=current_max_ver
   self._pull_versions(auth_headers=auth_headers,required_versions=required_versions)
  else:
   self._clone_pod(auth_headers=auth_headers,lazy=lazy)
 def commit(self,message:JhuKP=JhuKy):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod_context(self.pod_name)
  self._add_state_to_cpvs_store()
  completed_revision=cpvcs_api.commit(message=message)
  LOG.debug(f"Completed revision: {completed_revision}")
 def _download_version_product(self,version:JhuKi,retain:JhuKH=JhuKt)->Dict[JhuKP,JhuKP]:
  content=self._get_presigned_url_for_version_product(version=version)
  state_url=content.get("presigned_url_state")
  metadata_url=content.get("presigned_url_metadata")
  tmp_state_archive=new_tmp_file()
  tmp_metadata_archive=new_tmp_file()
  download(state_url,tmp_state_archive)
  download(metadata_url,tmp_metadata_archive)
  if retain:
   from localstack_ext.bootstrap.cpvcs.utils.remote_utils import(extract_meta_and_state_archives)
   extract_meta_and_state_archives(meta_archives={version:tmp_metadata_archive},state_archives={version:tmp_state_archive})
  return{"metadata_archive":tmp_metadata_archive,"state_archive":tmp_state_archive}
 def _get_presigned_url_for_version_product(self,version:JhuKi)->Dict:
  url=self.create_platform_url(f"{self.pod_name}/version/product")
  if version!=-1:
   url+=f"?version={version}"
  auth_headers=get_auth_headers()
  response=safe_requests.get(url,headers=auth_headers)
  if response.status_code>=300:
   LOG.warning(f"Failed to retrieve presigned url from remote for version {version} of pod {self.pod_name}")
   return
  return json.loads(response.content)
 def _inject_from_remote(self,version:JhuKi,retain:JhuKH=JhuKt)->JhuKH:
  from localstack_ext.bootstrap.cpvcs.utils.remote_utils import(extract_meta_and_state_archives)
  content=self._get_presigned_url_for_version_product(version=version)
  state_url=content.get("presigned_url_state")
  tmp_state_archive=new_tmp_file()
  download(state_url,tmp_state_archive)
  self.deploy_pod_into_instance(tmp_state_archive)
  if not retain:
   rm_rf(tmp_state_archive)
   return JhuKR
  metadata_url=content.get("presigned_url_metadata")
  tmp_metadata_archive=new_tmp_file()
  download(metadata_url,tmp_metadata_archive)
  extract_meta_and_state_archives(meta_archives={version:tmp_metadata_archive},state_archives={version:tmp_state_archive})
  return JhuKR
 def inject(self,version:JhuKi,reset_state:JhuKH)->JhuKH:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  if not cpvcs_api.config_context.pod_exists_locally(self.pod_name):
   LOG.debug(f"Pod {self.pod_name} does not exist locally. Requesting state from remote..")
   state_archive_path=self._download_version_product(version=version).get("state_archive")
  else:
   cpvcs_api.set_pod_context(self.pod_name)
   if version==-1:
    version=cpvcs_api.get_max_version_no()
   state_archive_path=cpvcs_api.PodFilePaths.get_version_state_archive(version)
   if not state_archive_path and cpvcs_api.is_remotely_managed():
    LOG.debug("Fetching requested archive from remote..")
    product_archive_path=self._download_version_product(version=version,retain=JhuKR)
    if not product_archive_path:
     return JhuKt
    state_archive_path=cpvcs_api.PodFilePaths.get_version_state_archive(version)
  if reset_state:
   reset_local_state(reset_data_dir=JhuKR,exclude_from_reset=["dynamodb","kinesis","stepfunctions"])
  self.deploy_pod_into_instance(state_archive_path)
  return JhuKR
 def list_versions(self)->List[JhuKP]:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod_context(self.pod_name)
  version_list=cpvcs_api.list_versions()
  return version_list
 def version_info(self,version:JhuKi):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod_context(self.pod_name)
  if version==-1:
   version=cpvcs_api.get_max_version_no()
  version_info=cpvcs_api.get_version_info(version)
  return version_info
 def version_metamodel(self,version:JhuKi)->Dict:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod_context(self.pod_name)
  if version==-1:
   version=cpvcs_api.get_max_version_no()
  result=cpvcs_api.CommitMetamodelUtils.create_metamodel_from_state_files(version=version)
  if not result and cpvcs_api.is_remotely_managed():
   self._download_version_product(version=version,retain=JhuKR)
   result=cpvcs_api.CommitMetamodelUtils.create_metamodel_from_state_files(version=version)
  return result[0]
 def set_version(self,version:JhuKi,inject_version_state:JhuKH,reset_state:JhuKH,commit_before:JhuKH):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod_context(self.pod_name)
  version_exists=cpvcs_api.set_active_version(version_no=version,commit_before=commit_before)
  if not version_exists:
   LOG.warning(f"Could not find version {version}")
  if inject_version_state:
   self.inject(version=version,reset_state=reset_state)
 def list_version_commits(self,version:JhuKi)->List[JhuKP]:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod_context(self.pod_name)
  commits=cpvcs_api.list_version_commits(version_no=version)
  return commits
 def get_commit_diff(self,version:JhuKi,commit:JhuKi)->Dict:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod_context(self.pod_name)
  commit_diff=cpvcs_api.CommitMetamodelUtils.get_commit_diff(version_no=version,commit_no=commit)
  return commit_diff
 def register_remote(self,pod_name:JhuKP,ci_pod:JhuKH=JhuKt)->JhuKH:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod_context(self.pod_name)
  max_ver=cpvcs_api.get_max_version_no()
  if max_ver==0:
   cpvcs_api.push("Init Version")
   max_ver=1
  auth_headers=get_auth_headers()
  url=self.create_platform_url("register")
  data={"pod_name":self.pod_name,"max_ver":max_ver,"ci_pod":ci_pod}
  data=json.dumps(data)
  response=safe_requests.post(url,data,headers=auth_headers)
  if response.status_code!=200:
   LOG.warning(f"Failed to register pod {self.pod_name}: {response.content}")
   return JhuKt
  content=json.loads(response.content)
  remote_info={"storage_uuid":content.get("storage_uuid"),"qualifying_name":content.get("pod_name")}
  presigned_urls=content.get("presigned_urls")
  self._upload_version_and_product_space(presigned_urls)
  cpvcs_api.register_remote(remote_info=remote_info)
  return JhuKR
 def rename_pod(self,current_pod_name,new_pod_name)->JhuKH:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod_context(current_pod_name)
  if new_pod_name in cpvcs_api.list_locally_available_pods():
   LOG.warning(f"{new_pod_name} already exists locally")
   return JhuKt
  if cpvcs_api.is_remotely_managed():
   auth_headers=get_auth_headers()
   url=self.create_platform_url(f"{current_pod_name}/rename")
   data={"new_pod_name":new_pod_name}
   data=json.dumps(data)
   response=safe_requests.put(url,data,headers=auth_headers)
   if response.status_code!=200:
    LOG.warning(f"Failed to rename {current_pod_name} to {new_pod_name}: {response.content}")
    return JhuKt
  cpvcs_api.rename_pod(new_pod_name)
  return JhuKR
 def list_pods(self,fetch_remote:JhuKH)->Set[JhuKP]:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  result=cpvcs_api.list_locally_available_pods()
  if fetch_remote:
   auth_headers=get_auth_headers()
   url=self.create_platform_url("pods")
   response=safe_requests.get(url,headers=auth_headers)
   content=json.loads(response.content)
   for remote_pod in content.get("registered_pods")or[]:
    result.add(f"remote/{remote_pod}")
  return result
 @JhuKn
 def upload_content(cls,presigned_url:JhuKP,zip_data_content):
  res=safe_requests.put(presigned_url,data=zip_data_content)
  if res.status_code>=400:
   raise JhuKo("Unable to upload pod state to S3 (code %s): %s"%(res.status_code,res.content))
  return res
 @JhuKL
 def create_platform_url(request:JhuKP)->JhuKP:
  base_url="%s/cpvcs"%constants.API_ENDPOINT
  return os.path.join(base_url,request)
class CloudPodManagerFilesystem(CloudPodManager):
 BACKEND="file"
 def push(self,comment:JhuKP=JhuKy,three_way:JhuKH=JhuKt)->PodInfo:
  local_folder=self.target_folder()
  print('Pushing state of cloud pod "%s" to local folder: %s'%(self.pod_name,local_folder))
  mkdir(local_folder)
  zip_file=self.get_state_zip_from_instance()
  unzip(zip_file,local_folder)
  chmod_r(local_folder,0o777)
  result=self.get_pod_info(local_folder)
  print("Done.")
  return result
 def pull(self,inject_version_state:JhuKH=JhuKt,reset_state_before:JhuKH=JhuKt,lazy:JhuKH=JhuKt):
  local_folder=self.target_folder()
  if not os.path.exists(local_folder):
   print('WARN: Local path of cloud pod "%s" does not exist: %s'%(self.pod_name,local_folder))
   return
  print('Pulling state of cloud pod "%s" from local folder: %s'%(self.pod_name,local_folder))
  self.deploy_pod_into_instance(local_folder)
 def target_folder(self):
  local_folder=re.sub(r"^file://","",self.pod_config.get("url",""))
  return local_folder
class CloudPodManagerManaged(CloudPodManager):
 BACKEND="managed"
 def push(self,comment:JhuKP=JhuKy,three_way:JhuKH=JhuKt)->PodInfo:
  zip_data_content=self.get_state_zip_from_instance(get_content=JhuKR)
  print('Pushing state of cloud pod "%s" to backend server (%s KB)'%(self.pod_name,format_number(JhuKI(zip_data_content)/1000.0)))
  self.push_content(self.pod_name,zip_data_content)
  print("Done.")
  result=self.get_pod_info()
  result.pod_size_compressed=JhuKI(zip_data_content)
  return result
 def pull(self,inject_version_state:JhuKH=JhuKt,reset_state_before:JhuKH=JhuKt,lazy:JhuKH=JhuKt):
  presigned_url=self.presigned_url(self.pod_name,"pull")
  print('Pulling state of cloud pod "%s" from managed storage'%self.pod_name)
  zip_path=new_tmp_file()
  download(presigned_url,zip_path)
  self.deploy_pod_into_instance(zip_path)
  rm_rf(zip_path)
 @JhuKL
 def presigned_url(pod_name:JhuKP,mode:JhuKP)->JhuKP:
  data={"pod_name":pod_name,"mode":mode}
  data=json.dumps(data)
  auth_headers=get_auth_headers()
  url="%s/cloudpods/data"%constants.API_ENDPOINT
  if ext_config.SYNC_POD_VERSION:
   url=f"{url}?version={ext_config.SYNC_POD_VERSION}"
  response=safe_requests.post(url,data,headers=auth_headers)
  content=response.content
  if response.status_code>=400:
   raise JhuKo("Unable to get cloud pod presigned URL (code %s): %s"%(response.status_code,content))
  content=json.loads(to_str(content))
  return content["presignedURL"]
 @JhuKn
 def push_content(cls,pod_name,zip_data_content):
  presigned_url=cls.presigned_url(pod_name,"push")
  res=safe_requests.put(presigned_url,data=zip_data_content)
  if res.status_code>=400:
   raise JhuKo("Unable to push pod state to API (code %s): %s"%(res.status_code,res.content))
  return res
class CloudPodManagerGit(CloudPodManager):
 BACKEND="git"
 def push(self,comment:JhuKP=JhuKy,three_way:JhuKH=JhuKt):
  repo=self.local_repo()
  branch=to_bytes(self.pod_config.get("branch"))
  remote_location=self.pod_config.get("url")
  try:
   porcelain.pull(repo,remote_location,refspecs=branch)
  except JhuKo as e:
   if self.has_git_cli():
    run("cd %s; git checkout %s; git pull"%(to_str(branch),self.clone_dir))
   else:
    LOG.info("Unable to pull repo: %s %s",e,traceback.format_exc())
  zip_file=self.get_state_zip_from_instance()
  tmp_data_dir=new_tmp_dir()
  unzip(zip_file,tmp_data_dir)
  is_empty_repo=b"HEAD" not in repo or repo.refs.allkeys()=={b"HEAD"}
  if is_empty_repo:
   LOG.debug("Initializing empty repository %s"%self.clone_dir)
   init_file=os.path.join(self.clone_dir,".init")
   save_file(init_file,"")
   porcelain.add(repo,init_file)
   porcelain.commit(repo,message="Initial commit")
  if branch not in repo:
   porcelain.branch_create(repo,branch,force=JhuKR)
  self.switch_branch(branch)
  for folder in PERSISTED_FOLDERS:
   LOG.info("Copying persistence folder %s to local git repo %s"%(folder,self.clone_dir))
   src_folder=os.path.join(tmp_data_dir,folder)
   tgt_folder=os.path.join(self.clone_dir,folder)
   cp_r(src_folder,tgt_folder)
   files=tgt_folder
   if os.path.isdir(files):
    files=[os.path.join(root,f)for root,_,files in os.walk(tgt_folder)for f in files]
   if files:
    porcelain.add(repo,files)
  porcelain.commit(repo,message="Update cloud pod state")
  try:
   porcelain.push(repo,remote_location,branch)
  except JhuKo:
   if not self.has_git_cli():
    raise
   run("cd %s; git push origin %s"%(self.clone_dir,to_str(branch)))
  result=self.get_pod_info(tmp_data_dir)
  return result
 def pull(self,inject_version_state:JhuKH=JhuKt,reset_state_before:JhuKH=JhuKt,lazy:JhuKH=JhuKt):
  repo=self.local_repo()
  client,path=self.client()
  remote_refs=client.fetch(path,repo)
  branch=self.pod_config.get("branch")
  remote_ref=b"refs/heads/%s"%to_bytes(branch)
  if remote_ref not in remote_refs:
   raise JhuKo('Unable to find branch "%s" in remote git repo'%branch)
  remote_location=self.pod_config.get("url")
  self.switch_branch(branch)
  branch_ref=b"refs/heads/%s"%to_bytes(branch)
  from dulwich.errors import HangupException
  try:
   porcelain.pull(repo,remote_location,branch_ref)
  except HangupException:
   pass
  self.deploy_pod_into_instance(self.clone_dir)
 def client(self):
  client,path=get_transport_and_path_from_url(self.pod_config.get("url"))
  return client,path
 def local_repo(self):
  self.clone_dir=JhuKS(self,"clone_dir",JhuKy)
  if not self.clone_dir:
   pod_dir_name=re.sub(r"(\s|/)+","",self.pod_name)
   self.clone_dir=os.path.join(config.dirs.tmp,"pods",pod_dir_name,"repo")
   mkdir(self.clone_dir)
   if not os.path.exists(os.path.join(self.clone_dir,".git")):
    porcelain.clone(self.pod_config.get("url"),self.clone_dir)
    self.switch_branch(self.pod_config.get("branch"))
  return Repo(self.clone_dir)
 def switch_branch(self,branch):
  repo=self.local_repo()
  if self.has_git_cli():
   return run("cd %s; git checkout %s"%(self.clone_dir,to_str(branch)))
  branch_ref=b"refs/heads/%s"%to_bytes(branch)
  if branch_ref not in repo.refs:
   branch_ref=b"refs/remotes/origin/%s"%to_bytes(branch)
  repo.reset_index(repo[branch_ref].tree)
  repo.refs.set_symbolic_ref(b"HEAD",branch_ref)
 def has_git_cli(self):
  return is_command_available("git")
class PodConfigManagerMeta(JhuKW):
 def __getattr__(cls,attr):
  def _call(*args,**kwargs):
   result=JhuKy
   for manager in cls.CHAIN:
    try:
     tmp=JhuKS(manager,attr)(*args,**kwargs)
     if tmp:
      if not result:
       result=tmp
      elif JhuKQ(tmp,JhuKT)and JhuKQ(result,JhuKT):
       result.extend(tmp)
    except JhuKo:
     if LOG.isEnabledFor(logging.DEBUG):
      LOG.exception("error during PodConfigManager call chain")
   if result is not JhuKy:
    return result
   raise JhuKo('Unable to run operation "%s" for local or remote configuration'%attr)
  return _call
class PodConfigManager(JhuKd,metaclass=PodConfigManagerMeta):
 CHAIN=[]
 @JhuKn
 def pod_config(cls,pod_name):
  pods=PodConfigManager.list_pods()
  pod_config=[pod for pod in pods if pod["pod_name"]==pod_name]
  if not pod_config:
   raise JhuKo('Unable to find config for pod named "%s"'%pod_name)
  return pod_config[0]
class PodConfigManagerLocal(JhuKd):
 CONFIG_FILE=".localstack.yml"
 def list_pods(self):
  local_pods=self._load_config(safe=JhuKR).get("pods",{})
  local_pods=[{"pod_name":k,"state":"Local Only",**v}for k,v in local_pods.items()]
  existing_names=JhuKX([pod["pod_name"]for pod in local_pods])
  result=[pod for pod in local_pods if pod["pod_name"]not in existing_names]
  return result
 def store_pod_metadata(self,pod_name,metadata):
  pass
 def _load_config(self,safe=JhuKt):
  try:
   return yaml.safe_load(to_str(load_file(self.CONFIG_FILE)))
  except JhuKo:
   if safe:
    return{}
   raise JhuKo('Unable to find and parse config file "%s"'%self.CONFIG_FILE)
class PodConfigManagerRemote(JhuKd):
 def list_pods(self):
  result=[]
  auth_headers=get_auth_headers()
  url="%s/cloudpods"%constants.API_ENDPOINT
  response=safe_requests.get(url,headers=auth_headers)
  content=response.content
  if response.status_code>=400:
   raise JhuKo("Unable to fetch list of pods from API (code %s): %s"%(response.status_code,content))
  remote_pods=json.loads(to_str(content)).get("cloudpods",[])
  remote_pods=[{"state":"Shared",**pod}for pod in remote_pods]
  result.extend(remote_pods)
  return result
 def store_pod_metadata(self,pod_name,metadata):
  auth_headers=get_auth_headers()
  metadata["pod_name"]=pod_name
  response=safe_requests.post("%s/cloudpods"%constants.API_ENDPOINT,json.dumps(metadata),headers=auth_headers)
  content=response.content
  if response.status_code>=400:
   raise JhuKo("Unable to store pod metadata in API (code %s): %s"%(response.status_code,content))
  return json.loads(to_str(content))
PodConfigManager.CHAIN.append(PodConfigManagerLocal())
PodConfigManager.CHAIN.append(PodConfigManagerRemote())
def init_cpvcs(pod_name:JhuKP,pre_config:Dict[JhuKP,JhuKP],**kwargs):
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 backend.init()
def delete_pod(pod_name:JhuKP,remote:JhuKH,pre_config:Dict[JhuKP,JhuKP])->JhuKH:
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 result=backend.delete(remote=remote)
 return result
def register_remote(pod_name:JhuKP,pre_config:Dict[JhuKP,JhuKP],**kwargs)->JhuKH:
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 result=backend.register_remote(pod_name=pod_name,ci_pod=pre_config.get("ci_pod",JhuKt))
 return result
def rename_pod(current_pod_name:JhuKP,new_pod_name:JhuKP,pre_config:Dict[JhuKP,JhuKP],**kwargs):
 backend=CloudPodManager.get(pod_name=current_pod_name,pre_config=pre_config)
 result=backend.rename_pod(current_pod_name=current_pod_name,new_pod_name=new_pod_name)
 return result
def list_pods_cpvcs(remote:JhuKH,pre_config:Dict[JhuKP,JhuKP],**kwargs)->List[JhuKP]:
 backend=CloudPodManager.get(pod_name="",pre_config=pre_config)
 result=backend.list_pods(fetch_remote=remote)
 return result
def commit_state(pod_name:JhuKP,pre_config:Dict[JhuKP,JhuKP],message:JhuKP=JhuKy,**kwargs):
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 backend.commit(message=message)
def inject_state(pod_name:JhuKP,version:JhuKi,reset_state:JhuKH,pre_config:Dict[JhuKP,JhuKP],**kwargs):
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 result=backend.inject(version=version,reset_state=reset_state)
 return result
def list_versions(pod_name:JhuKP,pre_config:Dict[JhuKP,JhuKP],**kwargs)->List[JhuKP]:
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 versions=backend.list_versions()
 return versions
def get_version_info(version:JhuKi,pod_name:JhuKP,pre_config:Dict[JhuKP,JhuKP],**kwargs):
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 info=backend.version_info(version=version)
 return info
def get_version_metamodel(version:JhuKi,pod_name:JhuKP,pre_config:Dict[JhuKP,JhuKP],**kwargs)->Dict:
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 metamodel=backend.version_metamodel(version=version)
 return metamodel
def set_version(version:JhuKi,inject_version_state:JhuKH,reset_state:JhuKH,commit_before:JhuKH,pod_name:JhuKP,pre_config:Dict[JhuKP,JhuKP],**kwargs)->JhuKH:
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 success=backend.set_version(version=version,inject_version_state=inject_version_state,reset_state=reset_state,commit_before=commit_before)
 return success
def list_version_commits(version:JhuKi,pod_name:JhuKP,pre_config:Dict[JhuKP,JhuKP])->List[JhuKP]:
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 commits=backend.list_version_commits(version=version)
 return commits
def get_commit_diff(version:JhuKi,commit:JhuKi,pod_name:JhuKP,pre_config:Dict[JhuKP,JhuKP])->Dict:
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 commit_diff=backend.get_commit_diff(version=version,commit=commit)
 return commit_diff
def push_overwrite(version:JhuKi,pod_name:JhuKP,comment:JhuKP,pre_config:Dict[JhuKP,JhuKP]):
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 backend.push_overwrite(version=version,comment=comment)
def push_state(pod_name,pre_config=JhuKy,squash_commits=JhuKt,comment=JhuKy,three_way=JhuKt,**kwargs):
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 pod_config=clone(backend.pod_config)
 pod_info=backend.push(comment=comment,three_way=three_way)
 pod_config["size"]=pod_info.pod_size or pod_info.pod_size_compressed
 pod_config["available_resources"]=pod_info.persisted_resource_names
 return pod_config
def get_pods_endpoint():
 edge_url=config.get_edge_url()
 return f"{edge_url}{API_PATH_PODS}"
def pull_state(pod_name,inject_version_state=JhuKt,reset_state_before=JhuKt,lazy=JhuKt,**kwargs):
 pre_config=kwargs.get("pre_config",JhuKy)
 if not pod_name:
  raise JhuKo("Need to specify a pod name")
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 backend.pull(inject_version_state=inject_version_state,reset_state_before=reset_state_before,lazy=lazy)
 print("Done.")
def reset_local_state(reset_data_dir=JhuKt,exclude_from_reset:List[JhuKP]=JhuKy):
 url=f"{get_pods_endpoint()}/state"
 if reset_data_dir:
  url+="/datadir"
 if exclude_from_reset:
  url+=f"?exclude={','.join(exclude_from_reset)}"
 print("Sending request to reset the service states in local instance ...")
 result=requests.delete(url)
 if result.status_code>=400:
  raise JhuKo("Unable to reset service state via local management API %s (code %s): %s"%(url,result.status_code,result.content))
 print("Done.")
def list_pods(args):
 return PodConfigManager.list_pods()
def get_data_dir_from_container()->JhuKP:
 try:
  details=DOCKER_CLIENT.inspect_container(config.MAIN_CONTAINER_NAME)
  mounts=details.get("Mounts")
  env=details.get("Config",{}).get("Env",[])
  data_dir_env=[e for e in env if e.startswith("DATA_DIR=")][0].partition("=")[2]
  try:
   data_dir_host=[m for m in mounts if m["Destination"]==data_dir_env][0]["Source"]
   data_dir_host=re.sub(r"^(/host_mnt)?",r"",data_dir_host)
   data_dir_env=data_dir_host
  except JhuKo:
   LOG.debug(f"No docker volume for data dir '{data_dir_env}' detected")
  return data_dir_env
 except JhuKo:
  LOG.warning('''Unable to determine DATA_DIR from LocalStack Docker container - please make sure $MAIN_CONTAINER_NAME is configured properly''')
def get_persisted_resource_names(data_dir)->List[JhuKP]:
 names=[]
 with os.scandir(data_dir)as entries:
  for entry in entries:
   if entry.is_dir()and entry.name!="api_states":
    names.append(entry.name)
 with os.scandir(os.path.join(data_dir,"api_states"))as entries:
  for entry in entries:
   if entry.is_dir()and JhuKI(os.listdir(entry.path))>0:
    names.append(entry.name)
 LOG.debug(f"Detected state files for the following APIs: {names}")
 return names
PODS_NAMESPACE_DELIM="-"
# Created by pyminifier (https://github.com/liftoff/pyminifier)

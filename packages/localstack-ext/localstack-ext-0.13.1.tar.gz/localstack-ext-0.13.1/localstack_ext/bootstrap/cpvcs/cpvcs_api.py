import json
TIdxq=set
TIdxc=None
TIdxO=open
TIdxC=str
TIdxN=bool
TIdxW=False
TIdxn=True
TIdxX=filter
TIdxo=int
TIdxJ=Exception
TIdxz=next
TIdxu=sorted
TIdxw=isinstance
import logging
import os
import shutil
import zipfile
from typing import Dict,List,Optional,Set,Tuple
from localstack.utils.common import mkdir,new_tmp_dir,rm_rf,save_file,short_uid,to_str
from moto.s3.models import FakeBucket
from moto.sqs.models import Queue
from localstack_ext.bootstrap.cpvcs.constants import(COMPRESSION_FORMAT,NIL_PTR,STATE_ZIP,VER_SYMLINK,VERSION_SERVICE_INFO_FILE,VERSION_SPACE_ARCHIVE)
from localstack_ext.bootstrap.cpvcs.models import Commit,Revision,StateFileRef,Version
from localstack_ext.bootstrap.cpvcs.obj_storage import default_storage as object_storage
from localstack_ext.bootstrap.cpvcs.utils.common import(PodFilePaths,config_context,read_file_from_archive,zip_directories)
from localstack_ext.bootstrap.cpvcs.utils.hash_utils import(compute_file_hash,compute_revision_hash,compute_version_archive_hash,random_hash)
from localstack_ext.bootstrap.cpvcs.utils.metamodel_utils import(CommitMetamodelUtils,MetamodelDelta,MetamodelDeltaMethod)
from localstack_ext.bootstrap.cpvcs.utils.remote_utils import(extract_meta_and_state_archives,merge_version_space,register_remote)
from localstack_ext.bootstrap.state_merge import merge_object_state
from localstack_ext.bootstrap.state_utils import(API_STATES_DIR,api_states_traverse,load_persisted_object,persist_object)
LOG=logging.getLogger(__name__)
def init(pod_name="My-Pod"):
 if config_context.pod_exists_locally(pod_name=pod_name):
  LOG.warning(f"Pod with name {pod_name} already exists locally")
  return
 config_context.set_pod_context(pod_name)
 def _create_internal_fs():
  mkdir(config_context.get_pod_root_dir())
  mkdir(config_context.get_ver_refs_path())
  mkdir(config_context.get_rev_refs_path())
  mkdir(config_context.get_ver_obj_store_path())
  mkdir(config_context.get_rev_obj_store_path())
  mkdir(config_context.get_delta_log_path())
 _create_internal_fs()
 r0_hash=random_hash()
 v0_hash=random_hash()
 r0=Revision(hash_ref=r0_hash,parent_ptr=NIL_PTR,creator=config_context.get_context_user(),rid=short_uid(),revision_number=0,state_files=TIdxq())
 v0=Version(hash_ref=v0_hash,parent_ptr=NIL_PTR,creator=config_context.get_context_user(),comment="Init version",active_revision_ptr=r0_hash,outgoing_revision_ptrs={r0_hash},incoming_revision_ptr=TIdxc,state_files=TIdxq(),version_number=0)
 rev_key,ver_key=object_storage.upsert_objects(r0,v0)
 ver_symlink=config_context.create_version_symlink(VER_SYMLINK.format(ver_no=v0.version_number),ver_key)
 with TIdxO(config_context.get_head_path(),"w")as fp:
  fp.write(ver_symlink)
 with TIdxO(config_context.get_max_ver_path(),"w")as fp:
  fp.write(ver_symlink)
 with TIdxO(config_context.get_known_ver_path(),"w")as fp:
  fp.write(ver_symlink)
 config_context.update_ver_log(author=config_context.get_context_user(),ver_no=v0.version_number,rev_id=r0.rid,rev_no=r0.revision_number)
 LOG.debug(f"Successfully initated CPVCS for pod at {config_context.get_pod_root_dir()}")
def init_remote(version_space_archive:TIdxC,meta_archives:Dict[TIdxC,TIdxC],state_archives:Dict[TIdxC,TIdxC],remote_info:Dict[TIdxC,TIdxC],pod_name:TIdxC):
 config_context.set_pod_context(pod_name=pod_name)
 mkdir(config_context.get_pod_root_dir())
 with zipfile.ZipFile(version_space_archive)as version_space_zip:
  version_space_zip.extractall(config_context.get_pod_root_dir())
  LOG.debug("Successfully extracted version space zip")
 rm_rf(version_space_archive)
 extract_meta_and_state_archives(meta_archives=meta_archives,state_archives=state_archives)
 max_ver=_get_max_version()
 ver_symlink=config_context.create_version_symlink(name=VER_SYMLINK.format(ver_no=max_ver.version_number))
 with TIdxO(config_context.get_head_path(),"w")as fp:
  fp.write(ver_symlink)
 register_remote(remote_info=remote_info)
def merge_from_remote(version_space_archive:TIdxC,meta_archives:Dict[TIdxC,TIdxC],state_archives:Dict[TIdxC,TIdxC]):
 merge_version_space(version_space_archive)
 extract_meta_and_state_archives(meta_archives=meta_archives,state_archives=state_archives)
def is_remotely_managed()->TIdxN:
 return config_context.is_remotly_managed()
def set_pod_context(pod_name:TIdxC):
 config_context.set_pod_context(pod_name)
def rename_pod(new_pod_name:TIdxC)->TIdxN:
 if config_context.pod_exists_locally(new_pod_name):
  LOG.warning(f"{new_pod_name} already exists locally")
  return TIdxW
 config_context.rename_pod(new_pod_name)
 return TIdxn
def list_locally_available_pods(show_remote_or_local:TIdxN=TIdxn)->Set[TIdxC]:
 mkdir(config_context.cpvcs_root_dir)
 available_pods=os.listdir(config_context.cpvcs_root_dir)
 if not show_remote_or_local:
  return TIdxq(available_pods)
 result=TIdxq()
 for available_pod in available_pods:
  pod_name=(f"remote/{available_pod}" if config_context.is_remotly_managed(available_pod)else f"local/{available_pod}")
  result.add(pod_name)
 return result
def create_state_file_from_fs(path:TIdxC,file_name:TIdxC,service:TIdxC,region:TIdxC)->TIdxC:
 file_path=os.path.join(path,file_name)
 key=compute_file_hash(file_path)
 rel_path=path.split(f"{API_STATES_DIR}/")[1]
 shutil.copy(file_path,os.path.join(config_context.get_obj_store_path(),key))
 state_file=StateFileRef(hash_ref=key,rel_path=rel_path,file_name=file_name,size=os.path.getsize(file_path),service=service,region=region)
 _add_state_file_to_expansion_point(state_file)
 return key
def _create_state_file_from_in_memory_blob(blob)->TIdxC:
 tmp_file_name=random_hash()
 tmp_dest=os.path.join(config_context.get_obj_store_path(),tmp_file_name)
 persist_object(blob,tmp_dest)
 key=compute_file_hash(tmp_dest)
 dest=os.path.join(config_context.get_obj_store_path(),key)
 os.rename(tmp_dest,dest)
 return key
def _get_state_file_path(key:TIdxC)->TIdxC:
 file_path=os.path.join(config_context.get_obj_store_path(),key)
 if os.path.isfile(file_path):
  return file_path
 LOG.warning(f"No state file with found with key: {key}")
def _add_state_file_to_expansion_point(state_file:StateFileRef):
 revision,_=_get_expansion_point_with_head()
 updated_state_files=TIdxq(TIdxX(lambda sf:not sf.congruent(state_file),revision.state_files))
 updated_state_files.add(state_file)
 revision.state_files=updated_state_files
 object_storage.upsert_objects(revision)
def list_state_files(key:TIdxC)->Optional[TIdxC]:
 cpvcs_obj=object_storage.get_revision_or_version_by_key(key)
 if cpvcs_obj:
  return cpvcs_obj.state_files_info()
 LOG.debug(f"No Version or Revision associated to {key}")
def get_version_info(version_no:TIdxo)->Dict[TIdxC,TIdxC]:
 archive_path=PodFilePaths.get_version_meta_archive(version_no)
 if not archive_path:
  LOG.warning(f"No Info found for version {version_no}")
  return
 result=read_file_from_archive(archive_path,VERSION_SERVICE_INFO_FILE)
 result=json.loads(to_str(result or "{}"))
 return result
def commit(message:TIdxC=TIdxc)->Revision:
 curr_expansion_point,head_version=_get_expansion_point_with_head()
 curr_expansion_point_hash=compute_revision_hash(curr_expansion_point)
 curr_expansion_point_parent_state_files=TIdxq()
 if curr_expansion_point.parent_ptr!=NIL_PTR:
  referenced_by_version=TIdxc
  curr_expansion_point_parent=object_storage.get_revision_by_key(curr_expansion_point.parent_ptr)
  curr_expansion_point_parent_state_files=curr_expansion_point_parent.state_files
  curr_expansion_point_parent.assoc_commit.head_ptr=curr_expansion_point_hash
  object_storage.upsert_objects(curr_expansion_point_parent)
 else:
  referenced_by_version=head_version.hash_ref
 object_storage.update_revision_key(curr_expansion_point.hash_ref,curr_expansion_point_hash,referenced_by_version)
 curr_expansion_point.hash_ref=curr_expansion_point_hash
 new_expansion_point=Revision(hash_ref=random_hash(),state_files=TIdxq(),parent_ptr=curr_expansion_point_hash,creator=curr_expansion_point.creator,rid=short_uid(),revision_number=curr_expansion_point.revision_number+1)
 delta_log_ptr=create_delta_log(curr_expansion_point_parent_state_files,curr_expansion_point.state_files)
 assoc_commit=Commit(tail_ptr=curr_expansion_point.hash_ref,head_ptr=new_expansion_point.hash_ref,message=message,delta_log_ptr=delta_log_ptr)
 curr_expansion_point.assoc_commit=assoc_commit
 object_storage.upsert_objects(new_expansion_point,curr_expansion_point)
 config_context.update_ver_log(author=new_expansion_point.creator,ver_no=head_version.version_number,rev_id=new_expansion_point.rid,rev_no=new_expansion_point.revision_number)
 return curr_expansion_point
def create_version_space_archive()->TIdxC:
 zip_dest=os.path.join(config_context.get_pod_root_dir(),VERSION_SPACE_ARCHIVE)
 rm_rf(zip_dest)
 result=zip_directories(zip_dest=zip_dest,directories=config_context.get_version_space_dir_paths())
 with zipfile.ZipFile(result,"a")as archive:
  for version_space_file in config_context.get_version_space_file_paths():
   archive.write(version_space_file,arcname=os.path.basename(version_space_file))
 return result
def get_head()->Version:
 return object_storage.get_version_by_key(config_context._get_head_key())
def _get_max_version()->Version:
 return object_storage.get_version_by_key(config_context.get_max_ver_key())
def get_max_version_no()->TIdxo:
 with TIdxO(config_context.get_max_ver_path())as fp:
  return TIdxo(os.path.basename(fp.readline()))
def _get_expansion_point_with_head()->Tuple[Revision,Version]:
 head_version=get_head()
 active_revision_root=object_storage.get_revision_by_key(head_version.active_revision_ptr)
 expansion_point=object_storage.get_terminal_revision(active_revision_root)
 return expansion_point,head_version
def push_overwrite(version:TIdxo,comment:TIdxC)->TIdxN:
 expansion_point,_=_get_expansion_point_with_head()
 if version>get_max_version_no():
  LOG.debug("Attempted to overwrite a non existing version.. Aborting")
  return TIdxW
 version_node=get_version_by_number(version)
 _create_state_directory(version_number=version,state_file_refs=expansion_point.state_files)
 metamodels_file=PodFilePaths.metamodel_file(expansion_point.revision_number)
 CommitMetamodelUtils.create_metadata_archive(version_node,overwrite=TIdxn,metamodels_file=metamodels_file)
 version_node.comment=comment
 object_storage.upsert_objects(version_node)
 return TIdxn
def push(comment:TIdxC=TIdxc,three_way:TIdxN=TIdxW)->Version:
 expansion_point,head_version=_get_expansion_point_with_head()
 max_version=_get_max_version()
 new_active_revision=Revision(hash_ref=random_hash(),state_files=TIdxq(),parent_ptr=NIL_PTR,creator=expansion_point.creator,rid=short_uid(),revision_number=0)
 new_max_version_no=max_version.version_number+1
 if head_version.version_number!=max_version.version_number:
  _merge_expansion_point_with_max(three_way=three_way)
 else:
  _create_state_directory(new_max_version_no,state_file_refs=expansion_point.state_files)
 new_version=Version(hash_ref=compute_version_archive_hash(new_max_version_no,PodFilePaths.get_version_state_archive(new_max_version_no)),state_files=TIdxq(),parent_ptr=max_version.hash_ref,creator=expansion_point.creator,comment=comment,active_revision_ptr=new_active_revision.hash_ref,outgoing_revision_ptrs={new_active_revision.hash_ref},incoming_revision_ptr=expansion_point.hash_ref,version_number=new_max_version_no)
 if expansion_point.parent_ptr!=NIL_PTR:
  expansion_point_parent=object_storage.get_revision_by_key(expansion_point.parent_ptr)
  state_from=expansion_point_parent.state_files
 else:
  state_from=TIdxq()
 delta_log_ptr=create_delta_log(state_from,new_version.state_files)
 expansion_point_commit=Commit(tail_ptr=expansion_point.hash_ref,head_ptr=new_version.hash_ref,message="Finalizing commit",delta_log_ptr=delta_log_ptr)
 expansion_point.state_files=new_version.state_files
 expansion_point.assoc_commit=expansion_point_commit
 head_version.active_revision_ptr=NIL_PTR
 object_storage.upsert_objects(head_version,expansion_point,new_active_revision,new_version)
 _update_head(new_version.version_number,new_version.hash_ref)
 _update_max_ver(new_version.version_number,new_version.hash_ref)
 _add_known_ver(new_version.version_number,new_version.hash_ref)
 CommitMetamodelUtils.create_metadata_archive(new_version)
 config_context.update_ver_log(author=expansion_point.creator,ver_no=new_version.version_number,rev_id=new_active_revision.rid,rev_no=new_active_revision.revision_number)
 return new_version
def _create_state_directory(version_number:TIdxo,state_file_refs:Set[StateFileRef],delete_files=TIdxW,archive=TIdxn):
 version_state_dir=os.path.join(config_context.get_pod_root_dir(),STATE_ZIP.format(version_no=version_number))
 for state_file in state_file_refs:
  try:
   dst_path=os.path.join(version_state_dir,API_STATES_DIR,state_file.rel_path)
   mkdir(dst_path)
   src=object_storage.get_state_file_location_by_key(state_file.hash_ref)
   dst=os.path.join(dst_path,state_file.file_name)
   shutil.copy(src,dst)
   if delete_files:
    os.remove(src)
  except TIdxJ as e:
   LOG.warning(f"Failed to locate state file with rel path: {state_file.rel_path}: {e}")
 mkdir(os.path.join(version_state_dir,"kinesis"))
 mkdir(os.path.join(version_state_dir,"dynamodb"))
 if archive:
  shutil.make_archive(version_state_dir,COMPRESSION_FORMAT,root_dir=version_state_dir)
  rm_rf(version_state_dir)
  return f"{version_state_dir}.{COMPRESSION_FORMAT}"
 return version_state_dir
def set_active_version(version_no:TIdxo,commit_before=TIdxW)->TIdxN:
 known_versions=load_version_references()
 for known_version_no,known_version_key in known_versions:
  if known_version_no==version_no:
   if commit_before:
    commit()
   _set_active_version(known_version_key)
   return TIdxn
 LOG.info(f"Version with number {version_no} not found")
 return TIdxW
def _set_active_version(key:TIdxC):
 current_head=get_head()
 if current_head.hash_ref!=key and object_storage.version_exists(key):
  requested_version=object_storage.get_version_by_key(key)
  _update_head(requested_version.version_number,key)
  if requested_version.active_revision_ptr==NIL_PTR:
   new_path_root=Revision(hash_ref=random_hash(),state_files=TIdxq(),parent_ptr=NIL_PTR,creator=config_context.get_context_user(),rid=short_uid(),revision_number=0)
   requested_version.active_revision_ptr=new_path_root.hash_ref
   requested_version.outgoing_revision_ptrs.add(new_path_root.hash_ref)
   object_storage.upsert_objects(new_path_root,requested_version)
def get_version_by_number(version_no:TIdxo)->Version:
 versions=load_version_references()
 version_ref=TIdxz((version[1]for version in versions if version[0]==version_no),TIdxc)
 if not version_ref:
  LOG.warning(f"Could not find version number {version_no}")
  return
 return object_storage.get_version_by_key(version_ref)
def load_version_references()->List[Tuple[TIdxo,TIdxC]]:
 result={}
 with TIdxO(config_context.get_known_ver_path(),"r")as vp:
  symlinks=vp.readlines()
  for symlink in symlinks:
   symlink=config_context.get_pod_absolute_path(symlink.rstrip())
   with TIdxO(symlink,"r")as sp:
    result[TIdxo(os.path.basename(symlink))]=sp.readline()
 return TIdxu(result.items(),key=lambda x:x[0],reverse=TIdxn)
def list_versions()->List[TIdxC]:
 version_references=load_version_references()
 result=[object_storage.get_version_by_key(version_key).info_str()for _,version_key in version_references]
 return result
def list_version_commits(version_no:TIdxo)->List[TIdxC]:
 if version_no==-1:
  version=_get_max_version()
 else:
  version=get_version_by_number(version_no)
 if not version:
  return[]
 result=[]
 revision=object_storage.get_revision_by_key(version.incoming_revision_ptr)
 while revision:
  assoc_commit=revision.assoc_commit
  revision_no=revision.revision_number
  if revision_no!=0:
   from_node=f"Revision-{revision_no - 1}"
  elif version_no!=0:
   from_node=f"Version-{version_no}"
  else:
   from_node="Empty state"
  to_node=f"Revision-{revision_no}"
  result.append(assoc_commit.info_str(from_node=from_node,to_node=to_node))
  revision=object_storage.get_revision_by_key(revision.parent_ptr)
 return result
def _update_head(new_head_ver_no,new_head_key)->TIdxC:
 with TIdxO(config_context.get_head_path(),"w")as fp:
  ver_symlink=config_context.create_version_symlink(VER_SYMLINK.format(ver_no=new_head_ver_no),new_head_key)
  fp.write(ver_symlink)
  return ver_symlink
def _update_max_ver(new_max_ver_no,new_max_ver_key)->TIdxC:
 with TIdxO(config_context.get_max_ver_path(),"w")as fp:
  max_ver_symlink=config_context.create_version_symlink(VER_SYMLINK.format(ver_no=new_max_ver_no),new_max_ver_key)
  fp.write(max_ver_symlink)
  return max_ver_symlink
def _add_known_ver(new_ver_no,new_ver_key)->TIdxC:
 with TIdxO(config_context.get_known_ver_path(),"a")as fp:
  new_ver_symlink=config_context.create_version_symlink(VER_SYMLINK.format(ver_no=new_ver_no),new_ver_key)
  fp.write(f"\n{new_ver_symlink}")
  return new_ver_symlink
def _is_special_case(obj)->TIdxN:
 return TIdxw(obj,(Queue,FakeBucket))
def _merge_three_way_dir_func(**kwargs):
 dir_name=kwargs.get("dir_name")
 fname=kwargs.get("fname")
 region=kwargs.get("region")
 service_name=kwargs.get("service_name")
 mutables=kwargs.get("mutables")
 other=mutables[0]
 ancestor=mutables[1]
 src_state_file_path=os.path.join(dir_name,fname)
 ancestor_state_dir=os.path.join(ancestor,service_name,region)
 ancestor_state_file_path=os.path.join(ancestor_state_dir,fname)
 dst_state_dir=os.path.join(other,service_name,region)
 dst_state_file_path=os.path.join(dst_state_dir,fname)
 src_state=load_persisted_object(src_state_file_path)
 ancestor_state=load_persisted_object(ancestor_state_file_path)
 special_case=_is_special_case(src_state)
 if os.path.isfile(dst_state_file_path):
  if not special_case:
   dst_state=load_persisted_object(dst_state_file_path)
   merge_object_state(dst_state,src_state,ancestor_state)
   persist_object(dst_state,dst_state_file_path)
 else:
  mkdir(dst_state_dir)
  persist_object(src_state,dst_state_file_path)
def _merge_two_state_dir_func(**kwargs):
 dir_name=kwargs.get("dir_name")
 fname=kwargs.get("fname")
 region=kwargs.get("region")
 service_name=kwargs.get("service_name")
 mutables=kwargs.get("mutables")
 other=mutables[0]
 src_state_file_path=os.path.join(dir_name,fname)
 dst_state_dir=os.path.join(other,service_name,region)
 dst_state_file_path=os.path.join(dst_state_dir,fname)
 src_state=load_persisted_object(src_state_file_path)
 special_case=_is_special_case(src_state)
 if os.path.isfile(dst_state_file_path):
  if not special_case:
   dst_state=load_persisted_object(dst_state_file_path)
   merge_object_state(dst_state,src_state)
   persist_object(dst_state,dst_state_file_path)
 else:
  mkdir(dst_state_dir)
  persist_object(src_state,dst_state_file_path)
def _merge_expansion_point_with_max(three_way=TIdxW):
 expansion_point,head=_get_expansion_point_with_head()
 curr_max_version_no=get_max_version_no()
 new_version_no=curr_max_version_no+1
 curr_max_version_state_archive=PodFilePaths.get_version_state_archive(curr_max_version_no)
 common_ancestor_state_archive=TIdxc
 tmp_common_ancestor_state_dir=TIdxc
 if head.version_number>1 and three_way:
  common_ancestor_state_archive=PodFilePaths.get_version_state_archive(head.version_number-1)
  tmp_common_ancestor_state_dir=new_tmp_dir()
  with zipfile.ZipFile(common_ancestor_state_archive)as archive:
   archive.extractall(tmp_common_ancestor_state_dir)
 tmp_max_version_state_dir=new_tmp_dir()
 with zipfile.ZipFile(curr_max_version_state_archive)as archive:
  archive.extractall(tmp_max_version_state_dir)
 new_max_version_states_dir=_create_state_directory(version_number=new_version_no,state_file_refs=expansion_point.state_files,archive=TIdxW)
 new_max_version_states_dir_api_states=os.path.join(new_max_version_states_dir,API_STATES_DIR)
 tmp_max_version_state_dir_api_states=os.path.join(tmp_max_version_state_dir,API_STATES_DIR)
 if not common_ancestor_state_archive:
  api_states_traverse(api_states_path=tmp_max_version_state_dir_api_states,side_effect=_merge_two_state_dir_func,mutables=[new_max_version_states_dir_api_states])
 else:
  LOG.debug(f"Starting three way merge between version {head.version_number} and {curr_max_version_no} with common ancestor {head.version_number - 1}")
  common_ancestor_version_state_dir_api_states=os.path.join(tmp_common_ancestor_state_dir,API_STATES_DIR)
  api_states_traverse(api_states_path=tmp_max_version_state_dir_api_states,side_effect=_merge_three_way_dir_func,mutables=[new_max_version_states_dir_api_states,common_ancestor_version_state_dir_api_states])
 shutil.make_archive(new_max_version_states_dir,COMPRESSION_FORMAT,root_dir=new_max_version_states_dir)
 rm_rf(new_max_version_states_dir)
 rm_rf(tmp_max_version_state_dir)
 rm_rf(tmp_common_ancestor_state_dir)
def create_delta_log(state_from:Set[StateFileRef],state_to:Set[StateFileRef],diff_method:MetamodelDeltaMethod=MetamodelDeltaMethod.SIMPLE)->TIdxC:
 try:
  delta_manager=MetamodelDelta.get(diff_method)
  return delta_manager.create_delta_log(state_from,state_to)
 except TIdxJ as e:
  LOG.debug("Unable to create delta log for version graph nodes: %s",e)
  key=short_uid()
  dest=os.path.join(config_context.get_delta_log_path(),key)
  save_file(dest,"{}")
  return key
# Created by pyminifier (https://github.com/liftoff/pyminifier)

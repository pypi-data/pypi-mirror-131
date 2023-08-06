from datetime import datetime
dFSgJ=str
dFSgQ=int
dFSgO=super
dFSgp=False
dFSgM=isinstance
dFSge=hash
dFSgw=bool
dFSgn=True
dFSgE=list
dFSgf=map
dFSgN=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:dFSgJ):
  self.hash_ref:dFSgJ=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:dFSgJ,rel_path:dFSgJ,file_name:dFSgJ,size:dFSgQ,service:dFSgJ,region:dFSgJ):
  dFSgO(StateFileRef,self).__init__(hash_ref)
  self.rel_path:dFSgJ=rel_path
  self.file_name:dFSgJ=file_name
  self.size:dFSgQ=size
  self.service:dFSgJ=service
  self.region:dFSgJ=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return dFSgp
  if not dFSgM(other,StateFileRef):
   return dFSgp
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return dFSge((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->dFSgw:
  if not other:
   return dFSgp
  if not dFSgM(other,StateFileRef):
   return dFSgp
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->dFSgw:
  for other in others:
   if self.congruent(other):
    return dFSgn
  return dFSgp
 def metadata(self)->dFSgJ:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:dFSgJ,state_files:Set[StateFileRef],parent_ptr:dFSgJ):
  dFSgO(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:dFSgJ=parent_ptr
 def state_files_info(self)->dFSgJ:
  return "\n".join(dFSgE(dFSgf(lambda state_file:dFSgJ(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:dFSgJ,head_ptr:dFSgJ,message:dFSgJ,timestamp:dFSgJ=dFSgJ(datetime.now().timestamp()),delta_log_ptr:dFSgJ=dFSgN):
  self.tail_ptr:dFSgJ=tail_ptr
  self.head_ptr:dFSgJ=head_ptr
  self.message:dFSgJ=message
  self.timestamp:dFSgJ=timestamp
  self.delta_log_ptr:dFSgJ=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:dFSgJ,to_node:dFSgJ)->dFSgJ:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:dFSgJ,state_files:Set[StateFileRef],parent_ptr:dFSgJ,creator:dFSgJ,rid:dFSgJ,revision_number:dFSgQ,assoc_commit:Commit=dFSgN):
  dFSgO(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:dFSgJ=creator
  self.rid:dFSgJ=rid
  self.revision_number:dFSgQ=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(dFSgf(lambda state_file:dFSgJ(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:dFSgJ,state_files:Set[StateFileRef],parent_ptr:dFSgJ,creator:dFSgJ,comment:dFSgJ,active_revision_ptr:dFSgJ,outgoing_revision_ptrs:Set[dFSgJ],incoming_revision_ptr:dFSgJ,version_number:dFSgQ):
  dFSgO(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(dFSgf(lambda stat_file:dFSgJ(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)

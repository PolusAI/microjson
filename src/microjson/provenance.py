from pydantic import BaseModel
from typing import List, Optional, Dict, Union, Literal


class MicroJSONLink(BaseModel):
    """A link to a MicroJSON object"""
    microjsonId: Union[str, List[str]]
    microjsonField: Optional[str] = None


class Artifact(BaseModel):
    """Artifact object representing a single file or directory"""
    id: Optional[str] = None
    type: Literal["Artifact"]
    uri: str
    properties: Optional[Dict[str, Union[str, float, int]]] = None
    microjsonLinks: List['MicroJSONLink']


class ArtifactCollection(BaseModel):
    """ArtifactCollection object representing a collection of files or
     directories"""
    type: Literal["ArtifactCollection"]
    artifacts: List[Artifact]


class Workflow(BaseModel):
    """Workflow object representing a single workflow"""
    id: Optional[str] = None
    type: Literal["Workflow"]
    properties: Optional[Dict[str, Union[str, float, int]]] = None
    subWorkflows: Optional[List['Workflow']] = None
    workflowProvenance: Optional['WorkflowProvenance'] = None


class WorkflowProvenance(BaseModel):
    """WorkflowProvenance object representing an execution of a workflow"""
    type: Literal["WorkflowProvenance"]
    properties: Optional[Dict[str, Union[str, float, int]]] = None
    outputArtifacts: Optional[Union[Artifact, ArtifactCollection]] = None


class WorkflowCollection(BaseModel):
    """WorkflowCollection object representing a collection of workflows"""
    type: Literal["WorkflowCollection"]
    workflows: List[Workflow]

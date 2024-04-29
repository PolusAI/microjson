from pydantic import BaseModel
from typing import List, Optional, Dict, Union, Literal


class MicroJSONLink(BaseModel):
    """A link to a MicroJSON object"""
    microjson_id: Union[str, List[str]]
    microjson_field: Optional[str] = None


class Artifact(BaseModel):
    """Artifact object representing a single file or directory"""
    id: Optional[str] = None
    type: Literal["Artifact"]
    uri: str
    properties: Optional[Dict[str, Union[str, float, int]]] = None
    microjson_links: List['MicroJSONLink']


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
    sub_workflows: Optional[List['Workflow']] = None
    workflow_provenance: Optional['WorkflowProvenance'] = None


class WorkflowProvenance(BaseModel):
    """WorkflowProvenance object representing an execution of a workflow"""
    type: Literal["WorkflowProvenance"]
    properties: Optional[Dict[str, Union[str, float, int]]] = None
    output_artifacts: Optional[Union[Artifact, ArtifactCollection]] = None


class WorkflowCollection(BaseModel):
    """WorkflowCollection object representing a collection of workflows"""
    type: Literal["WorkflowCollection"]
    workflows: List[Workflow]


# src/models/schemas.py
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

class Position(BaseModel):
    x: float
    y: float

class SubBlock(BaseModel):
    id: str
    type: str
    value: Any

class WorkflowBlockBase(BaseModel):
    id: str
    type: str
    name: str
    position: Position
    enabled: bool = True
    horizontal_handles: bool = True
    is_wide: bool = False
    height: float = 95
    sub_blocks: Dict[str, SubBlock] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)

class WorkflowBlock(WorkflowBlockBase):
    workflow_id: str
    position_x: float
    position_y: float
    advanced_mode: bool = False
    data: Optional[Dict[str, Any]] = None
    parent_id: Optional[str] = None
    extent: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Edge(BaseModel):
    source: str
    target: str
    source_handle: str = "output"
    target_handle: str = "input"

class WorkflowMetadata(BaseModel):
    version: str = "1.0.0"
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")

class WorkflowState(BaseModel):
    blocks: Dict[str, Dict[str, Any]]
    edges: List[Edge]
    subflows: Dict[str, Any] = Field(default_factory=dict)
    variables: Dict[str, Any] = Field(default_factory=dict)
    metadata: WorkflowMetadata

class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    state: WorkflowState
    color: str = "#3972F6"

class Workflow(WorkflowBase):
    id: str
    user_id: str
    workspace_id: Optional[str] = None
    folder_id: Optional[str] = None
    last_synced: datetime
    created_at: datetime
    updated_at: datetime
    is_deployed: bool = False
    deployed_state: Optional[Dict[str, Any]] = None
    deployed_at: Optional[datetime] = None
    collaborators: List[str] = Field(default_factory=list)
    run_count: int = 0
    last_run_at: Optional[datetime] = None
    variables: Dict[str, Any] = Field(default_factory=dict)
    is_published: bool = False
    marketplace_data: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True

class StateGenerationOptions(BaseModel):
    optimization_goal: str = "efficiency"
    include_suggestions: bool = True
    use_ai_enhancement: bool = True

class ValidationResult(BaseModel):
    validator_name: str
    valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None

class ValidationReport(BaseModel):
    overall_valid: bool
    validation_results: List[ValidationResult]
    agent_forge_compliance: bool
    suggestions: List[str] = Field(default_factory=list)

# src/models/database.py
from sqlalchemy import Column, Text, Numeric, Boolean, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Workflow(Base):
    __tablename__ = 'workflow'
    
    id = Column(Text, primary_key=True)
    user_id = Column(Text, nullable=False)
    workspace_id = Column(Text, nullable=True)
    folder_id = Column(Text, nullable=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    state = Column(JSON, nullable=False)
    color = Column(Text, nullable=False, default='#3972F6')
    last_synced = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_deployed = Column(Boolean, nullable=False, default=False)
    deployed_state = Column(JSON, nullable=True)
    deployed_at = Column(DateTime, nullable=True)
    collaborators = Column(JSON, nullable=False, default=lambda: [])
    run_count = Column(Integer, nullable=False, default=0)
    last_run_at = Column(DateTime, nullable=True)
    variables = Column(JSON, nullable=True, default=lambda: {})
    is_published = Column(Boolean, nullable=False, default=False)
    marketplace_data = Column(JSON, nullable=True)
    
    # Relationship
    blocks = relationship("WorkflowBlock", back_populates="workflow", cascade="all, delete-orphan")

class WorkflowBlock(Base):
    __tablename__ = 'workflow_blocks'
    
    id = Column(Text, primary_key=True)
    workflow_id = Column(Text, ForeignKey('workflow.id'), nullable=False)
    type = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    position_x = Column(Numeric, nullable=False)
    position_y = Column(Numeric, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    horizontal_handles = Column(Boolean, nullable=False, default=True)
    is_wide = Column(Boolean, nullable=False, default=False)
    advanced_mode = Column(Boolean, nullable=False, default=False)
    height = Column(Numeric, nullable=False, default=0)
    sub_blocks = Column(JSONB, nullable=False, default=lambda: {})
    outputs = Column(JSONB, nullable=False, default=lambda: {})
    data = Column(JSONB, nullable=True, default=lambda: {})
    parent_id = Column(Text, nullable=True)
    extent = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    workflow = relationship("Workflow", back_populates="blocks") 
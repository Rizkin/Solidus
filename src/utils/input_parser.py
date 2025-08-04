import re
import json
from typing import Dict, List, Tuple, Optional
from pathlib import Path

class WorkflowInputParser:
    """Parse workflow definition from text file"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.workflow = {}
        self.blocks = []
        self.connections = []
        self.errors = []
        
    def parse(self) -> Dict[str, any]:
        """Parse the input file and return structured data"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.file_path}")
        
        with open(self.file_path, 'r') as f:
            content = f.read()
        
        # Parse sections
        self._parse_workflow_section(content)
        self._parse_blocks_section(content)
        self._parse_connections_section(content)
        
        # Validate
        if self.errors:
            raise ValueError(f"Parsing errors: {self.errors}")
        
        return {
            "workflow": self.workflow,
            "blocks": self.blocks,
            "connections": self.connections
        }
    
    def _parse_workflow_section(self, content: str):
        """Parse @WORKFLOW section"""
        pattern = r'@WORKFLOW\s*\n(.*?)(?=@|$)'
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            self.errors.append("Missing @WORKFLOW section")
            return
        
        section = match.group(1)
        for line in section.strip().split('\n'):
            if line.strip() and not line.startswith('#'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    self.workflow[key.strip()] = value.strip()
    
    def _parse_blocks_section(self, content: str):
        """Parse @BLOCKS section"""
        pattern = r'@BLOCKS\s*\n(.*?)(?=@|$)'
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            self.errors.append("Missing @BLOCKS section")
            return
        
        section = match.group(1)
        for line in section.strip().split('\n'):
            if line.strip() and not line.startswith('#'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 5:
                    try:
                        config = json.loads(parts[5]) if len(parts) > 5 else {}
                        self.blocks.append({
                            "id": parts[0],
                            "type": parts[1],
                            "name": parts[2],
                            "position_x": float(parts[3]),
                            "position_y": float(parts[4]),
                            "config": config
                        })
                    except (ValueError, json.JSONDecodeError) as e:
                        self.errors.append(f"Invalid block line: {line} - {e}")
    
    def _parse_connections_section(self, content: str):
        """Parse @CONNECTIONS section"""
        pattern = r'@CONNECTIONS\s*\n(.*?)(?=@|$)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            section = match.group(1)
            for line in section.strip().split('\n'):
                if line.strip() and not line.startswith('#'):
                    if '->' in line:
                        source, target = line.split('->')
                        self.connections.append({
                            "source": source.strip(),
                            "target": target.strip()
                        })

    def validate(self) -> List[str]:
        """Validate the parsed data"""
        errors = []
        
        # Check required workflow fields
        required = ['id', 'name']
        for field in required:
            if field not in self.workflow:
                errors.append(f"Missing required workflow field: {field}")
        
        # Check blocks
        if not self.blocks:
            errors.append("No blocks defined")
        
        block_ids = {b['id'] for b in self.blocks}
        
        # Validate block types
        valid_types = ['starter', 'agent', 'api', 'output', 'tool']
        for block in self.blocks:
            if block['type'] not in valid_types:
                errors.append(f"Invalid block type: {block['type']}")
        
        # Validate connections
        for conn in self.connections:
            if conn['source'] not in block_ids:
                errors.append(f"Invalid connection source: {conn['source']}")
            if conn['target'] not in block_ids:
                errors.append(f"Invalid connection target: {conn['target']}")
        
        # Check for starter block
        if not any(b['type'] == 'starter' for b in self.blocks):
            errors.append("No starter block found")
        
        return errors 
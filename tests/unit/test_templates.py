"""
Comprehensive tests for all 13 workflow templates.

Tests template availability, generation, customization, block generation, and edge cases.

Coverage target: 100% for template system
"""

import pytest
from unittest.mock import MagicMock, patch
from typing import Dict, Any, List

from src.services.templates import TemplateService
from tests.fixtures.mock_data import TEMPLATE_TEST_DATA


class TestTemplateService:
    """Test suite for TemplateService - all 13 templates."""

    @pytest.fixture(autouse=True)
    def setup_template_service(self):
        """Set up template service for each test."""
        self.template_service = TemplateService()

    # ========================================
    # 1. Template Availability Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.template
    def test_all_13_templates_exist(self):
        """Test that all 13 templates are available."""
        expected_templates = [
            "lead_generation", "trading_bot", "multi_agent_research",
            "customer_support", "web3_automation", "data_pipeline",
            "content_generation", "notification_system",
            "social_media_automation", "ecommerce_automation", 
            "hr_recruitment", "financial_analysis", "project_management"
        ]
        
        available_templates = self.template_service.get_available_templates()
        
        assert len(available_templates) == 13
        
        for template_name in expected_templates:
            assert template_name in available_templates, f"Template {template_name} is missing"

    @pytest.mark.unit
    @pytest.mark.template
    def test_template_metadata_structure(self):
        """Test that template metadata follows expected structure."""
        templates = self.template_service.get_templates_with_metadata()
        
        for template_name, metadata in templates.items():
            # Verify required metadata fields
            assert "category" in metadata, f"Template {template_name} missing category"
            assert "description" in metadata, f"Template {template_name} missing description"  
            assert "blocks" in metadata, f"Template {template_name} missing blocks info"
            assert "difficulty" in metadata, f"Template {template_name} missing difficulty"
            
            # Verify metadata types
            assert isinstance(metadata["category"], str)
            assert isinstance(metadata["description"], str)
            assert isinstance(metadata["blocks"], list)
            assert metadata["difficulty"] in ["beginner", "intermediate", "advanced"]

    @pytest.mark.unit
    @pytest.mark.template
    def test_template_categories_coverage(self):
        """Test that templates cover expected categories."""
        expected_categories = [
            "Sales & Marketing", "Finance", "Blockchain", "AI Automation",
            "Data Processing", "Human Resources", "Communication", "Web3 Trading",
            "Project Management", "E-commerce", "Content & Media", "Social Media",
            "Customer Service"
        ]
        
        templates_metadata = self.template_service.get_templates_with_metadata()
        actual_categories = set(template["category"] for template in templates_metadata.values())
        
        assert len(actual_categories) >= 10, "Should have at least 10 different categories"
        
        for category in expected_categories:
            assert any(category in cat for cat in actual_categories), f"Missing category: {category}"

    @pytest.mark.unit
    @pytest.mark.template
    def test_template_structure_validation(self):
        """Test that all templates have valid structure."""
        templates = self.template_service.get_available_templates()
        
        for template_name in templates:
            template_config = self.template_service.get_template_config(template_name)
            
            # Verify required structure
            assert "blocks" in template_config, f"Template {template_name} missing blocks"
            assert "edges" in template_config, f"Template {template_name} missing edges"
            assert "metadata" in template_config, f"Template {template_name} missing metadata"
            
            # Verify blocks have required fields
            blocks = template_config["blocks"]
            for block_id, block in blocks.items():
                assert "type" in block, f"Block {block_id} in {template_name} missing type"
                assert "name" in block, f"Block {block_id} in {template_name} missing name"
                assert "position" in block, f"Block {block_id} in {template_name} missing position"

    # ========================================
    # 2. Template Generation Tests (All 13)
    # ========================================

    @pytest.mark.unit
    @pytest.mark.template
    @pytest.mark.parametrize("template_name", [
        "lead_generation", "trading_bot", "multi_agent_research",
        "customer_support", "web3_automation", "data_pipeline", 
        "content_generation", "notification_system",
        "social_media_automation", "ecommerce_automation",
        "hr_recruitment", "financial_analysis", "project_management"
    ])
    def test_template_generation_with_defaults(self, template_name):
        """Test template generation with default parameters for all 13 templates."""
        result = self.template_service.generate_from_template(template_name)
        
        # Verify successful generation
        assert result is not None
        assert "blocks" in result
        assert "edges" in result
        assert "metadata" in result
        
        # Verify structure
        blocks = result["blocks"]
        edges = result["edges"]
        
        assert len(blocks) > 0, f"Template {template_name} generated no blocks"
        assert isinstance(edges, list), f"Template {template_name} edges should be list"
        
        # Verify all blocks have required fields
        for block_id, block in blocks.items():
            assert "id" in block
            assert "type" in block
            assert "name" in block
            assert "position" in block
            assert "subBlocks" in block

    @pytest.mark.unit
    @pytest.mark.template
    @pytest.mark.parametrize("template_name", [
        "lead_generation", "trading_bot", "multi_agent_research",
        "customer_support", "web3_automation", "data_pipeline",
        "content_generation", "notification_system", 
        "social_media_automation", "ecommerce_automation",
        "hr_recruitment", "financial_analysis", "project_management"
    ])
    def test_template_generation_with_custom_params(self, template_name):
        """Test template generation with custom parameters for all templates."""
        # Define custom parameters for each template
        custom_params = {
            "lead_generation": {"lead_source": "LinkedIn", "crm": "Salesforce"},
            "trading_bot": {"trading_pair": "ETH/USD", "stop_loss": -3.5},
            "multi_agent_research": {"research_topic": "Quantum Computing", "num_agents": 4},
            "customer_support": {"channels": ["email", "chat"], "priority": "high"},
            "web3_automation": {"blockchain": "ethereum", "gas_limit": 50000},
            "data_pipeline": {"source": "postgresql", "destination": "snowflake"},
            "content_generation": {"content_type": "blog", "tone": "professional"},
            "notification_system": {"channels": ["email", "slack"], "urgency": "medium"},
            "social_media_automation": {"platforms": ["twitter", "linkedin"], "schedule": "daily"},
            "ecommerce_automation": {"platform": "shopify", "currency": "USD"},
            "hr_recruitment": {"position": "Software Engineer", "experience": "mid-level"},
            "financial_analysis": {"metrics": ["roi", "npv"], "period": "quarterly"},
            "project_management": {"methodology": "agile", "team_size": 8}
        }
        
        params = custom_params.get(template_name, {})
        result = self.template_service.generate_from_template(template_name, params)
        
        # Verify successful generation with customization
        assert result is not None
        assert "blocks" in result
        
        # Verify customization was applied (check metadata or block configs)
        metadata = result.get("metadata", {})
        if params:
            # At least some customization should be reflected
            customization_applied = (
                any(str(value) in str(metadata) for value in params.values()) or
                any(str(value) in str(result["blocks"]) for value in params.values())
            )
            assert customization_applied, f"Customization not applied for {template_name}"

    @pytest.mark.unit
    @pytest.mark.template
    def test_template_block_structure_compliance(self, template_name):
        """Test that generated templates comply with Agent Forge block structure."""
        result = self.template_service.generate_from_template(template_name)
        blocks = result["blocks"]
        
        # Verify Agent Forge compliance
        for block_id, block in blocks.items():
            # Required Agent Forge fields
            assert block["id"] == block_id
            assert block["type"] in ["starter", "agent", "api", "tool", "output"]
            assert isinstance(block["position"], dict)
            assert "x" in block["position"] and "y" in block["position"]
            assert isinstance(block["subBlocks"], list)
            
            # Type-specific validations
            if block["type"] == "agent":
                config = block.get("config", {})
                assert "model" in config or "systemPrompt" in config
            
            elif block["type"] == "api":
                config = block.get("config", {})
                assert "url" in config or "method" in config
            
            elif block["type"] == "starter":
                # Starter blocks should have minimal config
                assert "config" in block

    @pytest.mark.unit
    @pytest.mark.template
    def test_template_edge_connections(self, template_name):
        """Test that template edges create proper connections."""
        result = self.template_service.generate_from_template(template_name)
        blocks = result["blocks"]
        edges = result["edges"]
        
        # Verify edge structure
        for edge in edges:
            assert "from" in edge and "to" in edge
            assert edge["from"] in blocks, f"Edge 'from' {edge['from']} not in blocks"
            assert edge["to"] in blocks, f"Edge 'to' {edge['to']} not in blocks"
        
        # Verify connectivity (no orphaned blocks except potentially outputs)
        connected_blocks = set()
        for edge in edges:
            connected_blocks.add(edge["from"])
            connected_blocks.add(edge["to"])
        
        orphaned_blocks = set(blocks.keys()) - connected_blocks
        
        # Only output blocks should potentially be orphaned (as endpoints)
        for orphaned in orphaned_blocks:
            block_type = blocks[orphaned]["type"]
            assert block_type == "output", f"Non-output block {orphaned} is orphaned"

    # ========================================
    # 3. Template Customization Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.template
    def test_trading_bot_customization_parameters(self):
        """Test trading bot template with various customization parameters."""
        test_cases = [
            {"trading_pair": "BTC/USD", "stop_loss": -5.0},
            {"trading_pair": "ETH/BTC", "stop_loss": -2.5, "take_profit": 10.0},
            {"trading_pair": "ADA/USDT", "timeframe": "1h", "strategy": "momentum"},
            {"risk_management": True, "position_size": 0.1}
        ]
        
        for params in test_cases:
            result = self.template_service.generate_from_template("trading_bot", params)
            
            # Verify customization reflected in blocks or metadata
            blocks = result["blocks"]
            metadata = result["metadata"]
            
            customization_found = False
            for value in params.values():
                if (str(value) in str(blocks) or str(value) in str(metadata)):
                    customization_found = True
                    break
            
            assert customization_found, f"Customization {params} not applied"

    @pytest.mark.unit
    @pytest.mark.template
    def test_lead_generation_customization_sources(self):
        """Test lead generation template with different lead sources."""
        test_sources = [
            {"lead_source": "LinkedIn", "crm": "HubSpot"},
            {"lead_source": "Facebook", "crm": "Salesforce"},
            {"lead_source": "Cold Email", "crm": "Pipedrive"},
            {"lead_source": "Website", "crm": "Zoho", "qualification": "BANT"}
        ]
        
        for params in test_sources:
            result = self.template_service.generate_from_template("lead_generation", params)
            
            # Verify source-specific blocks or configurations
            blocks = result["blocks"]
            
            # Should have appropriate blocks for the source
            if params["lead_source"] == "LinkedIn":
                # Should have LinkedIn-specific configuration
                linkedin_config_found = any(
                    "linkedin" in str(block).lower() 
                    for block in blocks.values()
                )
                assert linkedin_config_found or "linkedin" in str(result).lower()

    @pytest.mark.unit
    @pytest.mark.template
    def test_social_media_platform_combinations(self):
        """Test social media automation with different platform combinations."""
        platform_combinations = [
            {"platforms": ["twitter"]},
            {"platforms": ["linkedin"]},
            {"platforms": ["twitter", "linkedin"]},
            {"platforms": ["twitter", "linkedin", "facebook"]},
            {"platforms": ["instagram", "tiktok"], "content_type": "video"}
        ]
        
        for params in platform_combinations:
            result = self.template_service.generate_from_template("social_media_automation", params)
            
            blocks = result["blocks"]
            platforms = params["platforms"]
            
            # Verify platform-specific blocks or configurations
            for platform in platforms:
                platform_found = any(
                    platform.lower() in str(block).lower()
                    for block in blocks.values()
                )
                # Platform should be referenced somewhere in the workflow
                assert platform_found or platform.lower() in str(result).lower()

    @pytest.mark.unit
    @pytest.mark.template  
    def test_multi_agent_research_agent_count(self):
        """Test multi-agent research template with different agent counts."""
        agent_counts = [2, 3, 5, 7]
        
        for num_agents in agent_counts:
            params = {"num_agents": num_agents, "research_topic": "AI Ethics"}
            result = self.template_service.generate_from_template("multi_agent_research", params)
            
            blocks = result["blocks"]
            agent_blocks = [block for block in blocks.values() if block["type"] == "agent"]
            
            # Should have approximately the requested number of agents
            # (allowing for some template-specific variation)
            assert len(agent_blocks) >= num_agents - 1, f"Expected ~{num_agents} agents, got {len(agent_blocks)}"

    @pytest.mark.unit
    @pytest.mark.template
    def test_template_specific_parameter_validation(self):
        """Test that templates validate their specific parameters."""
        # Test invalid parameters for each template type
        invalid_params_tests = [
            ("trading_bot", {"invalid_param": "test"}),
            ("lead_generation", {"crm": "NonexistentCRM"}),
            ("social_media_automation", {"platforms": []}),  # Empty platforms
            ("financial_analysis", {"period": "invalid_period"})
        ]
        
        for template_name, invalid_params in invalid_params_tests:
            # Should either reject invalid params or handle them gracefully
            result = self.template_service.generate_from_template(template_name, invalid_params)
            
            # Should still generate valid workflow (graceful handling)
            assert result is not None
            assert "blocks" in result

    # ========================================
    # 4. Block Generation Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.template
    def test_block_types_per_template(self):
        """Test that each template generates correct block types."""
        expected_block_types = {
            "trading_bot": ["starter", "agent", "api", "output"],
            "lead_generation": ["starter", "agent", "tool", "output"], 
            "multi_agent_research": ["starter", "agent", "agent", "output"],  # Multiple agents
            "customer_support": ["starter", "agent", "tool", "output"],
            "data_pipeline": ["starter", "api", "agent", "tool", "output"]
        }
        
        for template_name, expected_types in expected_block_types.items():
            result = self.template_service.generate_from_template(template_name)
            blocks = result["blocks"]
            
            actual_types = [block["type"] for block in blocks.values()]
            
            # Verify expected types are present (allowing for extras)
            for expected_type in set(expected_types):
                assert expected_type in actual_types, f"Template {template_name} missing {expected_type} block"

    @pytest.mark.unit
    @pytest.mark.template
    def test_block_positioning_logic(self):
        """Test that blocks are positioned logically in templates."""
        for template_name in ["trading_bot", "lead_generation", "social_media_automation"]:
            result = self.template_service.generate_from_template(template_name)
            blocks = result["blocks"]
            
            positions = [(block["position"]["x"], block["position"]["y"]) for block in blocks.values()]
            
            # Verify positions are reasonable
            x_positions = [pos[0] for pos in positions]
            y_positions = [pos[1] for pos in positions]
            
            # Should have reasonable spread and positioning
            assert min(x_positions) >= 0, "X positions should be non-negative"
            assert max(x_positions) <= 2000, "X positions should be within canvas bounds"
            assert min(y_positions) >= -200, "Y positions should be within canvas bounds"
            assert max(y_positions) <= 1000, "Y positions should be within canvas bounds"
            
            # Should have some variation in positions (not all stacked)
            assert len(set(x_positions)) > 1 or len(set(y_positions)) > 1, "Blocks should not all be at same position"

    @pytest.mark.unit
    @pytest.mark.template
    def test_block_configuration_validity(self):
        """Test that generated blocks have valid configurations."""
        for template_name in ["lead_generation", "trading_bot", "multi_agent_research"]:
            result = self.template_service.generate_from_template(template_name)
            blocks = result["blocks"]
            
            for block_id, block in blocks.items():
                block_type = block["type"]
                config = block.get("config", {})
                
                # Type-specific configuration validation
                if block_type == "agent":
                    # Agent blocks should have model or system prompt
                    has_model_config = "model" in config or "systemPrompt" in config
                    assert has_model_config, f"Agent block {block_id} missing model configuration"
                
                elif block_type == "api":
                    # API blocks should have URL
                    assert "url" in config, f"API block {block_id} missing URL configuration"
                
                elif block_type == "tool":
                    # Tool blocks should have tool specification
                    has_tool_config = "tool_name" in config or "tool_type" in config
                    assert has_tool_config, f"Tool block {block_id} missing tool configuration"

    @pytest.mark.unit
    @pytest.mark.template
    def test_subblocks_configuration(self):
        """Test that blocks have appropriate subBlocks configuration."""
        result = self.template_service.generate_from_template("trading_bot")
        blocks = result["blocks"]
        
        for block_id, block in blocks.items():
            subblocks = block.get("subBlocks", [])
            
            # Verify subBlocks is always a list
            assert isinstance(subblocks, list), f"Block {block_id} subBlocks should be list"
            
            # Complex blocks might have subBlocks
            if block["type"] == "agent" and len(subblocks) > 0:
                for subblock in subblocks:
                    assert isinstance(subblock, dict), "SubBlock should be dict"
                    assert "type" in subblock, "SubBlock should have type"

    @pytest.mark.unit
    @pytest.mark.template
    def test_template_workflow_connections(self):
        """Test that template workflows have proper connectivity."""
        for template_name in ["trading_bot", "lead_generation", "data_pipeline"]:
            result = self.template_service.generate_from_template(template_name)
            blocks = result["blocks"]
            edges = result["edges"]
            
            # Verify starter block connects to something
            starter_blocks = [bid for bid, block in blocks.items() if block["type"] == "starter"]
            assert len(starter_blocks) >= 1, f"Template {template_name} should have starter block"
            
            starter_id = starter_blocks[0]
            starter_connects = any(edge["from"] == starter_id for edge in edges)
            assert starter_connects, f"Starter block in {template_name} should connect to other blocks"
            
            # Verify workflow has logical flow
            output_blocks = [bid for bid, block in blocks.items() if block["type"] == "output"]
            if output_blocks:
                output_id = output_blocks[0]
                output_receives = any(edge["to"] == output_id for edge in edges)
                assert output_receives, f"Output block in {template_name} should receive connections"

    # ========================================
    # 5. Edge Cases and Error Handling
    # ========================================

    @pytest.mark.unit
    @pytest.mark.template
    @pytest.mark.error_handling
    def test_invalid_template_name(self):
        """Test error handling for invalid template names."""
        invalid_names = [
            "nonexistent_template",
            "",
            None,
            123,
            "invalid-template-name"
        ]
        
        for invalid_name in invalid_names:
            with pytest.raises((ValueError, KeyError, TypeError)):
                self.template_service.generate_from_template(invalid_name)

    @pytest.mark.unit
    @pytest.mark.template
    @pytest.mark.error_handling
    def test_empty_customization_handling(self):
        """Test handling of empty customization parameters."""
        empty_params = [{}, None, ""]
        
        for empty_param in empty_params:
            try:
                result = self.template_service.generate_from_template("trading_bot", empty_param)
                # Should succeed with defaults
                assert result is not None
                assert "blocks" in result
            except (TypeError, ValueError):
                # Acceptable to reject invalid param types
                pass

    @pytest.mark.unit
    @pytest.mark.template
    @pytest.mark.error_handling 
    def test_malformed_parameter_handling(self):
        """Test handling of malformed parameters."""
        malformed_params = [
            {"trading_pair": None},
            {"platforms": "not_a_list"},
            {"num_agents": "not_a_number"},
            {"invalid": {"nested": {"params": True}}}
        ]
        
        for params in malformed_params:
            # Should either handle gracefully or raise appropriate error
            try:
                result = self.template_service.generate_from_template("trading_bot", params)
                # If successful, should still be valid
                assert result is not None
            except (ValueError, TypeError):
                # Acceptable to reject malformed params
                pass

    @pytest.mark.unit
    @pytest.mark.template
    @pytest.mark.error_handling
    def test_partial_customization_robustness(self):
        """Test robustness with partial customization."""
        # Test partial parameters for templates
        partial_params = [
            {"trading_pair": "BTC/USD"},  # Missing other trading params
            {"lead_source": "LinkedIn"},  # Missing CRM
            {"platforms": ["twitter"]},   # Missing other social media params
        ]
        
        templates = ["trading_bot", "lead_generation", "social_media_automation"]
        
        for i, template_name in enumerate(templates):
            params = partial_params[i]
            result = self.template_service.generate_from_template(template_name, params)
            
            # Should handle partial params gracefully
            assert result is not None
            assert "blocks" in result
            assert len(result["blocks"]) > 0

    @pytest.mark.unit
    @pytest.mark.template
    @pytest.mark.error_handling
    def test_extreme_parameter_values(self):
        """Test handling of extreme parameter values."""
        extreme_cases = [
            ("multi_agent_research", {"num_agents": 100}),  # Very large number
            ("trading_bot", {"stop_loss": -99.9}),          # Extreme stop loss
            ("social_media_automation", {"platforms": ["platform"] * 50}),  # Many platforms
            ("content_generation", {"content_length": 1000000})  # Very long content
        ]
        
        for template_name, extreme_params in extreme_cases:
            result = self.template_service.generate_from_template(template_name, extreme_params)
            
            # Should handle extremes gracefully (might cap values)
            assert result is not None
            assert "blocks" in result

    @pytest.mark.unit
    @pytest.mark.template
    @pytest.mark.performance
    def test_template_generation_performance(self, performance_monitor):
        """Test template generation performance."""
        template_names = ["trading_bot", "lead_generation", "multi_agent_research"]
        
        for template_name in template_names:
            performance_monitor.start_timer(f"template_{template_name}")
            
            result = self.template_service.generate_from_template(template_name)
            
            performance_monitor.end_timer(f"template_{template_name}")
            
            # Verify successful generation
            assert result is not None
            
            # Template generation should be fast
            performance_monitor.assert_performance(f"template_{template_name}", 1.0)

    @pytest.mark.unit
    @pytest.mark.template
    def test_template_consistency_across_calls(self):
        """Test that templates generate consistent results across multiple calls."""
        template_name = "trading_bot"
        params = {"trading_pair": "BTC/USD", "stop_loss": -5.0}
        
        # Generate same template multiple times
        results = []
        for _ in range(3):
            result = self.template_service.generate_from_template(template_name, params)
            results.append(result)
        
        # Should generate consistent structure (same block types, similar counts)
        first_result = results[0]
        for result in results[1:]:
            # Same number of blocks
            assert len(result["blocks"]) == len(first_result["blocks"])
            
            # Same block types present
            first_types = set(block["type"] for block in first_result["blocks"].values())
            result_types = set(block["type"] for block in result["blocks"].values())
            assert first_types == result_types

    @pytest.mark.unit
    @pytest.mark.template
    def test_all_templates_generate_valid_agent_forge_output(self):
        """Test that all 13 templates generate valid Agent Forge compatible output."""
        all_templates = [
            "lead_generation", "trading_bot", "multi_agent_research",
            "customer_support", "web3_automation", "data_pipeline",
            "content_generation", "notification_system", 
            "social_media_automation", "ecommerce_automation",
            "hr_recruitment", "financial_analysis", "project_management"
        ]
        
        for template_name in all_templates:
            result = self.template_service.generate_from_template(template_name)
            
            # Verify Agent Forge compatibility
            assert "blocks" in result
            assert "edges" in result
            assert "metadata" in result
            
            # Verify metadata structure
            metadata = result["metadata"]
            assert "agent_forge_version" in metadata or "version" in metadata
            
            # Verify blocks structure for Agent Forge
            blocks = result["blocks"]
            for block_id, block in blocks.items():
                assert all(key in block for key in ["id", "type", "name", "position"])
                assert block["type"] in ["starter", "agent", "api", "tool", "output"]
                assert isinstance(block["position"], dict)
                assert "x" in block["position"] and "y" in block["position"] 
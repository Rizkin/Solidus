-- Agent Forge Synthetic Data
-- INSERT statements for workflow_rows and workflow_blocks_rows tables

-- Insert into workflow_rows (3 workflows)
INSERT INTO workflow_rows (id, name, description, user_id, workspace_id, folder_id, color, variables, is_published, created_at, updated_at, last_synced, state)
VALUES 
('wf1', 'Test Workflow 1', 'Basic workflow for testing', 'user123', 'ws1', NULL, '#3972F6', '{"var1": "value1"}', false, NOW(), NOW(), NOW(), '{}'),
('wf2', 'Approval Process', 'Multi-step approval workflow', 'user123', 'ws1', NULL, '#3972F6', '{"approver": "manager", "threshold": 1000}', true, NOW(), NOW(), NOW(), '{}'),
('wf3', 'Data Processing Pipeline', 'ETL workflow for data processing', 'user123', 'ws1', NULL, '#3972F6', '{"source": "api", "destination": "database"}', false, NOW(), NOW(), NOW(), '{}');

-- Insert into workflow_blocks_rows (4-6 blocks per workflow)
-- Blocks for Workflow 1 (wf1)
INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block1-wf1', 'wf1', 'starter', 'Start Point', 0, 0, true, '{}', '{"next": "block2-wf1"}', '{"trigger": "manual"}', NULL, NOW(), NOW()),
('block2-wf1', 'wf1', 'action', 'Process Data', 100, 0, true, '{}', '{"result": "processed"}', '{"action": "transform"}', 'block1-wf1', NOW(), NOW()),
('block3-wf1', 'wf1', 'decision', 'Check Condition', 200, 0, true, '{}', '{"true": "block4-wf1", "false": "block5-wf1"}', '{"condition": "value > 10"}', 'block2-wf1', NOW(), NOW()),
('block4-wf1', 'wf1', 'action', 'Success Handler', 300, -50, true, '{}', '{"status": "complete"}', '{"notify": true}', 'block3-wf1', NOW(), NOW()),
('block5-wf1', 'wf1', 'action', 'Error Handler', 300, 50, false, '{}', '{"status": "failed"}', '{"retry": true}', 'block3-wf1', NOW(), NOW());

-- Blocks for Workflow 2 (wf2)
INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block1-wf2', 'wf2', 'starter', 'Approval Trigger', 0, 0, true, '{}', '{"next": "block2-wf2"}', '{"trigger": "form"}', NULL, NOW(), NOW()),
('block2-wf2', 'wf2', 'action', 'Validate Request', 100, 0, true, '{}', '{"valid": "boolean"}', '{"validation": "strict"}', 'block1-wf2', NOW(), NOW()),
('block3-wf2', 'wf2', 'decision', 'Check Amount', 200, 0, true, '{}', '{"approve": "block4-wf2", "escalate": "block5-wf2"}', '{"threshold": 1000}', 'block2-wf2', NOW(), NOW()),
('block4-wf2', 'wf2', 'action', 'Auto Approve', 300, -50, true, '{}', '{"status": "approved"}', '{"level": "auto"}', 'block3-wf2', NOW(), NOW()),
('block5-wf2', 'wf2', 'action', 'Escalate to Manager', 300, 50, true, '{}', '{"status": "escalated"}', '{"recipient": "manager"}', 'block3-wf2', NOW(), NOW()),
('block6-wf2', 'wf2', 'output', 'Send Notification', 400, 0, true, '{}', '{"sent": "boolean"}', '{"method": "email"}', 'block4-wf2', NOW(), NOW());

-- Blocks for Workflow 3 (wf3)
INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block1-wf3', 'wf3', 'starter', 'Data Ingestion', 0, 0, true, '{}', '{"next": "block2-wf3"}', '{"source": "api"}', NULL, NOW(), NOW()),
('block2-wf3', 'wf3', 'action', 'Transform Data', 100, 0, true, '{}', '{"transformed": "dataset"}', '{"operation": "clean"}', 'block1-wf3', NOW(), NOW()),
('block3-wf3', 'wf3', 'action', 'Validate Schema', 200, 0, true, '{}', '{"valid": "boolean"}', '{"rules": "strict"}', 'block2-wf3', NOW(), NOW()),
('block4-wf3', 'wf3', 'decision', 'Data Quality Check', 300, 0, true, '{}', '{"pass": "block5-wf3", "fail": "block6-wf3"}', '{"threshold": 0.95}', 'block3-wf3', NOW(), NOW()),
('block5-wf3', 'wf3', 'action', 'Load to Database', 400, -50, true, '{}', '{"loaded": "boolean"}', '{"target": "postgres"}', 'block4-wf3', NOW(), NOW()),
('block6-wf3', 'wf3', 'action', 'Error Handling', 400, 50, true, '{}', '{"logged": "boolean"}', '{"action": "alert"}', 'block4-wf3', NOW(), NOW());

-- Additional 50+ synthetic entries with varied types, positions, hierarchies, and data patterns

-- Workflow 4
INSERT INTO workflow_rows (id, name, description, user_id, workspace_id, folder_id, color, variables, is_published, created_at, updated_at, last_synced, state)
VALUES 
('wf4', 'Notification System', 'Multi-channel notification workflow', 'user456', 'ws2', NULL, '#BE185D', '{"channels": ["email", "sms", "slack"]}', true, NOW(), NOW(), NOW(), '{}');

INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block1-wf4', 'wf4', 'starter', 'Event Trigger', 0, 0, true, '{}', '{"event": "triggered"}', '{"source": "webhook"}', NULL, NOW(), NOW()),
('block2-wf4', 'wf4', 'action', 'Format Message', 100, 0, true, '{}', '{"formatted": "message"}', '{"template": "standard"}', 'block1-wf4', NOW(), NOW()),
('block3-wf4', 'wf4', 'loop', 'Send to Channels', 200, 0, true, '{}', '{"sent": "array"}', '{"channels": ["email", "sms", "slack"]}', 'block2-wf4', NOW(), NOW()),
('block4-wf4', 'wf4', 'action', 'Email Notification', 300, -50, true, '{}', '{"delivered": "boolean"}', '{"provider": "sendgrid"}', 'block3-wf4', NOW(), NOW()),
('block5-wf4', 'wf4', 'action', 'SMS Notification', 300, 0, true, '{}', '{"delivered": "boolean"}', '{"provider": "twilio"}', 'block3-wf4', NOW(), NOW()),
('block6-wf4', 'wf4', 'action', 'Slack Notification', 300, 50, true, '{}', '{"delivered": "boolean"}', '{"provider": "slack"}', 'block3-wf4', NOW(), NOW());

-- Workflow 5
INSERT INTO workflow_rows (id, name, description, user_id, workspace_id, folder_id, color, variables, is_published, created_at, updated_at, last_synced, state)
VALUES 
('wf5', 'Customer Onboarding', 'Automated customer onboarding process', 'user789', 'ws3', NULL, '#1E40AF', '{"steps": ["welcome", "setup", "training"]}', false, NOW(), NOW(), NOW(), '{}');

INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block1-wf5', 'wf5', 'starter', 'New Signup', 0, 0, true, '{}', '{"customer": "object"}', '{"source": "signup"}', NULL, NOW(), NOW()),
('block2-wf5', 'wf5', 'action', 'Send Welcome Email', 100, 0, true, '{}', '{"sent": "boolean"}', '{"template": "welcome"}', 'block1-wf5', NOW(), NOW()),
('block3-wf5', 'wf5', 'wait', 'Wait 24 Hours', 200, 0, true, '{}', '{"completed": "boolean"}', '{"duration": "24h"}', 'block2-wf5', NOW(), NOW()),
('block4-wf5', 'wf5', 'action', 'Account Setup', 300, 0, true, '{}', '{"setup": "boolean"}', '{"steps": ["profile", "payment"]}', 'block3-wf5', NOW(), NOW()),
('block5-wf5', 'wf5', 'action', 'Training Invitation', 400, 0, true, '{}', '{"invited": "boolean"}', '{"platform": "zoom"}', 'block4-wf5', NOW(), NOW()),
('block6-wf5', 'wf5', 'output', 'Update CRM', 500, 0, true, '{}', '{"updated": "boolean"}', '{"system": "hubspot"}', 'block5-wf5', NOW(), NOW());

-- Additional blocks to reach 50+ entries
-- More varied blocks for existing workflows and new workflows

-- Additional blocks for wf1
INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block6-wf1', 'wf1', 'loop', 'Retry Mechanism', 400, 0, true, '{}', '{"retry": "object"}', '{"attempts": 3}', 'block5-wf1', NOW(), NOW()),
('block7-wf1', 'wf1', 'output', 'Log Result', 500, 0, true, '{}', '{"logged": "boolean"}', '{"level": "info"}', 'block6-wf1', NOW(), NOW());

-- Additional blocks for wf2
INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block7-wf2', 'wf2', 'action', 'Audit Trail', 500, 0, true, '{}', '{"recorded": "boolean"}', '{"system": "audit"}', 'block6-wf2', NOW(), NOW());

-- Additional blocks for wf3
INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block7-wf3', 'wf3', 'output', 'Generate Report', 500, 0, true, '{}', '{"report": "object"}', '{"format": "pdf"}', 'block6-wf3', NOW(), NOW());

-- Workflow 6
INSERT INTO workflow_rows (id, name, description, user_id, workspace_id, folder_id, color, variables, is_published, created_at, updated_at, last_synced, state)
VALUES 
('wf6', 'Inventory Management', 'Stock level monitoring and reordering', 'user101', 'ws1', NULL, '#15803D', '{"threshold": 10, "supplier": "default"}', true, NOW(), NOW(), NOW(), '{}');

INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block1-wf6', 'wf6', 'starter', 'Stock Check', 0, 0, true, '{}', '{"levels": "object"}', '{"frequency": "hourly"}', NULL, NOW(), NOW()),
('block2-wf6', 'wf6', 'decision', 'Low Stock?', 100, 0, true, '{}', '{"yes": "block3-wf6", "no": "block4-wf6"}', '{"threshold": 10}', 'block1-wf6', NOW(), NOW()),
('block3-wf6', 'wf6', 'action', 'Create PO', 200, -50, true, '{}', '{"po": "object"}', '{"supplier": "default"}', 'block2-wf6', NOW(), NOW()),
('block4-wf6', 'wf6', 'action', 'Update Dashboard', 200, 50, true, '{}', '{"updated": "boolean"}', '{"system": "bi"}', 'block2-wf6', NOW(), NOW()),
('block5-wf6', 'wf6', 'output', 'Notify Manager', 300, -50, true, '{}', '{"notified": "boolean"}', '{"method": "email"}', 'block3-wf6', NOW(), NOW());

-- Workflow 7
INSERT INTO workflow_rows (id, name, description, user_id, workspace_id, folder_id, color, variables, is_published, created_at, updated_at, last_synced, state)
VALUES 
('wf7', 'User Feedback Analysis', 'Process and categorize user feedback', 'user202', 'ws2', NULL, '#7C2D12', '{"sources": ["app", "email", "survey"]}', false, NOW(), NOW(), NOW(), '{}');

INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block1-wf7', 'wf7', 'starter', 'Feedback Collection', 0, 0, true, '{}', '{"feedback": "array"}', '{"sources": ["app", "email", "survey"]}', NULL, NOW(), NOW()),
('block2-wf7', 'wf7', 'action', 'Categorize Feedback', 100, 0, true, '{}', '{"categories": "object"}', '{"model": "sentiment"}', 'block1-wf7', NOW(), NOW()),
('block3-wf7', 'wf7', 'action', 'Extract Keywords', 200, 0, true, '{}', '{"keywords": "array"}', '{"method": "nlp"}', 'block2-wf7', NOW(), NOW()),
('block4-wf7', 'wf7', 'decision', 'Priority Level', 300, 0, true, '{}', '{"high": "block5-wf7", "normal": "block6-wf7"}', '{"threshold": 0.7}', 'block3-wf7', NOW(), NOW()),
('block5-wf7', 'wf7', 'action', 'Create Urgent Ticket', 400, -50, true, '{}', '{"ticket": "object"}', '{"priority": "high"}', 'block4-wf7', NOW(), NOW()),
('block6-wf7', 'wf7', 'action', 'Add to Backlog', 400, 50, true, '{}', '{"added": "boolean"}', '{"sprint": "next"}', 'block4-wf7', NOW(), NOW());

-- Additional blocks to reach our target
INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block7-wf6', 'wf6', 'action', 'Track Shipment', 400, -50, true, '{}', '{"tracking": "object"}', '{"carrier": "fedex"}', 'block5-wf6', NOW(), NOW()),
('block8-wf7', 'wf7', 'output', 'Generate Summary', 500, 0, true, '{}', '{"summary": "object"}', '{"format": "weekly"}', 'block6-wf7', NOW(), NOW()),
('block9-wf1', 'wf1', 'action', 'Archive Process', 600, 0, true, '{}', '{"archived": "boolean"}', '{"location": "storage"}', 'block7-wf1', NOW(), NOW()),
('block10-wf2', 'wf2', 'action', 'Compliance Check', 600, 0, true, '{}', '{"compliant": "boolean"}', '{"regulation": "sox"}', 'block7-wf2', NOW(), NOW()),
('block11-wf3', 'wf3', 'action', 'Backup Data', 600, 0, true, '{}', '{"backup": "object"}', '{"location": "cloud"}', 'block7-wf3', NOW(), NOW()),
('block12-wf4', 'wf4', 'action', 'Analytics Update', 400, 100, true, '{}', '{"updated": "boolean"}', '{"system": "mixpanel"}', 'block6-wf4', NOW(), NOW()),
('block13-wf5', 'wf5', 'action', 'Feedback Request', 600, 0, true, '{}', '{"requested": "boolean"}', '{"template": "nps"}', 'block7-wf5', NOW(), NOW()),
('block14-wf6', 'wf6', 'action', 'Cost Analysis', 500, -50, true, '{}', '{"analysis": "object"}', '{"method": "abc"}', 'block7-wf6', NOW(), NOW()),
('block15-wf7', 'wf7', 'action', 'Trend Analysis', 600, 0, true, '{}', '{"trends": "object"}', '{"period": "monthly"}', 'block8-wf7', NOW(), NOW());

-- More workflows to increase variety
-- Workflow 8
INSERT INTO workflow_rows (id, name, description, user_id, workspace_id, folder_id, color, variables, is_published, created_at, updated_at, last_synced, state)
VALUES 
('wf8', 'Security Monitoring', 'Continuous security threat detection', 'user303', 'ws3', NULL, '#BE185D', '{"alerts": "realtime"}', true, NOW(), NOW(), NOW(), '{}');

INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block1-wf8', 'wf8', 'starter', 'Log Monitor', 0, 0, true, '{}', '{"event": "log"}', '{"source": "syslog"}', NULL, NOW(), NOW()),
('block2-wf8', 'wf8', 'action', 'Threat Detection', 100, 0, true, '{}', '{"threats": "array"}', '{"engine": "ai"}', 'block1-wf8', NOW(), NOW()),
('block3-wf8', 'wf8', 'decision', 'Severity Level', 200, 0, true, '{}', '{"critical": "block4-wf8", "warning": "block5-wf8"}', '{"threshold": 0.8}', 'block2-wf8', NOW(), NOW()),
('block4-wf8', 'wf8', 'action', 'Incident Response', 300, -50, true, '{}', '{"response": "object"}', '{"team": "noc"}', 'block3-wf8', NOW(), NOW()),
('block5-wf8', 'wf8', 'action', 'Alert Engineer', 300, 50, true, '{}', '{"alerted": "boolean"}', '{"method": "pagerduty"}', 'block3-wf8', NOW(), NOW());

-- Workflow 9
INSERT INTO workflow_rows (id, name, description, user_id, workspace_id, folder_id, color, variables, is_published, created_at, updated_at, last_synced, state)
VALUES 
('wf9', 'Content Publishing', 'Automated content publishing pipeline', 'user404', 'ws1', NULL, '#1E40AF', '{"platforms": ["web", "social"]}', false, NOW(), NOW(), NOW(), '{}');

INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block1-wf9', 'wf9', 'starter', 'Content Ready', 0, 0, true, '{}', '{"content": "object"}', '{"source": "cms"}', NULL, NOW(), NOW()),
('block2-wf9', 'wf9', 'action', 'SEO Optimization', 100, 0, true, '{}', '{"optimized": "boolean"}', '{"tool": "yoast"}', 'block1-wf9', NOW(), NOW()),
('block3-wf9', 'wf9', 'action', 'Generate Thumbnails', 200, 0, true, '{}', '{"thumbnails": "array"}', '{"sizes": ["small", "medium", "large"]}', 'block2-wf9', NOW(), NOW()),
('block4-wf9', 'wf9', 'parallel', 'Publish to Platforms', 300, 0, true, '{}', '{"published": "array"}', '{"platforms": ["web", "social"]}', 'block3-wf9', NOW(), NOW()),
('block5-wf9', 'wf9', 'action', 'Web Publishing', 400, -50, true, '{}', '{"published": "boolean"}', '{"platform": "wordpress"}', 'block4-wf9', NOW(), NOW()),
('block6-wf9', 'wf9', 'action', 'Social Sharing', 400, 50, true, '{}', '{"shared": "boolean"}', '{"platforms": ["twitter", "linkedin"]}', 'block4-wf9', NOW(), NOW());

-- Final additional blocks to reach 50+
INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, enabled, sub_blocks, outputs, data, parent_id, created_at, updated_at)
VALUES 
('block7-wf8', 'wf8', 'action', 'Forensics Analysis', 400, -50, true, '{}', '{"analysis": "object"}', '{"tool": "splunk"}', 'block4-wf8', NOW(), NOW()),
('block8-wf9', 'wf9', 'output', 'Analytics Setup', 500, 0, true, '{}', '{"setup": "boolean"}', '{"tool": "ga4"}', 'block6-wf9', NOW(), NOW()),
('block16-wf1', 'wf1', 'action', 'Performance Metrics', 700, 0, true, '{}', '{"metrics": "object"}', '{"type": "latency"}', 'block9-wf1', NOW(), NOW()),
('block17-wf2', 'wf2', 'action', 'Audit Report', 700, 0, true, '{}', '{"report": "object"}', '{"format": "pdf"}', 'block10-wf2', NOW(), NOW()),
('block18-wf3', 'wf3', 'action', 'Data Validation', 700, 0, true, '{}', '{"validated": "boolean"}', '{"rules": "business"}', 'block11-wf3', NOW(), NOW()),
('block19-wf4', 'wf4', 'action', 'User Engagement', 500, 100, true, '{}', '{"engagement": "object"}', '{"metrics": ["opens", "clicks"]}', 'block12-wf4', NOW(), NOW()),
('block20-wf5', 'wf5', 'action', 'Success Metrics', 700, 0, true, '{}', '{"metrics": "object"}', '{"kpi": "retention"}', 'block13-wf5', NOW(), NOW()),
('block21-wf6', 'wf6', 'action', 'Supplier Rating', 600, -50, true, '{}', '{"rating": "object"}', '{"scale": "5-star"}', 'block14-wf6', NOW(), NOW()),
('block22-wf7', 'wf7', 'action', 'Action Items', 700, 0, true, '{}', '{"items": "array"}', '{"priority": "high"}', 'block15-wf7', NOW(), NOW()),
('block23-wf8', 'wf8', 'action', 'Compliance Logging', 500, -50, true, '{}', '{"logged": "boolean"}', '{"standard": "iso27001"}', 'block7-wf8', NOW(), NOW()),
('block24-wf9', 'wf9', 'action', 'Content Archive', 600, 0, true, '{}', '{"archived": "boolean"}', '{"location": "s3"}', 'block8-wf9', NOW(), NOW()); 
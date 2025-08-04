
INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    '1de3a20b-293e-4433-b7a2-9fa57c69a5ed',
    'demo-user-1',
    'workspace-team',
    NULL,
    'Lead Capture System',
    'Automated lead qualification and CRM integration',
    '{"blocks": {"60f36dd8-bea3-46cc-8fa5-727d34a8e334": {"id": "60f36dd8-bea3-46cc-8fa5-727d34a8e334", "type": "starter", "name": "Lead Form Submission", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}, "webhookPath": {"id": "webhookPath", "type": "short-input", "value": "lead-capture"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "c7b28e16-8acc-4499-bbe0-426aa73dfe75": {"id": "c7b28e16-8acc-4499-bbe0-426aa73dfe75", "type": "agent", "name": "Lead Qualifier", "position": {"x": 300, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "Qualify leads based on company size, budget, and urgency. Score 1-10."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.3}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "2f6e2121-5e3b-4f35-a3f2-da1d84591845": {"id": "2f6e2121-5e3b-4f35-a3f2-da1d84591845", "type": "output", "name": "CRM Update", "position": {"x": 500, "y": 200}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "api"}, "channels": {"id": "channels", "type": "multi-select", "value": ["hubspot", "email"]}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "60f36dd8-bea3-46cc-8fa5-727d34a8e334", "target": "c7b28e16-8acc-4499-bbe0-426aa73dfe75", "sourceHandle": "output", "targetHandle": "input"}, {"source": "c7b28e16-8acc-4499-bbe0-426aa73dfe75", "target": "2f6e2121-5e3b-4f35-a3f2-da1d84591845", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.697666Z", "updatedAt": "2025-08-04T08:04:34.697667Z"}}',
    '#1E40AF',
    '2025-08-04T08:04:34.697730',
    '2025-07-28T08:04:34.697731',
    '2025-08-04T05:04:34.697736',
    True,
    '{"blocks": {"60f36dd8-bea3-46cc-8fa5-727d34a8e334": {"id": "60f36dd8-bea3-46cc-8fa5-727d34a8e334", "type": "starter", "name": "Lead Form Submission", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}, "webhookPath": {"id": "webhookPath", "type": "short-input", "value": "lead-capture"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "c7b28e16-8acc-4499-bbe0-426aa73dfe75": {"id": "c7b28e16-8acc-4499-bbe0-426aa73dfe75", "type": "agent", "name": "Lead Qualifier", "position": {"x": 300, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "Qualify leads based on company size, budget, and urgency. Score 1-10."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.3}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "2f6e2121-5e3b-4f35-a3f2-da1d84591845": {"id": "2f6e2121-5e3b-4f35-a3f2-da1d84591845", "type": "output", "name": "CRM Update", "position": {"x": 500, "y": 200}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "api"}, "channels": {"id": "channels", "type": "multi-select", "value": ["hubspot", "email"]}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "60f36dd8-bea3-46cc-8fa5-727d34a8e334", "target": "c7b28e16-8acc-4499-bbe0-426aa73dfe75", "sourceHandle": "output", "targetHandle": "input"}, {"source": "c7b28e16-8acc-4499-bbe0-426aa73dfe75", "target": "2f6e2121-5e3b-4f35-a3f2-da1d84591845", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.697666Z", "updatedAt": "2025-08-04T08:04:34.697667Z"}}',
    '2025-08-02T17:04:34.697764',
    '["user0@company.com", "user1@company.com"]',
    289,
    NULL,
    '{}',
    False,
    '{"category": "Sales & Marketing", "tags": ["sales_&_marketing", "automation", "ai"], "pricing": "usage-based", "rating": 3.8, "downloads": 2000}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '60f36dd8-bea3-46cc-8fa5-727d34a8e334',
    '1de3a20b-293e-4433-b7a2-9fa57c69a5ed',
    'starter',
    'Lead Form Submission',
    100,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}, "webhookPath": {"id": "webhookPath", "type": "short-input", "value": "lead-capture"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'c7b28e16-8acc-4499-bbe0-426aa73dfe75',
    '1de3a20b-293e-4433-b7a2-9fa57c69a5ed',
    'agent',
    'Lead Qualifier',
    300,
    200,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-4"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "Qualify leads based on company size, budget, and urgency. Score 1-10."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.3}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '2f6e2121-5e3b-4f35-a3f2-da1d84591845',
    '1de3a20b-293e-4433-b7a2-9fa57c69a5ed',
    'output',
    'CRM Update',
    500,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"outputType": {"id": "outputType", "type": "dropdown", "value": "api"}, "channels": {"id": "channels", "type": "multi-select", "value": ["hubspot", "email"]}}',
    '{"success": "boolean", "message": "string"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    'a5875e2b-3c85-4803-93bb-6fff7bc2084d',
    'demo-user-29',
    'workspace-enterprise',
    NULL,
    'Daily Analytics Report',
    'Automated daily performance reporting',
    '{"blocks": {"d956896d-174c-4614-9da1-bd1bf60da6c4": {"id": "d956896d-174c-4614-9da1-bd1bf60da6c4", "type": "starter", "name": "Daily Report Trigger", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}, "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "daily"}, "dailyTime": {"id": "dailyTime", "type": "short-input", "value": "09:00"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "c2a2dc57-546b-434e-ab9f-da4d2bcee1eb": {"id": "c2a2dc57-546b-434e-ab9f-da4d2bcee1eb", "type": "api", "name": "Analytics Data", "position": {"x": 300, "y": 200}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.analytics.com/daily-stats"}, "method": {"id": "method", "type": "dropdown", "value": "GET"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "f36283b2-cdb6-4128-b6c2-bceb70758b4e": {"id": "f36283b2-cdb6-4128-b6c2-bceb70758b4e", "type": "agent", "name": "Report Generator", "position": {"x": 500, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "Generate daily performance report with insights and recommendations."}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "8b2be019-0e44-4087-9531-f0df97851d0b": {"id": "8b2be019-0e44-4087-9531-f0df97851d0b", "type": "output", "name": "Email Report", "position": {"x": 700, "y": 200}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "email"}, "channels": {"id": "channels", "type": "multi-select", "value": ["email"]}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "d956896d-174c-4614-9da1-bd1bf60da6c4", "target": "c2a2dc57-546b-434e-ab9f-da4d2bcee1eb", "sourceHandle": "output", "targetHandle": "input"}, {"source": "c2a2dc57-546b-434e-ab9f-da4d2bcee1eb", "target": "f36283b2-cdb6-4128-b6c2-bceb70758b4e", "sourceHandle": "output", "targetHandle": "input"}, {"source": "f36283b2-cdb6-4128-b6c2-bceb70758b4e", "target": "8b2be019-0e44-4087-9531-f0df97851d0b", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.697829Z", "updatedAt": "2025-08-04T08:04:34.697830Z"}}',
    '#BE185D',
    '2025-08-04T08:04:34.697945',
    '2025-07-22T08:04:34.697946',
    '2025-08-04T05:04:34.697949',
    False,
    NULL,
    '2025-08-02T12:04:34.697952',
    '["user0@company.com", "user1@company.com", "user2@company.com"]',
    6,
    '2025-08-03T19:28:34.697960',
    '{}',
    True,
    '{"category": "Analytics", "tags": ["analytics", "automation", "ai"], "pricing": "usage-based", "rating": 4.9, "downloads": 2067}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'd956896d-174c-4614-9da1-bd1bf60da6c4',
    'a5875e2b-3c85-4803-93bb-6fff7bc2084d',
    'starter',
    'Daily Report Trigger',
    100,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}, "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "daily"}, "dailyTime": {"id": "dailyTime", "type": "short-input", "value": "09:00"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'c2a2dc57-546b-434e-ab9f-da4d2bcee1eb',
    'a5875e2b-3c85-4803-93bb-6fff7bc2084d',
    'api',
    'Analytics Data',
    300,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.analytics.com/daily-stats"}, "method": {"id": "method", "type": "dropdown", "value": "GET"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'f36283b2-cdb6-4128-b6c2-bceb70758b4e',
    'a5875e2b-3c85-4803-93bb-6fff7bc2084d',
    'agent',
    'Report Generator',
    500,
    200,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "claude-3"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "Generate daily performance report with insights and recommendations."}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '8b2be019-0e44-4087-9531-f0df97851d0b',
    'a5875e2b-3c85-4803-93bb-6fff7bc2084d',
    'output',
    'Email Report',
    700,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"outputType": {"id": "outputType", "type": "dropdown", "value": "email"}, "channels": {"id": "channels", "type": "multi-select", "value": ["email"]}}',
    '{"success": "boolean", "message": "string"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    'b1b0140f-4cf9-408e-bf5c-1c789651efae',
    'demo-user-74',
    'workspace-enterprise',
    NULL,
    'Webhook Handler',
    'Process incoming webhooks and send alerts',
    '{"blocks": {"1c154f33-778d-4004-a2c7-703e3a1508e0": {"id": "1c154f33-778d-4004-a2c7-703e3a1508e0", "type": "starter", "name": "Webhook Receiver", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "11b72b99-7e5d-481d-82db-be9fcd57eb6b": {"id": "11b72b99-7e5d-481d-82db-be9fcd57eb6b", "type": "agent", "name": "Data Processor", "position": {"x": 300, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-3.5-turbo"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "Process webhook data and extract key information."}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "1b0978c6-5ff0-45e8-9aae-b5184f120e44": {"id": "1b0978c6-5ff0-45e8-9aae-b5184f120e44", "type": "output", "name": "Slack Alert", "position": {"x": 500, "y": 200}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "slack"}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "1c154f33-778d-4004-a2c7-703e3a1508e0", "target": "11b72b99-7e5d-481d-82db-be9fcd57eb6b", "sourceHandle": "output", "targetHandle": "input"}, {"source": "11b72b99-7e5d-481d-82db-be9fcd57eb6b", "target": "1b0978c6-5ff0-45e8-9aae-b5184f120e44", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698001Z", "updatedAt": "2025-08-04T08:04:34.698002Z"}}',
    '#15803D',
    '2025-08-04T08:04:34.698023',
    '2025-07-10T08:04:34.698023',
    '2025-08-03T23:04:34.698025',
    False,
    NULL,
    NULL,
    '["user0@company.com", "user1@company.com"]',
    26,
    '2025-08-04T04:58:34.698033',
    '{}',
    False,
    '{"category": "Integration", "tags": ["integration", "automation", "ai"], "pricing": "usage-based", "rating": 3.7, "downloads": 3518}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '1c154f33-778d-4004-a2c7-703e3a1508e0',
    'b1b0140f-4cf9-408e-bf5c-1c789651efae',
    'starter',
    'Webhook Receiver',
    100,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '11b72b99-7e5d-481d-82db-be9fcd57eb6b',
    'b1b0140f-4cf9-408e-bf5c-1c789651efae',
    'agent',
    'Data Processor',
    300,
    200,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-3.5-turbo"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "Process webhook data and extract key information."}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '1b0978c6-5ff0-45e8-9aae-b5184f120e44',
    'b1b0140f-4cf9-408e-bf5c-1c789651efae',
    'output',
    'Slack Alert',
    500,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"outputType": {"id": "outputType", "type": "dropdown", "value": "slack"}}',
    '{"success": "boolean", "message": "string"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    '5277ffae-0e9e-4bb6-8c58-aaea00ebb6d8',
    'demo-user-99',
    'workspace-enterprise',
    NULL,
    'Data Sync Pipeline',
    'Scheduled data synchronization',
    '{"blocks": {"6cfa097c-f790-4328-8778-326c5ab4d0c6": {"id": "6cfa097c-f790-4328-8778-326c5ab4d0c6", "type": "starter", "name": "Data Sync", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "92406eb7-f49f-45ec-83b5-add1099a613b": {"id": "92406eb7-f49f-45ec-83b5-add1099a613b", "type": "api", "name": "External API", "position": {"x": 300, "y": 200}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.example.com/data"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "61e23c4f-baa4-43bb-8bea-768ce4b941a5": {"id": "61e23c4f-baa4-43bb-8bea-768ce4b941a5", "type": "output", "name": "Database Update", "position": {"x": 500, "y": 200}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "database"}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "6cfa097c-f790-4328-8778-326c5ab4d0c6", "target": "92406eb7-f49f-45ec-83b5-add1099a613b", "sourceHandle": "output", "targetHandle": "input"}, {"source": "92406eb7-f49f-45ec-83b5-add1099a613b", "target": "61e23c4f-baa4-43bb-8bea-768ce4b941a5", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698070Z", "updatedAt": "2025-08-04T08:04:34.698071Z"}}',
    '#BE185D',
    '2025-08-04T08:04:34.698090',
    '2025-07-19T08:04:34.698091',
    '2025-08-04T00:04:34.698093',
    True,
    NULL,
    '2025-08-04T01:04:34.698096',
    '["user0@company.com", "user1@company.com"]',
    263,
    '2025-08-03T13:49:34.698102',
    '{}',
    False,
    '{"category": "Data Processing", "tags": ["data_processing", "automation", "ai"], "pricing": "premium", "rating": 3.6, "downloads": 1606}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '6cfa097c-f790-4328-8778-326c5ab4d0c6',
    '5277ffae-0e9e-4bb6-8c58-aaea00ebb6d8',
    'starter',
    'Data Sync',
    100,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '92406eb7-f49f-45ec-83b5-add1099a613b',
    '5277ffae-0e9e-4bb6-8c58-aaea00ebb6d8',
    'api',
    'External API',
    300,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.example.com/data"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '61e23c4f-baa4-43bb-8bea-768ce4b941a5',
    '5277ffae-0e9e-4bb6-8c58-aaea00ebb6d8',
    'output',
    'Database Update',
    500,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"outputType": {"id": "outputType", "type": "dropdown", "value": "database"}}',
    '{"success": "boolean", "message": "string"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    'aacc703b-b064-429f-8c5d-14cd2835f4c5',
    'demo-user-75',
    'workspace-team',
    NULL,
    'Alert System',
    'Multi-channel notification system',
    '{"blocks": {"034cbe28-1fef-403f-9d49-b9039df78e9a": {"id": "034cbe28-1fef-403f-9d49-b9039df78e9a", "type": "starter", "name": "Alert Trigger", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "9545fd33-98a9-46b0-9708-4802909e8236": {"id": "9545fd33-98a9-46b0-9708-4802909e8236", "type": "output", "name": "Multi-Channel Alert", "position": {"x": 300, "y": 200}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "multi"}, "channels": {"id": "channels", "type": "multi-select", "value": ["email", "sms", "slack"]}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "034cbe28-1fef-403f-9d49-b9039df78e9a", "target": "9545fd33-98a9-46b0-9708-4802909e8236", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698132Z", "updatedAt": "2025-08-04T08:04:34.698132Z"}}',
    '#BE185D',
    '2025-08-04T08:04:34.698148',
    '2025-07-26T08:04:34.698148',
    '2025-08-03T18:04:34.698150',
    True,
    '{"blocks": {"034cbe28-1fef-403f-9d49-b9039df78e9a": {"id": "034cbe28-1fef-403f-9d49-b9039df78e9a", "type": "starter", "name": "Alert Trigger", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "9545fd33-98a9-46b0-9708-4802909e8236": {"id": "9545fd33-98a9-46b0-9708-4802909e8236", "type": "output", "name": "Multi-Channel Alert", "position": {"x": 300, "y": 200}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "multi"}, "channels": {"id": "channels", "type": "multi-select", "value": ["email", "sms", "slack"]}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "034cbe28-1fef-403f-9d49-b9039df78e9a", "target": "9545fd33-98a9-46b0-9708-4802909e8236", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698132Z", "updatedAt": "2025-08-04T08:04:34.698132Z"}}',
    '2025-08-02T07:04:34.698164',
    '["user0@company.com", "user1@company.com", "user2@company.com"]',
    494,
    '2025-08-04T03:26:34.698171',
    '{}',
    False,
    '{"category": "Communication", "tags": ["communication", "automation", "ai"], "pricing": "usage-based", "rating": 4.3, "downloads": 783}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '034cbe28-1fef-403f-9d49-b9039df78e9a',
    'aacc703b-b064-429f-8c5d-14cd2835f4c5',
    'starter',
    'Alert Trigger',
    100,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '9545fd33-98a9-46b0-9708-4802909e8236',
    'aacc703b-b064-429f-8c5d-14cd2835f4c5',
    'output',
    'Multi-Channel Alert',
    300,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"outputType": {"id": "outputType", "type": "dropdown", "value": "multi"}, "channels": {"id": "channels", "type": "multi-select", "value": ["email", "sms", "slack"]}}',
    '{"success": "boolean", "message": "string"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    'c664c7dc-8599-404f-a6c8-e93675c87a96',
    'demo-user-41',
    'workspace-personal',
    NULL,
    'Marketing Automation',
    'Automated audience segmentation and content generation',
    '{"blocks": {"0d7927f7-38fd-4dd7-b0ee-bdadb6f2f7ec": {"id": "0d7927f7-38fd-4dd7-b0ee-bdadb6f2f7ec", "type": "starter", "name": "Campaign Trigger", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "185d935b-3f5e-4df2-83cc-d1d6b49fd440": {"id": "185d935b-3f5e-4df2-83cc-d1d6b49fd440", "type": "agent", "name": "Audience Segmentation", "position": {"x": 300, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "ba0dc9c3-add3-413e-9390-bbd29d7c5b3e": {"id": "ba0dc9c3-add3-413e-9390-bbd29d7c5b3e", "type": "agent", "name": "Content Generator", "position": {"x": 500, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "676acbf4-a878-428e-bafc-308304aae73e": {"id": "676acbf4-a878-428e-bafc-308304aae73e", "type": "api", "name": "Email Campaign", "position": {"x": 700, "y": 200}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.mailchimp.com/3.0/campaigns"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "0d7927f7-38fd-4dd7-b0ee-bdadb6f2f7ec", "target": "185d935b-3f5e-4df2-83cc-d1d6b49fd440", "sourceHandle": "output", "targetHandle": "input"}, {"source": "185d935b-3f5e-4df2-83cc-d1d6b49fd440", "target": "ba0dc9c3-add3-413e-9390-bbd29d7c5b3e", "sourceHandle": "output", "targetHandle": "input"}, {"source": "ba0dc9c3-add3-413e-9390-bbd29d7c5b3e", "target": "676acbf4-a878-428e-bafc-308304aae73e", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698231Z", "updatedAt": "2025-08-04T08:04:34.698232Z"}}',
    '#15803D',
    '2025-08-04T08:04:34.698257',
    '2025-07-14T08:04:34.698257',
    '2025-08-03T10:04:34.698259',
    False,
    NULL,
    '2025-08-04T05:04:34.698263',
    '["user0@company.com", "user1@company.com"]',
    236,
    NULL,
    '{}',
    False,
    '{"category": "Marketing", "tags": ["marketing", "automation", "ai"], "pricing": "premium", "rating": 4.5, "downloads": 4336}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '0d7927f7-38fd-4dd7-b0ee-bdadb6f2f7ec',
    'c664c7dc-8599-404f-a6c8-e93675c87a96',
    'starter',
    'Campaign Trigger',
    100,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '185d935b-3f5e-4df2-83cc-d1d6b49fd440',
    'c664c7dc-8599-404f-a6c8-e93675c87a96',
    'agent',
    'Audience Segmentation',
    300,
    200,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'ba0dc9c3-add3-413e-9390-bbd29d7c5b3e',
    'c664c7dc-8599-404f-a6c8-e93675c87a96',
    'agent',
    'Content Generator',
    500,
    200,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "claude-3"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '676acbf4-a878-428e-bafc-308304aae73e',
    'c664c7dc-8599-404f-a6c8-e93675c87a96',
    'api',
    'Email Campaign',
    700,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.mailchimp.com/3.0/campaigns"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    '3dc11bbd-5f5e-42ad-9aec-b61809d67fbd',
    'demo-user-92',
    'workspace-personal',
    NULL,
    'Customer Support Automation',
    'Automated ticket classification and response',
    '{"blocks": {"eeacf8c3-8d94-46ac-bd98-dfdd7384693a": {"id": "eeacf8c3-8d94-46ac-bd98-dfdd7384693a", "type": "starter", "name": "Support Ticket", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "07d85164-372b-4d0b-bf04-5b2ffd7b89c8": {"id": "07d85164-372b-4d0b-bf04-5b2ffd7b89c8", "type": "agent", "name": "Ticket Classifier", "position": {"x": 300, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "eb2ff996-40a2-4fca-b66e-5449edd0db46": {"id": "eb2ff996-40a2-4fca-b66e-5449edd0db46", "type": "agent", "name": "Support Agent", "position": {"x": 500, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "8cefa38c-6810-426e-bb9d-e73bd53493a3": {"id": "8cefa38c-6810-426e-bb9d-e73bd53493a3", "type": "output", "name": "Customer Response", "position": {"x": 700, "y": 200}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "email"}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "eeacf8c3-8d94-46ac-bd98-dfdd7384693a", "target": "07d85164-372b-4d0b-bf04-5b2ffd7b89c8", "sourceHandle": "output", "targetHandle": "input"}, {"source": "07d85164-372b-4d0b-bf04-5b2ffd7b89c8", "target": "eb2ff996-40a2-4fca-b66e-5449edd0db46", "sourceHandle": "output", "targetHandle": "input"}, {"source": "eb2ff996-40a2-4fca-b66e-5449edd0db46", "target": "8cefa38c-6810-426e-bb9d-e73bd53493a3", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698314Z", "updatedAt": "2025-08-04T08:04:34.698314Z"}}',
    '#3972F6',
    '2025-08-04T08:04:34.698337',
    '2025-07-18T08:04:34.698338',
    '2025-08-03T17:04:34.698340',
    True,
    NULL,
    '2025-08-04T05:04:34.698343',
    '["user0@company.com"]',
    496,
    '2025-08-03T21:37:34.698349',
    '{}',
    True,
    '{"category": "Customer Service", "tags": ["customer_service", "automation", "ai"], "pricing": "premium", "rating": 4.3, "downloads": 1036}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'eeacf8c3-8d94-46ac-bd98-dfdd7384693a',
    '3dc11bbd-5f5e-42ad-9aec-b61809d67fbd',
    'starter',
    'Support Ticket',
    100,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '07d85164-372b-4d0b-bf04-5b2ffd7b89c8',
    '3dc11bbd-5f5e-42ad-9aec-b61809d67fbd',
    'agent',
    'Ticket Classifier',
    300,
    200,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'eb2ff996-40a2-4fca-b66e-5449edd0db46',
    '3dc11bbd-5f5e-42ad-9aec-b61809d67fbd',
    'agent',
    'Support Agent',
    500,
    200,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "claude-3"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '8cefa38c-6810-426e-bb9d-e73bd53493a3',
    '3dc11bbd-5f5e-42ad-9aec-b61809d67fbd',
    'output',
    'Customer Response',
    700,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"outputType": {"id": "outputType", "type": "dropdown", "value": "email"}}',
    '{"success": "boolean", "message": "string"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    'b5d37a0f-f441-4952-b022-a4fb8d09771b',
    'demo-user-trader',
    'crypto-trading-workspace',
    NULL,
    'Advanced Crypto Trading Bot',
    '24/7 autonomous crypto trading with advanced risk management, technical analysis, and multi-channel notifications',
    '{"blocks": {"30e4a79d-a018-488d-89f1-a29a33cf93b0": {"id": "30e4a79d-a018-488d-89f1-a29a33cf93b0", "type": "starter", "name": "Market Monitor", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}, "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "minutes"}, "minutesInterval": {"id": "minutesInterval", "type": "short-input", "value": "5"}, "timezone": {"id": "timezone", "type": "dropdown", "value": "UTC"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "245db495-03cd-4736-b06b-fa6391945199": {"id": "245db495-03cd-4736-b06b-fa6391945199", "type": "api", "name": "CoinGecko Price Data", "position": {"x": 300, "y": 200}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.coingecko.com/api/v3/simple/price"}, "method": {"id": "method", "type": "dropdown", "value": "GET"}, "params": {"id": "params", "type": "table", "value": [{"id": "d8ec1035-4600-45ac-b680-c61ec74c0ef6", "cells": {"Key": "ids", "Value": "bitcoin,ethereum,solana"}}, {"id": "a930b1b1-75c6-4799-87dc-a26e50171107", "cells": {"Key": "vs_currencies", "Value": "usd"}}, {"id": "3257ae29-27b3-400d-b17d-101615c8b4f4", "cells": {"Key": "include_24hr_change", "Value": "true"}}]}, "headers": {"id": "headers", "type": "table", "value": [{"id": "b1216260-e1ed-4f9f-905b-2299775b1bd7", "cells": {"Key": "Accept", "Value": "application/json"}}]}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "bb00ef60-748a-43bf-a7e2-d2ae24ff2770": {"id": "bb00ef60-748a-43bf-a7e2-d2ae24ff2770", "type": "agent", "name": "Trading Decision Agent", "position": {"x": 500, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a professional crypto trading agent. Analyze market data and make trading decisions based on: 1) Stop-loss at -5% 2) Take-profit at +10% 3) RSI indicators 4) Volume analysis 5) 24h price change. Respond with clear BUY/SELL/HOLD decisions and reasoning."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.3}, "tools": {"id": "tools", "type": "tool-input", "value": [{"type": "market_analysis", "title": "Market Analysis", "enabled": true}, {"type": "risk_calculator", "title": "Risk Calculator", "enabled": true}, {"type": "technical_indicators", "title": "Technical Indicators", "enabled": true}]}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "6334937a-9d4c-4e9b-aa48-8a7cde225286": {"id": "6334937a-9d4c-4e9b-aa48-8a7cde225286", "type": "api", "name": "Execute Trade Order", "position": {"x": 700, "y": 200}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.binance.com/api/v3/order"}, "method": {"id": "method", "type": "dropdown", "value": "POST"}, "headers": {"id": "headers", "type": "table", "value": [{"id": "72c3e397-c9a7-4861-bce5-186c2f0c1ec6", "cells": {"Key": "X-MBX-APIKEY", "Value": "{{BINANCE_API_KEY}}"}}, {"id": "d6ba52c9-1072-4182-89a6-f25d7fdf24d8", "cells": {"Key": "Content-Type", "Value": "application/json"}}]}, "body": {"id": "body", "type": "code", "value": "{\n  \"symbol\": \"{{TRADING_PAIR}}\",\n  \"side\": \"{{TRADE_SIDE}}\",\n  \"type\": \"MARKET\",\n  \"quantity\": \"{{TRADE_AMOUNT}}\"\n}"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "cde26915-766a-488d-8024-095042a68c74": {"id": "cde26915-766a-488d-8024-095042a68c74", "type": "output", "name": "Trade Notification", "position": {"x": 900, "y": 200}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "multi"}, "channels": {"id": "channels", "type": "multi-select", "value": ["email", "slack", "discord"]}, "emailConfig": {"id": "emailConfig", "type": "json", "value": {"to": "trader@cryptobot.com", "subject": "Trade Executed: {{TRADING_PAIR}}"}}, "slackConfig": {"id": "slackConfig", "type": "json", "value": {"webhook": "https://hooks.slack.com/services/...", "channel": "#trading"}}, "discordConfig": {"id": "discordConfig", "type": "json", "value": {"webhook": "https://discord.com/api/webhooks/..."}}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "30e4a79d-a018-488d-89f1-a29a33cf93b0", "target": "245db495-03cd-4736-b06b-fa6391945199", "sourceHandle": "output", "targetHandle": "input"}, {"source": "245db495-03cd-4736-b06b-fa6391945199", "target": "bb00ef60-748a-43bf-a7e2-d2ae24ff2770", "sourceHandle": "output", "targetHandle": "input"}, {"source": "bb00ef60-748a-43bf-a7e2-d2ae24ff2770", "target": "6334937a-9d4c-4e9b-aa48-8a7cde225286", "sourceHandle": "output", "targetHandle": "input"}, {"source": "6334937a-9d4c-4e9b-aa48-8a7cde225286", "target": "cde26915-766a-488d-8024-095042a68c74", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {"BINANCE_API_KEY": {"type": "secret", "value": ""}, "BINANCE_SECRET_KEY": {"type": "secret", "value": ""}, "TRADING_PAIR": {"type": "string", "value": "BTCUSDT"}, "STOP_LOSS_PCT": {"type": "number", "value": -5}, "TAKE_PROFIT_PCT": {"type": "number", "value": 10}, "TRADE_AMOUNT": {"type": "number", "value": 0.001}}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698428Z", "updatedAt": "2025-08-04T08:04:34.698429Z"}}',
    '#15803D',
    '2025-08-04T08:04:34.698486',
    '2025-08-04T08:04:34.698486',
    '2025-08-04T08:04:34.698487',
    True,
    '{"blocks": {"30e4a79d-a018-488d-89f1-a29a33cf93b0": {"id": "30e4a79d-a018-488d-89f1-a29a33cf93b0", "type": "starter", "name": "Market Monitor", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}, "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "minutes"}, "minutesInterval": {"id": "minutesInterval", "type": "short-input", "value": "5"}, "timezone": {"id": "timezone", "type": "dropdown", "value": "UTC"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "245db495-03cd-4736-b06b-fa6391945199": {"id": "245db495-03cd-4736-b06b-fa6391945199", "type": "api", "name": "CoinGecko Price Data", "position": {"x": 300, "y": 200}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.coingecko.com/api/v3/simple/price"}, "method": {"id": "method", "type": "dropdown", "value": "GET"}, "params": {"id": "params", "type": "table", "value": [{"id": "d8ec1035-4600-45ac-b680-c61ec74c0ef6", "cells": {"Key": "ids", "Value": "bitcoin,ethereum,solana"}}, {"id": "a930b1b1-75c6-4799-87dc-a26e50171107", "cells": {"Key": "vs_currencies", "Value": "usd"}}, {"id": "3257ae29-27b3-400d-b17d-101615c8b4f4", "cells": {"Key": "include_24hr_change", "Value": "true"}}]}, "headers": {"id": "headers", "type": "table", "value": [{"id": "b1216260-e1ed-4f9f-905b-2299775b1bd7", "cells": {"Key": "Accept", "Value": "application/json"}}]}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "bb00ef60-748a-43bf-a7e2-d2ae24ff2770": {"id": "bb00ef60-748a-43bf-a7e2-d2ae24ff2770", "type": "agent", "name": "Trading Decision Agent", "position": {"x": 500, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a professional crypto trading agent. Analyze market data and make trading decisions based on: 1) Stop-loss at -5% 2) Take-profit at +10% 3) RSI indicators 4) Volume analysis 5) 24h price change. Respond with clear BUY/SELL/HOLD decisions and reasoning."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.3}, "tools": {"id": "tools", "type": "tool-input", "value": [{"type": "market_analysis", "title": "Market Analysis", "enabled": true}, {"type": "risk_calculator", "title": "Risk Calculator", "enabled": true}, {"type": "technical_indicators", "title": "Technical Indicators", "enabled": true}]}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "6334937a-9d4c-4e9b-aa48-8a7cde225286": {"id": "6334937a-9d4c-4e9b-aa48-8a7cde225286", "type": "api", "name": "Execute Trade Order", "position": {"x": 700, "y": 200}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.binance.com/api/v3/order"}, "method": {"id": "method", "type": "dropdown", "value": "POST"}, "headers": {"id": "headers", "type": "table", "value": [{"id": "72c3e397-c9a7-4861-bce5-186c2f0c1ec6", "cells": {"Key": "X-MBX-APIKEY", "Value": "{{BINANCE_API_KEY}}"}}, {"id": "d6ba52c9-1072-4182-89a6-f25d7fdf24d8", "cells": {"Key": "Content-Type", "Value": "application/json"}}]}, "body": {"id": "body", "type": "code", "value": "{\n  \"symbol\": \"{{TRADING_PAIR}}\",\n  \"side\": \"{{TRADE_SIDE}}\",\n  \"type\": \"MARKET\",\n  \"quantity\": \"{{TRADE_AMOUNT}}\"\n}"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "cde26915-766a-488d-8024-095042a68c74": {"id": "cde26915-766a-488d-8024-095042a68c74", "type": "output", "name": "Trade Notification", "position": {"x": 900, "y": 200}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "multi"}, "channels": {"id": "channels", "type": "multi-select", "value": ["email", "slack", "discord"]}, "emailConfig": {"id": "emailConfig", "type": "json", "value": {"to": "trader@cryptobot.com", "subject": "Trade Executed: {{TRADING_PAIR}}"}}, "slackConfig": {"id": "slackConfig", "type": "json", "value": {"webhook": "https://hooks.slack.com/services/...", "channel": "#trading"}}, "discordConfig": {"id": "discordConfig", "type": "json", "value": {"webhook": "https://discord.com/api/webhooks/..."}}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "30e4a79d-a018-488d-89f1-a29a33cf93b0", "target": "245db495-03cd-4736-b06b-fa6391945199", "sourceHandle": "output", "targetHandle": "input"}, {"source": "245db495-03cd-4736-b06b-fa6391945199", "target": "bb00ef60-748a-43bf-a7e2-d2ae24ff2770", "sourceHandle": "output", "targetHandle": "input"}, {"source": "bb00ef60-748a-43bf-a7e2-d2ae24ff2770", "target": "6334937a-9d4c-4e9b-aa48-8a7cde225286", "sourceHandle": "output", "targetHandle": "input"}, {"source": "6334937a-9d4c-4e9b-aa48-8a7cde225286", "target": "cde26915-766a-488d-8024-095042a68c74", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {"BINANCE_API_KEY": {"type": "secret", "value": ""}, "BINANCE_SECRET_KEY": {"type": "secret", "value": ""}, "TRADING_PAIR": {"type": "string", "value": "BTCUSDT"}, "STOP_LOSS_PCT": {"type": "number", "value": -5}, "TAKE_PROFIT_PCT": {"type": "number", "value": 10}, "TRADE_AMOUNT": {"type": "number", "value": 0.001}}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698428Z", "updatedAt": "2025-08-04T08:04:34.698429Z"}}',
    '2025-08-04T08:04:34.698538',
    '[]',
    887,
    '2025-08-04T07:59:34.698542',
    '{"TRADING_PAIR": "BTCUSDT", "STOP_LOSS_PCT": -5, "TAKE_PROFIT_PCT": 10}',
    True,
    '{"category": "Web3 Trading", "tags": ["crypto", "trading", "defi", "automation", "bitcoin", "ethereum"], "pricing": "usage-based", "rating": 4.8, "downloads": 2547, "featured": true}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '30e4a79d-a018-488d-89f1-a29a33cf93b0',
    'b5d37a0f-f441-4952-b022-a4fb8d09771b',
    'starter',
    'Market Monitor',
    100,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}, "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "minutes"}, "minutesInterval": {"id": "minutesInterval", "type": "short-input", "value": "5"}, "timezone": {"id": "timezone", "type": "dropdown", "value": "UTC"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '245db495-03cd-4736-b06b-fa6391945199',
    'b5d37a0f-f441-4952-b022-a4fb8d09771b',
    'api',
    'CoinGecko Price Data',
    300,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.coingecko.com/api/v3/simple/price"}, "method": {"id": "method", "type": "dropdown", "value": "GET"}, "params": {"id": "params", "type": "table", "value": [{"id": "d8ec1035-4600-45ac-b680-c61ec74c0ef6", "cells": {"Key": "ids", "Value": "bitcoin,ethereum,solana"}}, {"id": "a930b1b1-75c6-4799-87dc-a26e50171107", "cells": {"Key": "vs_currencies", "Value": "usd"}}, {"id": "3257ae29-27b3-400d-b17d-101615c8b4f4", "cells": {"Key": "include_24hr_change", "Value": "true"}}]}, "headers": {"id": "headers", "type": "table", "value": [{"id": "b1216260-e1ed-4f9f-905b-2299775b1bd7", "cells": {"Key": "Accept", "Value": "application/json"}}]}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'bb00ef60-748a-43bf-a7e2-d2ae24ff2770',
    'b5d37a0f-f441-4952-b022-a4fb8d09771b',
    'agent',
    'Trading Decision Agent',
    500,
    200,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-4"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a professional crypto trading agent. Analyze market data and make trading decisions based on: 1) Stop-loss at -5% 2) Take-profit at +10% 3) RSI indicators 4) Volume analysis 5) 24h price change. Respond with clear BUY/SELL/HOLD decisions and reasoning."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.3}, "tools": {"id": "tools", "type": "tool-input", "value": [{"type": "market_analysis", "title": "Market Analysis", "enabled": true}, {"type": "risk_calculator", "title": "Risk Calculator", "enabled": true}, {"type": "technical_indicators", "title": "Technical Indicators", "enabled": true}]}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '6334937a-9d4c-4e9b-aa48-8a7cde225286',
    'b5d37a0f-f441-4952-b022-a4fb8d09771b',
    'api',
    'Execute Trade Order',
    700,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.binance.com/api/v3/order"}, "method": {"id": "method", "type": "dropdown", "value": "POST"}, "headers": {"id": "headers", "type": "table", "value": [{"id": "72c3e397-c9a7-4861-bce5-186c2f0c1ec6", "cells": {"Key": "X-MBX-APIKEY", "Value": "{{BINANCE_API_KEY}}"}}, {"id": "d6ba52c9-1072-4182-89a6-f25d7fdf24d8", "cells": {"Key": "Content-Type", "Value": "application/json"}}]}, "body": {"id": "body", "type": "code", "value": "{\n  \"symbol\": \"{{TRADING_PAIR}}\",\n  \"side\": \"{{TRADE_SIDE}}\",\n  \"type\": \"MARKET\",\n  \"quantity\": \"{{TRADE_AMOUNT}}\"\n}"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'cde26915-766a-488d-8024-095042a68c74',
    'b5d37a0f-f441-4952-b022-a4fb8d09771b',
    'output',
    'Trade Notification',
    900,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"outputType": {"id": "outputType", "type": "dropdown", "value": "multi"}, "channels": {"id": "channels", "type": "multi-select", "value": ["email", "slack", "discord"]}, "emailConfig": {"id": "emailConfig", "type": "json", "value": {"to": "trader@cryptobot.com", "subject": "Trade Executed: {{TRADING_PAIR}}"}}, "slackConfig": {"id": "slackConfig", "type": "json", "value": {"webhook": "https://hooks.slack.com/services/...", "channel": "#trading"}}, "discordConfig": {"id": "discordConfig", "type": "json", "value": {"webhook": "https://discord.com/api/webhooks/..."}}}',
    '{"success": "boolean", "message": "string"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    'ccdcc9f7-f46c-4ef0-947f-eaada31278a7',
    'demo-user-4',
    'workspace-enterprise',
    NULL,
    'Content Generation Pipeline',
    'AI-powered content research, writing, and publishing',
    '{"blocks": {"e66ac923-8541-4843-84a8-7dcadd5eacb9": {"id": "e66ac923-8541-4843-84a8-7dcadd5eacb9", "type": "starter", "name": "Content Request", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "cee97950-46b1-45a7-9ba5-b37267547c78": {"id": "cee97950-46b1-45a7-9ba5-b37267547c78", "type": "agent", "name": "Research Agent", "position": {"x": 300, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "0937b1be-a43c-4a84-9dc6-f11173604c7c": {"id": "0937b1be-a43c-4a84-9dc6-f11173604c7c", "type": "agent", "name": "Content Writer", "position": {"x": 500, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "6e0adcff-5894-42bf-aada-6c5a960f6087": {"id": "6e0adcff-5894-42bf-aada-6c5a960f6087", "type": "api", "name": "Content Publisher", "position": {"x": 700, "y": 200}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.wordpress.com/wp/v2/posts"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "e66ac923-8541-4843-84a8-7dcadd5eacb9", "target": "cee97950-46b1-45a7-9ba5-b37267547c78", "sourceHandle": "output", "targetHandle": "input"}, {"source": "cee97950-46b1-45a7-9ba5-b37267547c78", "target": "0937b1be-a43c-4a84-9dc6-f11173604c7c", "sourceHandle": "output", "targetHandle": "input"}, {"source": "0937b1be-a43c-4a84-9dc6-f11173604c7c", "target": "6e0adcff-5894-42bf-aada-6c5a960f6087", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698588Z", "updatedAt": "2025-08-04T08:04:34.698589Z"}}',
    '#1E40AF',
    '2025-08-04T08:04:34.698613',
    '2025-07-06T08:04:34.698613',
    '2025-08-03T20:04:34.698615',
    False,
    '{"blocks": {"e66ac923-8541-4843-84a8-7dcadd5eacb9": {"id": "e66ac923-8541-4843-84a8-7dcadd5eacb9", "type": "starter", "name": "Content Request", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "cee97950-46b1-45a7-9ba5-b37267547c78": {"id": "cee97950-46b1-45a7-9ba5-b37267547c78", "type": "agent", "name": "Research Agent", "position": {"x": 300, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "0937b1be-a43c-4a84-9dc6-f11173604c7c": {"id": "0937b1be-a43c-4a84-9dc6-f11173604c7c", "type": "agent", "name": "Content Writer", "position": {"x": 500, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "6e0adcff-5894-42bf-aada-6c5a960f6087": {"id": "6e0adcff-5894-42bf-aada-6c5a960f6087", "type": "api", "name": "Content Publisher", "position": {"x": 700, "y": 200}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.wordpress.com/wp/v2/posts"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "e66ac923-8541-4843-84a8-7dcadd5eacb9", "target": "cee97950-46b1-45a7-9ba5-b37267547c78", "sourceHandle": "output", "targetHandle": "input"}, {"source": "cee97950-46b1-45a7-9ba5-b37267547c78", "target": "0937b1be-a43c-4a84-9dc6-f11173604c7c", "sourceHandle": "output", "targetHandle": "input"}, {"source": "0937b1be-a43c-4a84-9dc6-f11173604c7c", "target": "6e0adcff-5894-42bf-aada-6c5a960f6087", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698588Z", "updatedAt": "2025-08-04T08:04:34.698589Z"}}',
    NULL,
    '[]',
    261,
    '2025-08-04T03:21:34.698641',
    '{}',
    False,
    '{"category": "Content & Media", "tags": ["content_&_media", "automation", "ai"], "pricing": "usage-based", "rating": 4.7, "downloads": 178}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'e66ac923-8541-4843-84a8-7dcadd5eacb9',
    'ccdcc9f7-f46c-4ef0-947f-eaada31278a7',
    'starter',
    'Content Request',
    100,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'cee97950-46b1-45a7-9ba5-b37267547c78',
    'ccdcc9f7-f46c-4ef0-947f-eaada31278a7',
    'agent',
    'Research Agent',
    300,
    200,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '0937b1be-a43c-4a84-9dc6-f11173604c7c',
    'ccdcc9f7-f46c-4ef0-947f-eaada31278a7',
    'agent',
    'Content Writer',
    500,
    200,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "claude-3"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '6e0adcff-5894-42bf-aada-6c5a960f6087',
    'ccdcc9f7-f46c-4ef0-947f-eaada31278a7',
    'api',
    'Content Publisher',
    700,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.wordpress.com/wp/v2/posts"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    'b3777909-9863-47ac-92cf-c9d3375f8d4a',
    'demo-user-95',
    'workspace-team',
    NULL,
    'Real Estate Investment Analyzer',
    'Automated property analysis and investment alerts',
    '{"blocks": {"5d705848-2656-48d6-b084-c0ca0df86ecd": {"id": "5d705848-2656-48d6-b084-c0ca0df86ecd", "type": "starter", "name": "Property Alert", "position": {"x": 100, "y": 200}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "5774f819-0279-495d-a53e-91fe1c798ade": {"id": "5774f819-0279-495d-a53e-91fe1c798ade", "type": "api", "name": "Property Listings", "position": {"x": 300, "y": 200}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.zillow.com/properties"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "a9eb2373-c417-4532-8ea4-6d96acccef8d": {"id": "a9eb2373-c417-4532-8ea4-6d96acccef8d", "type": "agent", "name": "Property Analyzer", "position": {"x": 500, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "41864fc2-b2ff-4399-a457-22664775cded": {"id": "41864fc2-b2ff-4399-a457-22664775cded", "type": "output", "name": "Investment Alert", "position": {"x": 700, "y": 200}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "email"}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "5d705848-2656-48d6-b084-c0ca0df86ecd", "target": "5774f819-0279-495d-a53e-91fe1c798ade", "sourceHandle": "output", "targetHandle": "input"}, {"source": "5774f819-0279-495d-a53e-91fe1c798ade", "target": "a9eb2373-c417-4532-8ea4-6d96acccef8d", "sourceHandle": "output", "targetHandle": "input"}, {"source": "a9eb2373-c417-4532-8ea4-6d96acccef8d", "target": "41864fc2-b2ff-4399-a457-22664775cded", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698687Z", "updatedAt": "2025-08-04T08:04:34.698688Z"}}',
    '#15803D',
    '2025-08-04T08:04:34.698710',
    '2025-08-02T08:04:34.698711',
    '2025-08-03T10:04:34.698713',
    False,
    NULL,
    NULL,
    '["user0@company.com", "user1@company.com"]',
    430,
    NULL,
    '{}',
    False,
    '{"category": "Real Estate", "tags": ["real_estate", "automation", "ai"], "pricing": "premium", "rating": 4.4, "downloads": 3092}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '5d705848-2656-48d6-b084-c0ca0df86ecd',
    'b3777909-9863-47ac-92cf-c9d3375f8d4a',
    'starter',
    'Property Alert',
    100,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '5774f819-0279-495d-a53e-91fe1c798ade',
    'b3777909-9863-47ac-92cf-c9d3375f8d4a',
    'api',
    'Property Listings',
    300,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.zillow.com/properties"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'a9eb2373-c417-4532-8ea4-6d96acccef8d',
    'b3777909-9863-47ac-92cf-c9d3375f8d4a',
    'agent',
    'Property Analyzer',
    500,
    200,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '41864fc2-b2ff-4399-a457-22664775cded',
    'b3777909-9863-47ac-92cf-c9d3375f8d4a',
    'output',
    'Investment Alert',
    700,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"outputType": {"id": "outputType", "type": "dropdown", "value": "email"}}',
    '{"success": "boolean", "message": "string"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    '3112fb43-23c7-4e62-86bb-43a9f94f27d7',
    'demo-user-research',
    'research-team-workspace',
    NULL,
    'Multi-Agent Research Team',
    'Collaborative AI research team with specialized agents for market analysis, technical evaluation, and competitive intelligence',
    '{"blocks": {"fc30df4d-8dd5-46be-86e8-3e6672a62c62": {"id": "fc30df4d-8dd5-46be-86e8-3e6672a62c62", "type": "starter", "name": "Research Request", "position": {"x": 100, "y": 300}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}, "webhookPath": {"id": "webhookPath", "type": "short-input", "value": "research-request"}, "webhookSecret": {"id": "webhookSecret", "type": "short-input", "value": "research-secret-key"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "ec77497c-d157-49ff-b1be-8035d575a98e": {"id": "ec77497c-d157-49ff-b1be-8035d575a98e", "type": "agent", "name": "Research Coordinator", "position": {"x": 300, "y": 300}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a research coordinator managing a team of specialist agents. Break down research queries into focused subtasks and assign them to the appropriate specialists: Market Research Agent (trends, consumer behavior), Technical Analysis Agent (technical specs, implementation), and Competitive Intelligence Agent (competitor analysis, market positioning). Provide clear, specific instructions to each agent."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.5}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "e679d710-a94b-4f3a-9091-2fdf162de85c": {"id": "e679d710-a94b-4f3a-9091-2fdf162de85c", "type": "agent", "name": "Market Research Agent", "position": {"x": 500, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a market research specialist. Focus on market trends, consumer behavior, demand analysis, market size, growth projections, and customer segments. Provide data-driven insights with sources and confidence levels."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.7}, "tools": {"id": "tools", "type": "tool-input", "value": [{"type": "web_search", "title": "Web Search", "enabled": true}, {"type": "market_data", "title": "Market Data APIs", "enabled": true}]}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "6352e918-0179-4dbd-866a-6d43f304f372": {"id": "6352e918-0179-4dbd-866a-6d43f304f372", "type": "agent", "name": "Technical Analysis Agent", "position": {"x": 500, "y": 300}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a technical analysis specialist. Focus on technical specifications, implementation details, architecture analysis, technology stack evaluation, performance metrics, and technical feasibility. Provide detailed technical assessments."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.6}, "tools": {"id": "tools", "type": "tool-input", "value": [{"type": "code_analysis", "title": "Code Analysis", "enabled": true}, {"type": "technical_docs", "title": "Technical Documentation", "enabled": true}]}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "d81fe9a4-dcb6-4636-9c39-d78d61060da6": {"id": "d81fe9a4-dcb6-4636-9c39-d78d61060da6", "type": "agent", "name": "Competitive Intelligence Agent", "position": {"x": 500, "y": 400}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a competitive intelligence specialist. Focus on competitor analysis, market positioning, pricing strategies, feature comparisons, SWOT analysis, and competitive advantages. Identify market gaps and opportunities."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.7}, "tools": {"id": "tools", "type": "tool-input", "value": [{"type": "competitor_analysis", "title": "Competitor Analysis", "enabled": true}, {"type": "pricing_data", "title": "Pricing Intelligence", "enabled": true}]}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "7e50989a-8242-417a-bf0a-dd0dca5423a1": {"id": "7e50989a-8242-417a-bf0a-dd0dca5423a1", "type": "agent", "name": "Research Synthesizer", "position": {"x": 700, "y": 300}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a research synthesis specialist. Combine insights from market research, technical analysis, and competitive intelligence into a comprehensive report. Create executive summary, key findings, strategic recommendations, and actionable next steps. Ensure consistency and identify cross-functional insights."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.4}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "5af0c3f4-3757-4da7-bd8b-e9e8d9ab8a8a": {"id": "5af0c3f4-3757-4da7-bd8b-e9e8d9ab8a8a", "type": "output", "name": "Research Report Delivery", "position": {"x": 900, "y": 300}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "document"}, "channels": {"id": "channels", "type": "multi-select", "value": ["email", "google_docs", "slack"]}, "emailConfig": {"id": "emailConfig", "type": "json", "value": {"to": "research@company.com", "subject": "Research Report: {{RESEARCH_TOPIC}}"}}, "docConfig": {"id": "docConfig", "type": "json", "value": {"format": "pdf", "template": "research_report", "folder": "Research Reports"}}, "slackConfig": {"id": "slackConfig", "type": "json", "value": {"channel": "#research", "message": "New research report available"}}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "fc30df4d-8dd5-46be-86e8-3e6672a62c62", "target": "ec77497c-d157-49ff-b1be-8035d575a98e", "sourceHandle": "output", "targetHandle": "input"}, {"source": "ec77497c-d157-49ff-b1be-8035d575a98e", "target": "e679d710-a94b-4f3a-9091-2fdf162de85c", "sourceHandle": "output", "targetHandle": "input"}, {"source": "ec77497c-d157-49ff-b1be-8035d575a98e", "target": "6352e918-0179-4dbd-866a-6d43f304f372", "sourceHandle": "output", "targetHandle": "input"}, {"source": "ec77497c-d157-49ff-b1be-8035d575a98e", "target": "d81fe9a4-dcb6-4636-9c39-d78d61060da6", "sourceHandle": "output", "targetHandle": "input"}, {"source": "e679d710-a94b-4f3a-9091-2fdf162de85c", "target": "7e50989a-8242-417a-bf0a-dd0dca5423a1", "sourceHandle": "output", "targetHandle": "input"}, {"source": "6352e918-0179-4dbd-866a-6d43f304f372", "target": "7e50989a-8242-417a-bf0a-dd0dca5423a1", "sourceHandle": "output", "targetHandle": "input"}, {"source": "d81fe9a4-dcb6-4636-9c39-d78d61060da6", "target": "7e50989a-8242-417a-bf0a-dd0dca5423a1", "sourceHandle": "output", "targetHandle": "input"}, {"source": "7e50989a-8242-417a-bf0a-dd0dca5423a1", "target": "5af0c3f4-3757-4da7-bd8b-e9e8d9ab8a8a", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {"RESEARCH_TOPIC": {"type": "string", "value": "AI Market Analysis"}, "RESEARCH_DEPTH": {"type": "string", "value": "comprehensive"}, "DEADLINE": {"type": "string", "value": "7 days"}}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698800Z", "updatedAt": "2025-08-04T08:04:34.698801Z"}}',
    '#7C2D12',
    '2025-08-04T08:04:34.698867',
    '2025-08-04T08:04:34.698867',
    '2025-08-04T08:04:34.698868',
    True,
    '{"blocks": {"fc30df4d-8dd5-46be-86e8-3e6672a62c62": {"id": "fc30df4d-8dd5-46be-86e8-3e6672a62c62", "type": "starter", "name": "Research Request", "position": {"x": 100, "y": 300}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}, "webhookPath": {"id": "webhookPath", "type": "short-input", "value": "research-request"}, "webhookSecret": {"id": "webhookSecret", "type": "short-input", "value": "research-secret-key"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "ec77497c-d157-49ff-b1be-8035d575a98e": {"id": "ec77497c-d157-49ff-b1be-8035d575a98e", "type": "agent", "name": "Research Coordinator", "position": {"x": 300, "y": 300}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a research coordinator managing a team of specialist agents. Break down research queries into focused subtasks and assign them to the appropriate specialists: Market Research Agent (trends, consumer behavior), Technical Analysis Agent (technical specs, implementation), and Competitive Intelligence Agent (competitor analysis, market positioning). Provide clear, specific instructions to each agent."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.5}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "e679d710-a94b-4f3a-9091-2fdf162de85c": {"id": "e679d710-a94b-4f3a-9091-2fdf162de85c", "type": "agent", "name": "Market Research Agent", "position": {"x": 500, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a market research specialist. Focus on market trends, consumer behavior, demand analysis, market size, growth projections, and customer segments. Provide data-driven insights with sources and confidence levels."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.7}, "tools": {"id": "tools", "type": "tool-input", "value": [{"type": "web_search", "title": "Web Search", "enabled": true}, {"type": "market_data", "title": "Market Data APIs", "enabled": true}]}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "6352e918-0179-4dbd-866a-6d43f304f372": {"id": "6352e918-0179-4dbd-866a-6d43f304f372", "type": "agent", "name": "Technical Analysis Agent", "position": {"x": 500, "y": 300}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a technical analysis specialist. Focus on technical specifications, implementation details, architecture analysis, technology stack evaluation, performance metrics, and technical feasibility. Provide detailed technical assessments."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.6}, "tools": {"id": "tools", "type": "tool-input", "value": [{"type": "code_analysis", "title": "Code Analysis", "enabled": true}, {"type": "technical_docs", "title": "Technical Documentation", "enabled": true}]}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "d81fe9a4-dcb6-4636-9c39-d78d61060da6": {"id": "d81fe9a4-dcb6-4636-9c39-d78d61060da6", "type": "agent", "name": "Competitive Intelligence Agent", "position": {"x": 500, "y": 400}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a competitive intelligence specialist. Focus on competitor analysis, market positioning, pricing strategies, feature comparisons, SWOT analysis, and competitive advantages. Identify market gaps and opportunities."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.7}, "tools": {"id": "tools", "type": "tool-input", "value": [{"type": "competitor_analysis", "title": "Competitor Analysis", "enabled": true}, {"type": "pricing_data", "title": "Pricing Intelligence", "enabled": true}]}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "7e50989a-8242-417a-bf0a-dd0dca5423a1": {"id": "7e50989a-8242-417a-bf0a-dd0dca5423a1", "type": "agent", "name": "Research Synthesizer", "position": {"x": 700, "y": 300}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a research synthesis specialist. Combine insights from market research, technical analysis, and competitive intelligence into a comprehensive report. Create executive summary, key findings, strategic recommendations, and actionable next steps. Ensure consistency and identify cross-functional insights."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.4}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "5af0c3f4-3757-4da7-bd8b-e9e8d9ab8a8a": {"id": "5af0c3f4-3757-4da7-bd8b-e9e8d9ab8a8a", "type": "output", "name": "Research Report Delivery", "position": {"x": 900, "y": 300}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "document"}, "channels": {"id": "channels", "type": "multi-select", "value": ["email", "google_docs", "slack"]}, "emailConfig": {"id": "emailConfig", "type": "json", "value": {"to": "research@company.com", "subject": "Research Report: {{RESEARCH_TOPIC}}"}}, "docConfig": {"id": "docConfig", "type": "json", "value": {"format": "pdf", "template": "research_report", "folder": "Research Reports"}}, "slackConfig": {"id": "slackConfig", "type": "json", "value": {"channel": "#research", "message": "New research report available"}}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "fc30df4d-8dd5-46be-86e8-3e6672a62c62", "target": "ec77497c-d157-49ff-b1be-8035d575a98e", "sourceHandle": "output", "targetHandle": "input"}, {"source": "ec77497c-d157-49ff-b1be-8035d575a98e", "target": "e679d710-a94b-4f3a-9091-2fdf162de85c", "sourceHandle": "output", "targetHandle": "input"}, {"source": "ec77497c-d157-49ff-b1be-8035d575a98e", "target": "6352e918-0179-4dbd-866a-6d43f304f372", "sourceHandle": "output", "targetHandle": "input"}, {"source": "ec77497c-d157-49ff-b1be-8035d575a98e", "target": "d81fe9a4-dcb6-4636-9c39-d78d61060da6", "sourceHandle": "output", "targetHandle": "input"}, {"source": "e679d710-a94b-4f3a-9091-2fdf162de85c", "target": "7e50989a-8242-417a-bf0a-dd0dca5423a1", "sourceHandle": "output", "targetHandle": "input"}, {"source": "6352e918-0179-4dbd-866a-6d43f304f372", "target": "7e50989a-8242-417a-bf0a-dd0dca5423a1", "sourceHandle": "output", "targetHandle": "input"}, {"source": "d81fe9a4-dcb6-4636-9c39-d78d61060da6", "target": "7e50989a-8242-417a-bf0a-dd0dca5423a1", "sourceHandle": "output", "targetHandle": "input"}, {"source": "7e50989a-8242-417a-bf0a-dd0dca5423a1", "target": "5af0c3f4-3757-4da7-bd8b-e9e8d9ab8a8a", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {"RESEARCH_TOPIC": {"type": "string", "value": "AI Market Analysis"}, "RESEARCH_DEPTH": {"type": "string", "value": "comprehensive"}, "DEADLINE": {"type": "string", "value": "7 days"}}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698800Z", "updatedAt": "2025-08-04T08:04:34.698801Z"}}',
    '2025-08-04T08:04:34.698925',
    '["research-lead@company.com", "analyst@company.com"]',
    121,
    '2025-08-04T06:04:34.698930',
    '{"RESEARCH_TOPIC": "AI Market Analysis"}',
    True,
    '{"category": "Research & Analysis", "tags": ["research", "multi-agent", "analysis", "reports", "intelligence"], "pricing": "premium", "rating": 4.9, "downloads": 1823, "featured": true}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'fc30df4d-8dd5-46be-86e8-3e6672a62c62',
    '3112fb43-23c7-4e62-86bb-43a9f94f27d7',
    'starter',
    'Research Request',
    100,
    300,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}, "webhookPath": {"id": "webhookPath", "type": "short-input", "value": "research-request"}, "webhookSecret": {"id": "webhookSecret", "type": "short-input", "value": "research-secret-key"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'ec77497c-d157-49ff-b1be-8035d575a98e',
    '3112fb43-23c7-4e62-86bb-43a9f94f27d7',
    'agent',
    'Research Coordinator',
    300,
    300,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "claude-3"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a research coordinator managing a team of specialist agents. Break down research queries into focused subtasks and assign them to the appropriate specialists: Market Research Agent (trends, consumer behavior), Technical Analysis Agent (technical specs, implementation), and Competitive Intelligence Agent (competitor analysis, market positioning). Provide clear, specific instructions to each agent."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.5}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'e679d710-a94b-4f3a-9091-2fdf162de85c',
    '3112fb43-23c7-4e62-86bb-43a9f94f27d7',
    'agent',
    'Market Research Agent',
    500,
    200,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-4"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a market research specialist. Focus on market trends, consumer behavior, demand analysis, market size, growth projections, and customer segments. Provide data-driven insights with sources and confidence levels."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.7}, "tools": {"id": "tools", "type": "tool-input", "value": [{"type": "web_search", "title": "Web Search", "enabled": true}, {"type": "market_data", "title": "Market Data APIs", "enabled": true}]}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '6352e918-0179-4dbd-866a-6d43f304f372',
    '3112fb43-23c7-4e62-86bb-43a9f94f27d7',
    'agent',
    'Technical Analysis Agent',
    500,
    300,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-4"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a technical analysis specialist. Focus on technical specifications, implementation details, architecture analysis, technology stack evaluation, performance metrics, and technical feasibility. Provide detailed technical assessments."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.6}, "tools": {"id": "tools", "type": "tool-input", "value": [{"type": "code_analysis", "title": "Code Analysis", "enabled": true}, {"type": "technical_docs", "title": "Technical Documentation", "enabled": true}]}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'd81fe9a4-dcb6-4636-9c39-d78d61060da6',
    '3112fb43-23c7-4e62-86bb-43a9f94f27d7',
    'agent',
    'Competitive Intelligence Agent',
    500,
    400,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "claude-3"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a competitive intelligence specialist. Focus on competitor analysis, market positioning, pricing strategies, feature comparisons, SWOT analysis, and competitive advantages. Identify market gaps and opportunities."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.7}, "tools": {"id": "tools", "type": "tool-input", "value": [{"type": "competitor_analysis", "title": "Competitor Analysis", "enabled": true}, {"type": "pricing_data", "title": "Pricing Intelligence", "enabled": true}]}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '7e50989a-8242-417a-bf0a-dd0dca5423a1',
    '3112fb43-23c7-4e62-86bb-43a9f94f27d7',
    'agent',
    'Research Synthesizer',
    700,
    300,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "claude-3"}, "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are a research synthesis specialist. Combine insights from market research, technical analysis, and competitive intelligence into a comprehensive report. Create executive summary, key findings, strategic recommendations, and actionable next steps. Ensure consistency and identify cross-functional insights."}, "temperature": {"id": "temperature", "type": "slider", "value": 0.4}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '5af0c3f4-3757-4da7-bd8b-e9e8d9ab8a8a',
    '3112fb43-23c7-4e62-86bb-43a9f94f27d7',
    'output',
    'Research Report Delivery',
    900,
    300,
    True,
    True,
    False,
    FALSE,
    95,
    '{"outputType": {"id": "outputType", "type": "dropdown", "value": "document"}, "channels": {"id": "channels", "type": "multi-select", "value": ["email", "google_docs", "slack"]}, "emailConfig": {"id": "emailConfig", "type": "json", "value": {"to": "research@company.com", "subject": "Research Report: {{RESEARCH_TOPIC}}"}}, "docConfig": {"id": "docConfig", "type": "json", "value": {"format": "pdf", "template": "research_report", "folder": "Research Reports"}}, "slackConfig": {"id": "slackConfig", "type": "json", "value": {"channel": "#research", "message": "New research report available"}}}',
    '{"success": "boolean", "message": "string"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    'd9e6ab6e-1019-4102-abd2-0c038ef99553',
    'demo-user-67',
    'workspace-personal',
    NULL,
    'DeFi Yield Optimizer',
    'Multi-protocol DeFi yield farming optimization',
    '{"blocks": {"710aee57-13da-435e-8db5-dfad7ec668cb": {"id": "710aee57-13da-435e-8db5-dfad7ec668cb", "type": "starter", "name": "DeFi Monitor", "position": {"x": 100, "y": 300}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "1e34df38-d4f8-44da-9f54-f7de3d733003": {"id": "1e34df38-d4f8-44da-9f54-f7de3d733003", "type": "api", "name": "Uniswap Data", "position": {"x": 300, "y": 200}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "ef5fdd4c-cf21-489b-b4b2-fae0f520d800": {"id": "ef5fdd4c-cf21-489b-b4b2-fae0f520d800", "type": "api", "name": "Aave Data", "position": {"x": 300, "y": 300}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.aave.com/data/liquidity/v2"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "c5529537-a499-4bff-a803-56f0b883ef10": {"id": "c5529537-a499-4bff-a803-56f0b883ef10", "type": "api", "name": "Compound Data", "position": {"x": 300, "y": 400}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.compound.finance/api/v2/ctoken"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "b4c5ccdd-cdd0-488b-940c-0a804968a192": {"id": "b4c5ccdd-cdd0-488b-940c-0a804968a192", "type": "agent", "name": "DeFi Strategy Agent", "position": {"x": 500, "y": 300}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "54f0e7f3-bb77-4de7-b816-b6b3d55562aa": {"id": "54f0e7f3-bb77-4de7-b816-b6b3d55562aa", "type": "api", "name": "Smart Contract Execution", "position": {"x": 700, "y": 300}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://mainnet.infura.io/v3/YOUR-PROJECT-ID"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "710aee57-13da-435e-8db5-dfad7ec668cb", "target": "1e34df38-d4f8-44da-9f54-f7de3d733003", "sourceHandle": "output", "targetHandle": "input"}, {"source": "710aee57-13da-435e-8db5-dfad7ec668cb", "target": "ef5fdd4c-cf21-489b-b4b2-fae0f520d800", "sourceHandle": "output", "targetHandle": "input"}, {"source": "710aee57-13da-435e-8db5-dfad7ec668cb", "target": "c5529537-a499-4bff-a803-56f0b883ef10", "sourceHandle": "output", "targetHandle": "input"}, {"source": "1e34df38-d4f8-44da-9f54-f7de3d733003", "target": "b4c5ccdd-cdd0-488b-940c-0a804968a192", "sourceHandle": "output", "targetHandle": "input"}, {"source": "ef5fdd4c-cf21-489b-b4b2-fae0f520d800", "target": "b4c5ccdd-cdd0-488b-940c-0a804968a192", "sourceHandle": "output", "targetHandle": "input"}, {"source": "c5529537-a499-4bff-a803-56f0b883ef10", "target": "b4c5ccdd-cdd0-488b-940c-0a804968a192", "sourceHandle": "output", "targetHandle": "input"}, {"source": "b4c5ccdd-cdd0-488b-940c-0a804968a192", "target": "54f0e7f3-bb77-4de7-b816-b6b3d55562aa", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.698990Z", "updatedAt": "2025-08-04T08:04:34.698990Z"}}',
    '#15803D',
    '2025-08-04T08:04:34.699027',
    '2025-07-25T08:04:34.699027',
    '2025-08-03T19:04:34.699029',
    False,
    NULL,
    NULL,
    '["user0@company.com", "user1@company.com"]',
    213,
    NULL,
    '{}',
    True,
    '{"category": "Web3 & DeFi", "tags": ["web3_&_defi", "automation", "ai"], "pricing": "free", "rating": 4.6, "downloads": 4457}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '710aee57-13da-435e-8db5-dfad7ec668cb',
    'd9e6ab6e-1019-4102-abd2-0c038ef99553',
    'starter',
    'DeFi Monitor',
    100,
    300,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '1e34df38-d4f8-44da-9f54-f7de3d733003',
    'd9e6ab6e-1019-4102-abd2-0c038ef99553',
    'api',
    'Uniswap Data',
    300,
    200,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'ef5fdd4c-cf21-489b-b4b2-fae0f520d800',
    'd9e6ab6e-1019-4102-abd2-0c038ef99553',
    'api',
    'Aave Data',
    300,
    300,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.aave.com/data/liquidity/v2"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'c5529537-a499-4bff-a803-56f0b883ef10',
    'd9e6ab6e-1019-4102-abd2-0c038ef99553',
    'api',
    'Compound Data',
    300,
    400,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.compound.finance/api/v2/ctoken"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'b4c5ccdd-cdd0-488b-940c-0a804968a192',
    'd9e6ab6e-1019-4102-abd2-0c038ef99553',
    'agent',
    'DeFi Strategy Agent',
    500,
    300,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '54f0e7f3-bb77-4de7-b816-b6b3d55562aa',
    'd9e6ab6e-1019-4102-abd2-0c038ef99553',
    'api',
    'Smart Contract Execution',
    700,
    300,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://mainnet.infura.io/v3/YOUR-PROJECT-ID"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    'a36b1626-ffb5-4265-a420-bd71f52cfe9c',
    'demo-user-52',
    'workspace-personal',
    NULL,
    'Enterprise Process Automation',
    'Multi-department business process automation',
    '{"blocks": {"b39f6f2f-a1c4-4a74-99c4-83f130ebc52a": {"id": "b39f6f2f-a1c4-4a74-99c4-83f130ebc52a", "type": "starter", "name": "Business Process Trigger", "position": {"x": 100, "y": 300}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "42f2a5b1-ff8d-44b7-8574-2921da24b2ca": {"id": "42f2a5b1-ff8d-44b7-8574-2921da24b2ca", "type": "agent", "name": "HR Agent", "position": {"x": 300, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "07a93e30-4189-4b88-9a2c-4e0961574104": {"id": "07a93e30-4189-4b88-9a2c-4e0961574104", "type": "agent", "name": "Finance Agent", "position": {"x": 300, "y": 300}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "22cc90bb-4df7-45e7-a238-e9325f0e99c0": {"id": "22cc90bb-4df7-45e7-a238-e9325f0e99c0", "type": "agent", "name": "Legal Agent", "position": {"x": 300, "y": 400}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5": {"id": "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5", "type": "agent", "name": "Process Coordinator", "position": {"x": 500, "y": 300}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "90173f4a-42c6-4c28-b094-041b584654d9": {"id": "90173f4a-42c6-4c28-b094-041b584654d9", "type": "api", "name": "ERP Integration", "position": {"x": 700, "y": 250}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.sap.com/enterprise"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "1dfc8fa5-ea81-46ce-85e7-404219d6be06": {"id": "1dfc8fa5-ea81-46ce-85e7-404219d6be06", "type": "output", "name": "Stakeholder Notification", "position": {"x": 700, "y": 350}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "multi"}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "b39f6f2f-a1c4-4a74-99c4-83f130ebc52a", "target": "42f2a5b1-ff8d-44b7-8574-2921da24b2ca", "sourceHandle": "output", "targetHandle": "input"}, {"source": "b39f6f2f-a1c4-4a74-99c4-83f130ebc52a", "target": "07a93e30-4189-4b88-9a2c-4e0961574104", "sourceHandle": "output", "targetHandle": "input"}, {"source": "b39f6f2f-a1c4-4a74-99c4-83f130ebc52a", "target": "22cc90bb-4df7-45e7-a238-e9325f0e99c0", "sourceHandle": "output", "targetHandle": "input"}, {"source": "42f2a5b1-ff8d-44b7-8574-2921da24b2ca", "target": "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5", "sourceHandle": "output", "targetHandle": "input"}, {"source": "07a93e30-4189-4b88-9a2c-4e0961574104", "target": "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5", "sourceHandle": "output", "targetHandle": "input"}, {"source": "22cc90bb-4df7-45e7-a238-e9325f0e99c0", "target": "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5", "sourceHandle": "output", "targetHandle": "input"}, {"source": "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5", "target": "90173f4a-42c6-4c28-b094-041b584654d9", "sourceHandle": "output", "targetHandle": "input"}, {"source": "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5", "target": "1dfc8fa5-ea81-46ce-85e7-404219d6be06", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.699102Z", "updatedAt": "2025-08-04T08:04:34.699102Z"}}',
    '#DC2626',
    '2025-08-04T08:04:34.699141',
    '2025-08-01T08:04:34.699141',
    '2025-08-03T19:04:34.699143',
    True,
    '{"blocks": {"b39f6f2f-a1c4-4a74-99c4-83f130ebc52a": {"id": "b39f6f2f-a1c4-4a74-99c4-83f130ebc52a", "type": "starter", "name": "Business Process Trigger", "position": {"x": 100, "y": 300}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "42f2a5b1-ff8d-44b7-8574-2921da24b2ca": {"id": "42f2a5b1-ff8d-44b7-8574-2921da24b2ca", "type": "agent", "name": "HR Agent", "position": {"x": 300, "y": 200}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "07a93e30-4189-4b88-9a2c-4e0961574104": {"id": "07a93e30-4189-4b88-9a2c-4e0961574104", "type": "agent", "name": "Finance Agent", "position": {"x": 300, "y": 300}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "22cc90bb-4df7-45e7-a238-e9325f0e99c0": {"id": "22cc90bb-4df7-45e7-a238-e9325f0e99c0", "type": "agent", "name": "Legal Agent", "position": {"x": 300, "y": 400}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5": {"id": "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5", "type": "agent", "name": "Process Coordinator", "position": {"x": 500, "y": 300}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "90173f4a-42c6-4c28-b094-041b584654d9": {"id": "90173f4a-42c6-4c28-b094-041b584654d9", "type": "api", "name": "ERP Integration", "position": {"x": 700, "y": 250}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.sap.com/enterprise"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "1dfc8fa5-ea81-46ce-85e7-404219d6be06": {"id": "1dfc8fa5-ea81-46ce-85e7-404219d6be06", "type": "output", "name": "Stakeholder Notification", "position": {"x": 700, "y": 350}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "multi"}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "b39f6f2f-a1c4-4a74-99c4-83f130ebc52a", "target": "42f2a5b1-ff8d-44b7-8574-2921da24b2ca", "sourceHandle": "output", "targetHandle": "input"}, {"source": "b39f6f2f-a1c4-4a74-99c4-83f130ebc52a", "target": "07a93e30-4189-4b88-9a2c-4e0961574104", "sourceHandle": "output", "targetHandle": "input"}, {"source": "b39f6f2f-a1c4-4a74-99c4-83f130ebc52a", "target": "22cc90bb-4df7-45e7-a238-e9325f0e99c0", "sourceHandle": "output", "targetHandle": "input"}, {"source": "42f2a5b1-ff8d-44b7-8574-2921da24b2ca", "target": "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5", "sourceHandle": "output", "targetHandle": "input"}, {"source": "07a93e30-4189-4b88-9a2c-4e0961574104", "target": "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5", "sourceHandle": "output", "targetHandle": "input"}, {"source": "22cc90bb-4df7-45e7-a238-e9325f0e99c0", "target": "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5", "sourceHandle": "output", "targetHandle": "input"}, {"source": "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5", "target": "90173f4a-42c6-4c28-b094-041b584654d9", "sourceHandle": "output", "targetHandle": "input"}, {"source": "eb0d8716-8107-4fcf-8ae3-badc3cd44ca5", "target": "1dfc8fa5-ea81-46ce-85e7-404219d6be06", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.699102Z", "updatedAt": "2025-08-04T08:04:34.699102Z"}}',
    NULL,
    '["user0@company.com", "user1@company.com", "user2@company.com"]',
    261,
    NULL,
    '{}',
    True,
    '{"category": "Enterprise", "tags": ["enterprise", "automation", "ai"], "pricing": "premium", "rating": 4.4, "downloads": 643}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'b39f6f2f-a1c4-4a74-99c4-83f130ebc52a',
    'a36b1626-ffb5-4265-a420-bd71f52cfe9c',
    'starter',
    'Business Process Trigger',
    100,
    300,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '42f2a5b1-ff8d-44b7-8574-2921da24b2ca',
    'a36b1626-ffb5-4265-a420-bd71f52cfe9c',
    'agent',
    'HR Agent',
    300,
    200,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '07a93e30-4189-4b88-9a2c-4e0961574104',
    'a36b1626-ffb5-4265-a420-bd71f52cfe9c',
    'agent',
    'Finance Agent',
    300,
    300,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "claude-3"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '22cc90bb-4df7-45e7-a238-e9325f0e99c0',
    'a36b1626-ffb5-4265-a420-bd71f52cfe9c',
    'agent',
    'Legal Agent',
    300,
    400,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'eb0d8716-8107-4fcf-8ae3-badc3cd44ca5',
    'a36b1626-ffb5-4265-a420-bd71f52cfe9c',
    'agent',
    'Process Coordinator',
    500,
    300,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "claude-3"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '90173f4a-42c6-4c28-b094-041b584654d9',
    'a36b1626-ffb5-4265-a420-bd71f52cfe9c',
    'api',
    'ERP Integration',
    700,
    250,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.sap.com/enterprise"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '1dfc8fa5-ea81-46ce-85e7-404219d6be06',
    'a36b1626-ffb5-4265-a420-bd71f52cfe9c',
    'output',
    'Stakeholder Notification',
    700,
    350,
    True,
    True,
    False,
    FALSE,
    95,
    '{"outputType": {"id": "outputType", "type": "dropdown", "value": "multi"}}',
    '{"success": "boolean", "message": "string"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    '8ba3e25b-e838-4128-8959-663fd03f114d',
    'demo-user-44',
    'workspace-team',
    NULL,
    'Multi-Model AI Team',
    'Collaborative AI team using different models',
    '{"blocks": {"610aa5c7-7747-4ac4-85f8-c7480a0f3a36": {"id": "610aa5c7-7747-4ac4-85f8-c7480a0f3a36", "type": "starter", "name": "AI Team Request", "position": {"x": 100, "y": 400}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "8a0506dc-1f19-450b-8f8f-438cf07e2099": {"id": "8a0506dc-1f19-450b-8f8f-438cf07e2099", "type": "agent", "name": "GPT-4 Analyst", "position": {"x": 300, "y": 300}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "96628c74-1f64-4102-a080-a67be94897f6": {"id": "96628c74-1f64-4102-a080-a67be94897f6", "type": "agent", "name": "Claude Writer", "position": {"x": 300, "y": 400}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "6085c06f-1e12-43c4-939b-aa30b0de8563": {"id": "6085c06f-1e12-43c4-939b-aa30b0de8563", "type": "agent", "name": "Gemini Researcher", "position": {"x": 300, "y": 500}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gemini-pro"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "ebdf60f8-fd4b-4eb6-b17e-53e67def6c27": {"id": "ebdf60f8-fd4b-4eb6-b17e-53e67def6c27", "type": "agent", "name": "AI Coordinator", "position": {"x": 500, "y": 400}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "claude-3"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "7cc62d79-fb04-4925-a1bf-d2039dd700ea": {"id": "7cc62d79-fb04-4925-a1bf-d2039dd700ea", "type": "output", "name": "Team Output", "position": {"x": 700, "y": 400}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "document"}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "610aa5c7-7747-4ac4-85f8-c7480a0f3a36", "target": "8a0506dc-1f19-450b-8f8f-438cf07e2099", "sourceHandle": "output", "targetHandle": "input"}, {"source": "610aa5c7-7747-4ac4-85f8-c7480a0f3a36", "target": "96628c74-1f64-4102-a080-a67be94897f6", "sourceHandle": "output", "targetHandle": "input"}, {"source": "610aa5c7-7747-4ac4-85f8-c7480a0f3a36", "target": "6085c06f-1e12-43c4-939b-aa30b0de8563", "sourceHandle": "output", "targetHandle": "input"}, {"source": "8a0506dc-1f19-450b-8f8f-438cf07e2099", "target": "ebdf60f8-fd4b-4eb6-b17e-53e67def6c27", "sourceHandle": "output", "targetHandle": "input"}, {"source": "96628c74-1f64-4102-a080-a67be94897f6", "target": "ebdf60f8-fd4b-4eb6-b17e-53e67def6c27", "sourceHandle": "output", "targetHandle": "input"}, {"source": "6085c06f-1e12-43c4-939b-aa30b0de8563", "target": "ebdf60f8-fd4b-4eb6-b17e-53e67def6c27", "sourceHandle": "output", "targetHandle": "input"}, {"source": "ebdf60f8-fd4b-4eb6-b17e-53e67def6c27", "target": "7cc62d79-fb04-4925-a1bf-d2039dd700ea", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.699239Z", "updatedAt": "2025-08-04T08:04:34.699240Z"}}',
    '#BE185D',
    '2025-08-04T08:04:34.699271',
    '2025-07-08T08:04:34.699272',
    '2025-08-03T18:04:34.699274',
    True,
    NULL,
    NULL,
    '["user0@company.com", "user1@company.com"]',
    209,
    '2025-08-03T13:28:34.699281',
    '{}',
    False,
    '{"category": "AI & ML", "tags": ["ai_&_ml", "automation", "ai"], "pricing": "usage-based", "rating": 3.7, "downloads": 543}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '610aa5c7-7747-4ac4-85f8-c7480a0f3a36',
    '8ba3e25b-e838-4128-8959-663fd03f114d',
    'starter',
    'AI Team Request',
    100,
    400,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '8a0506dc-1f19-450b-8f8f-438cf07e2099',
    '8ba3e25b-e838-4128-8959-663fd03f114d',
    'agent',
    'GPT-4 Analyst',
    300,
    300,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '96628c74-1f64-4102-a080-a67be94897f6',
    '8ba3e25b-e838-4128-8959-663fd03f114d',
    'agent',
    'Claude Writer',
    300,
    400,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "claude-3"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '6085c06f-1e12-43c4-939b-aa30b0de8563',
    '8ba3e25b-e838-4128-8959-663fd03f114d',
    'agent',
    'Gemini Researcher',
    300,
    500,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gemini-pro"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'ebdf60f8-fd4b-4eb6-b17e-53e67def6c27',
    '8ba3e25b-e838-4128-8959-663fd03f114d',
    'agent',
    'AI Coordinator',
    500,
    400,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "claude-3"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '7cc62d79-fb04-4925-a1bf-d2039dd700ea',
    '8ba3e25b-e838-4128-8959-663fd03f114d',
    'output',
    'Team Output',
    700,
    400,
    True,
    True,
    False,
    FALSE,
    95,
    '{"outputType": {"id": "outputType", "type": "dropdown", "value": "document"}}',
    '{"success": "boolean", "message": "string"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    'fb5a9d57-8eeb-4bf5-96f7-08e045e6f5a7',
    'demo-user-11',
    'workspace-enterprise',
    NULL,
    'E-commerce Price Aggregator',
    'Multi-marketplace price monitoring and comparison',
    '{"blocks": {"6cfc3e96-4347-4973-a6c9-c465719d4eff": {"id": "6cfc3e96-4347-4973-a6c9-c465719d4eff", "type": "starter", "name": "Market Scan", "position": {"x": 100, "y": 400}, "subBlocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}}, "outputs": {"response": {"type": {"input": "any"}}}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "67b3883a-a892-4978-8865-3befe0a6c601": {"id": "67b3883a-a892-4978-8865-3befe0a6c601", "type": "api", "name": "Amazon API", "position": {"x": 300, "y": 300}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://webservices.amazon.com/paapi5/searchitems"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "f3fc307c-9508-4de3-96f4-8119a1a3a4a3": {"id": "f3fc307c-9508-4de3-96f4-8119a1a3a4a3", "type": "api", "name": "eBay API", "position": {"x": 300, "y": 400}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.ebay.com/buy/browse/v1/item_summary/search"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "60122d80-0a32-47bc-9ae3-bc76b8a81564": {"id": "60122d80-0a32-47bc-9ae3-bc76b8a81564", "type": "api", "name": "Shopify API", "position": {"x": 300, "y": 500}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.shopify.com/admin/api/2023-01/products.json"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "c26b115d-20ab-4dca-822f-b2e7eb771218": {"id": "c26b115d-20ab-4dca-822f-b2e7eb771218", "type": "agent", "name": "Price Comparison Agent", "position": {"x": 500, "y": 400}, "subBlocks": {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}, "outputs": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}, "enabled": true, "horizontalHandles": true, "isWide": true, "height": 120}, "654b1b70-29f1-476c-9208-bf018de32d36": {"id": "654b1b70-29f1-476c-9208-bf018de32d36", "type": "api", "name": "Database Update", "position": {"x": 700, "y": 350}, "subBlocks": {"url": {"id": "url", "type": "short-input", "value": "https://api.database.com/products"}}, "outputs": {"data": "any", "status": "number", "headers": "json"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}, "972870e0-10be-45e0-9016-bd1b6b1e6446": {"id": "972870e0-10be-45e0-9016-bd1b6b1e6446", "type": "output", "name": "Price Alert", "position": {"x": 700, "y": 450}, "subBlocks": {"outputType": {"id": "outputType", "type": "dropdown", "value": "email"}}, "outputs": {"success": "boolean", "message": "string"}, "enabled": true, "horizontalHandles": true, "isWide": false, "height": 95}}, "edges": [{"source": "6cfc3e96-4347-4973-a6c9-c465719d4eff", "target": "67b3883a-a892-4978-8865-3befe0a6c601", "sourceHandle": "output", "targetHandle": "input"}, {"source": "6cfc3e96-4347-4973-a6c9-c465719d4eff", "target": "f3fc307c-9508-4de3-96f4-8119a1a3a4a3", "sourceHandle": "output", "targetHandle": "input"}, {"source": "6cfc3e96-4347-4973-a6c9-c465719d4eff", "target": "60122d80-0a32-47bc-9ae3-bc76b8a81564", "sourceHandle": "output", "targetHandle": "input"}, {"source": "67b3883a-a892-4978-8865-3befe0a6c601", "target": "c26b115d-20ab-4dca-822f-b2e7eb771218", "sourceHandle": "output", "targetHandle": "input"}, {"source": "f3fc307c-9508-4de3-96f4-8119a1a3a4a3", "target": "c26b115d-20ab-4dca-822f-b2e7eb771218", "sourceHandle": "output", "targetHandle": "input"}, {"source": "60122d80-0a32-47bc-9ae3-bc76b8a81564", "target": "c26b115d-20ab-4dca-822f-b2e7eb771218", "sourceHandle": "output", "targetHandle": "input"}, {"source": "c26b115d-20ab-4dca-822f-b2e7eb771218", "target": "654b1b70-29f1-476c-9208-bf018de32d36", "sourceHandle": "output", "targetHandle": "input"}, {"source": "c26b115d-20ab-4dca-822f-b2e7eb771218", "target": "972870e0-10be-45e0-9016-bd1b6b1e6446", "sourceHandle": "output", "targetHandle": "input"}], "subflows": {}, "variables": {}, "metadata": {"version": "1.0.0", "createdAt": "2025-08-04T08:04:34.699344Z", "updatedAt": "2025-08-04T08:04:34.699345Z"}}',
    '#DC2626',
    '2025-08-04T08:04:34.699381',
    '2025-07-11T08:04:34.699382',
    '2025-08-04T02:04:34.699384',
    False,
    NULL,
    '2025-08-03T16:04:34.699387',
    '["user0@company.com"]',
    63,
    '2025-08-03T08:41:34.699393',
    '{}',
    False,
    '{"category": "E-commerce", "tags": ["e-commerce", "automation", "ai"], "pricing": "usage-based", "rating": 3.6, "downloads": 1767}'
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '6cfc3e96-4347-4973-a6c9-c465719d4eff',
    'fb5a9d57-8eeb-4bf5-96f7-08e045e6f5a7',
    'starter',
    'Market Scan',
    100,
    400,
    True,
    True,
    False,
    FALSE,
    95,
    '{"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}}',
    '{"response": {"type": {"input": "any"}}}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '67b3883a-a892-4978-8865-3befe0a6c601',
    'fb5a9d57-8eeb-4bf5-96f7-08e045e6f5a7',
    'api',
    'Amazon API',
    300,
    300,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://webservices.amazon.com/paapi5/searchitems"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'f3fc307c-9508-4de3-96f4-8119a1a3a4a3',
    'fb5a9d57-8eeb-4bf5-96f7-08e045e6f5a7',
    'api',
    'eBay API',
    300,
    400,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.ebay.com/buy/browse/v1/item_summary/search"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '60122d80-0a32-47bc-9ae3-bc76b8a81564',
    'fb5a9d57-8eeb-4bf5-96f7-08e045e6f5a7',
    'api',
    'Shopify API',
    300,
    500,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.shopify.com/admin/api/2023-01/products.json"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    'c26b115d-20ab-4dca-822f-b2e7eb771218',
    'fb5a9d57-8eeb-4bf5-96f7-08e045e6f5a7',
    'agent',
    'Price Comparison Agent',
    500,
    400,
    True,
    True,
    True,
    FALSE,
    120,
    '{"model": {"id": "model", "type": "combobox", "value": "gpt-4"}}',
    '{"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '654b1b70-29f1-476c-9208-bf018de32d36',
    'fb5a9d57-8eeb-4bf5-96f7-08e045e6f5a7',
    'api',
    'Database Update',
    700,
    350,
    True,
    True,
    False,
    FALSE,
    95,
    '{"url": {"id": "url", "type": "short-input", "value": "https://api.database.com/products"}}',
    '{"data": "any", "status": "number", "headers": "json"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);

INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '972870e0-10be-45e0-9016-bd1b6b1e6446',
    'fb5a9d57-8eeb-4bf5-96f7-08e045e6f5a7',
    'output',
    'Price Alert',
    700,
    450,
    True,
    True,
    False,
    FALSE,
    95,
    '{"outputType": {"id": "outputType", "type": "dropdown", "value": "email"}}',
    '{"success": "boolean", "message": "string"}',
    '{}',
    NULL,
    NULL,
    NOW(),
    NOW()
);
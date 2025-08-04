-- Sample Data Inserts for Agent Forge State Generator
-- Based on ACTUAL CSV data from solidus_docs/

-- Insert sample workflow_rows data (matching actual CSV structure)
INSERT INTO public.workflow_rows (
    id, user_id, workspace_id, folder_id, name, description, color, variables, is_published, created_at, updated_at
) VALUES 
(
    '79e8076f-0ae0-4b6f-9d14-65364ddae6d2', 
    'sEfcNW1TZedrJ8mDW81UFVtZpZXVd3Mf', 
    'f639bbc2-cbda-49c3-9301-9c632c8e86e2', 
    NULL, 
    'default-agent', 
    'Your first workflow - start building here!', 
    '#3972F6', 
    '{}',
    false,
    '2025-07-22 07:10:51.778',
    '2025-07-22 07:10:51.778'
),
(
    '81e98d1e-459d-4e1d-b9c3-e1e56f8155ab', 
    'H2sjCYSjVkkhay0GpyXM53XmEWwDVgjc', 
    'd8b61a6b-d682-4d70-8f39-1261eb4d880b', 
    NULL, 
    'workflow-test', 
    'Your first workflow - start building here!', 
    '#3972F6', 
    '{}',
    false,
    '2025-07-21 14:25:55.945',
    '2025-07-22 07:38:15.676'
),
(
    'af18372b-03e8-45fd-9be5-3ac559c88f57', 
    'H2sjCYSjVkkhay0GpyXM53XmEWwDVgjc', 
    'd8b61a6b-d682-4d70-8f39-1261eb4d880b', 
    NULL, 
    'arctic-constellation', 
    'New workflow', 
    '#15803D', 
    '{}',
    false,
    '2025-07-21 14:26:24.553',
    '2025-07-21 14:26:24.553'
);

-- Insert sample workflow_blocks_rows data (matching actual CSV structure)
INSERT INTO public.workflow_blocks_rows (
    id, workflow_id, type, name, position_x, position_y, enabled, horizontal_handles, 
    is_wide, advanced_mode, height, sub_blocks, outputs, data, parent_id, extent
) VALUES 
-- Agent Block from workflow-test
(
    '135552e8-592e-4567-bf09-156b0a5e28f0', 
    '81e98d1e-459d-4e1d-b9c3-e1e56f8155ab', 
    'agent', 
    'Agent 1', 
    556.9230769230769, 
    -119.80769230769232, 
    true, 
    true, 
    false, 
    false, 
    0, 
    '{"model":{"id":"model","type":"combobox","value":"gemini-2.5-pro"},"tools":{"id":"tools","type":"tool-input","value":[{"type":"elevenlabs","title":"ElevenLabs","params":{"apiKey":"sk_539725a6d8b99b16a11467e7b1cb7d514233f90a58dc4823","voiceId":"Xb7hH8MSUJpSbSDYk0k2"},"isExpanded":true,"usageControl":"auto"}]},"apiKey":{"id":"apiKey","type":"short-input","value":"AIzaSyByzvH03g09lJrv9t6OLJ9GlQqrNUuqRJY"},"memories":{"id":"memories","type":"short-input","value":null},"userPrompt":{"id":"userPrompt","type":"long-input","value":"<start>"},"temperature":{"id":"temperature","type":"slider","value":null},"systemPrompt":{"id":"systemPrompt","type":"long-input","value":"You are an assistant that transitions what the user says into text to speech using elevenlabs and sends them the URL to the output."},"azureEndpoint":{"id":"azureEndpoint","type":"short-input","value":null},"responseFormat":{"id":"responseFormat","type":"code","value":null},"azureApiVersion":{"id":"azureApiVersion","type":"short-input","value":null}}',
    '{"model":"string","tokens":"any","content":"string","toolCalls":"any"}',
    '{}',
    NULL,
    NULL
),
-- Starter Block from arctic-constellation
(
    '1814dd59-5ded-43ed-9b90-549861b8bbde', 
    'af18372b-03e8-45fd-9be5-3ac559c88f57', 
    'starter', 
    'Start', 
    100, 
    100, 
    true, 
    true, 
    false, 
    false, 
    95, 
    '{"timezone":{"id":"timezone","type":"dropdown","value":"UTC"},"dailyTime":{"id":"dailyTime","type":"short-input","value":""},"weeklyDay":{"id":"weeklyDay","type":"dropdown","value":"MON"},"monthlyDay":{"id":"monthlyDay","type":"short-input","value":""},"monthlyTime":{"id":"monthlyTime","type":"short-input","value":""},"webhookPath":{"id":"webhookPath","type":"short-input","value":""},"hourlyMinute":{"id":"hourlyMinute","type":"short-input","value":""},"scheduleType":{"id":"scheduleType","type":"dropdown","value":"daily"},"startWorkflow":{"id":"startWorkflow","type":"dropdown","value":"manual"},"webhookSecret":{"id":"webhookSecret","type":"short-input","value":""},"weeklyDayTime":{"id":"weeklyDayTime","type":"short-input","value":""},"cronExpression":{"id":"cronExpression","type":"short-input","value":""},"minutesInterval":{"id":"minutesInterval","type":"short-input","value":""},"minutesStartingAt":{"id":"minutesStartingAt","type":"short-input","value":""}}',
    '{"response":{"type":{"input":"any"}}}',
    '{}',
    NULL,
    NULL
),
-- API Block from workflow-test
(
    'a091ef02-b50b-425f-b5cf-f3a936281c32', 
    '81e98d1e-459d-4e1d-b9c3-e1e56f8155ab', 
    'api', 
    'API 1', 
    959.7926327015055, 
    129.0738138570569, 
    true, 
    true, 
    false, 
    false, 
    0, 
    '{"url":{"id":"url","type":"short-input","value":"https://api.coingecko.com/api/v3/search/trending"},"body":{"id":"body","type":"code","value":null},"method":{"id":"method","type":"dropdown","value":null},"params":{"id":"params","type":"table","value":null},"headers":{"id":"headers","type":"table","value":[{"id":"58f892db-c69b-49d0-a803-33e9ed4c25e1","cells":{"Key":"Accept","Value":"application/json"}},{"id":"ba713868-ae3e-474b-b881-32fc893d173c","cells":{"Key":"","Value":""}}]}}',
    '{"data":"any","status":"number","headers":"json"}',
    '{}',
    NULL,
    NULL
),
-- Starter Block from default-agent
(
    'cb7ebf84-9d43-45bf-a327-cca64d30d602', 
    '79e8076f-0ae0-4b6f-9d14-65364ddae6d2', 
    'starter', 
    'Start', 
    100, 
    100, 
    true, 
    true, 
    false, 
    false, 
    95, 
    '{"webhookPath":{"id":"webhookPath","type":"short-input","value":""},"scheduleType":{"id":"scheduleType","type":"dropdown","value":"daily"},"startWorkflow":{"id":"startWorkflow","type":"dropdown","value":"manual"},"webhookSecret":{"id":"webhookSecret","type":"short-input","value":""},"minutesInterval":{"id":"minutesInterval","type":"short-input","value":""},"minutesStartingAt":{"id":"minutesStartingAt","type":"short-input","value":""}}',
    '{"response":{"type":{"input":"any"}}}',
    '{}',
    NULL,
    NULL
),
-- Starter Block from workflow-test (main)
(
    'f668ee62-8abb-49df-9b4e-b7d5e18f11df', 
    '81e98d1e-459d-4e1d-b9c3-e1e56f8155ab', 
    'starter', 
    'Start', 
    100, 
    100, 
    true, 
    true, 
    false, 
    false, 
    95, 
    '{"webhookPath":{"id":"webhookPath","type":"short-input","value":"732a975e-4a63-4c5c-bee4-d8061444ae24"},"scheduleType":{"id":"scheduleType","type":"dropdown","value":"daily"},"startWorkflow":{"id":"startWorkflow","type":"dropdown","value":"manual"},"webhookSecret":{"id":"webhookSecret","type":"short-input","value":""},"providerConfig":{"id":"providerConfig","type":"unknown","value":{}},"minutesInterval":{"id":"minutesInterval","type":"short-input","value":""},"webhookProvider":{"id":"webhookProvider","type":"unknown","value":"generic"},"minutesStartingAt":{"id":"minutesStartingAt","type":"short-input","value":""}}',
    '{"response":{"type":{"input":"any"}}}',
    '{}',
    NULL,
    NULL
); 
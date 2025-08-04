#!/usr/bin/env python3
"""
Database Setup and Connection Test Script
Validates Supabase configuration and creates test data
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_environment_variables() -> Dict[str, Any]:
    """Check and validate environment variables"""
    required_vars = {
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_SERVICE_KEY': os.getenv('SUPABASE_SERVICE_KEY'),
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY')
    }
    
    status = {
        'all_configured': True,
        'variables': {},
        'missing': [],
        'issues': []
    }
    
    for var_name, value in required_vars.items():
        if not value:
            status['variables'][var_name] = 'NOT_SET'
            status['missing'].append(var_name)
            status['all_configured'] = False
        elif not value.strip():
            status['variables'][var_name] = 'EMPTY'
            status['issues'].append(f"{var_name} is empty")
            status['all_configured'] = False
        else:
            # Mask sensitive values for display
            if len(value) > 20:
                masked = value[:10] + "..." + value[-10:]
            else:
                masked = value[:5] + "..."
            status['variables'][var_name] = f"SET ({len(value)} chars, {masked})"
    
    return status

async def test_supabase_connection() -> Dict[str, Any]:
    """Test Supabase connection and basic operations"""
    result = {
        'connection_test': 'FAILED',
        'library_import': 'FAILED',
        'client_creation': 'FAILED',
        'basic_query': 'FAILED',
        'table_access': 'FAILED',
        'error_details': []
    }
    
    try:
        # Test library import
        try:
            import supabase
            result['library_import'] = 'SUCCESS'
            print(f"✅ Supabase library imported (version: {supabase.__version__})")
        except ImportError as e:
            result['error_details'].append(f"Library import failed: {e}")
            print(f"❌ Supabase library import failed: {e}")
            return result
        
        # Get environment variables
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not supabase_url or not supabase_key:
            result['error_details'].append("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY")
            print("❌ Missing required environment variables")
            return result
        
        # Test client creation
        try:
            from supabase import create_client
            client = create_client(supabase_url, supabase_key)
            result['client_creation'] = 'SUCCESS'
            print("✅ Supabase client created successfully")
        except Exception as e:
            result['error_details'].append(f"Client creation failed: {e}")
            print(f"❌ Supabase client creation failed: {e}")
            return result
        
        # Test basic connection
        try:
            # Try a simple query to test connection
            response = client.table('workflow').select('id').limit(1).execute()
            result['basic_query'] = 'SUCCESS'
            result['connection_test'] = 'SUCCESS'
            print("✅ Database connection successful")
            
            # Check if we can access workflow table
            workflow_count = len(response.data) if response.data else 0
            result['table_access'] = 'SUCCESS'
            result['workflow_count'] = workflow_count
            print(f"✅ Workflow table accessible (found {workflow_count} workflows)")
            
        except Exception as e:
            result['error_details'].append(f"Database query failed: {e}")
            print(f"❌ Database query failed: {e}")
            
            # Check if it's a tenant/user error
            if "tenant" in str(e).lower() or "user not found" in str(e).lower():
                result['error_details'].append("TENANT_ERROR: Check Supabase project URL and service key")
                print("💡 Hint: This looks like a tenant/user error. Check your Supabase project URL and service key.")
            
    except Exception as e:
        result['error_details'].append(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")
    
    return result

async def create_test_workflow() -> Dict[str, Any]:
    """Create a test workflow for validation"""
    result = {
        'workflow_created': False,
        'blocks_created': False,
        'workflow_id': None,
        'error_details': []
    }
    
    try:
        from supabase import create_client
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not supabase_url or not supabase_key:
            result['error_details'].append("Missing environment variables")
            return result
        
        client = create_client(supabase_url, supabase_key)
        
        # Create test workflow
        test_workflow_id = f"test-workflow-{int(datetime.now().timestamp())}"
        workflow_data = {
            'id': test_workflow_id,
            'user_id': 'test-user',
            'name': 'Test Workflow for Connection Validation',
            'description': 'This is a test workflow created to validate database connectivity',
            'state': {
                'blocks': {},
                'edges': [],
                'variables': {},
                'metadata': {
                    'created_by': 'database_setup_script',
                    'created_at': datetime.now().isoformat()
                }
            },
            'last_synced': datetime.now().isoformat(),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Insert workflow
        workflow_response = client.table('workflow').insert(workflow_data).execute()
        
        if workflow_response.data:
            result['workflow_created'] = True
            result['workflow_id'] = test_workflow_id
            print(f"✅ Test workflow created: {test_workflow_id}")
            
            # Create test blocks
            test_blocks = [
                {
                    'id': f'{test_workflow_id}-block-1',
                    'workflow_id': test_workflow_id,
                    'type': 'starter',
                    'name': 'Test Starter Block',
                    'position_x': 100,
                    'position_y': 100,
                    'sub_blocks': {'startWorkflow': 'manual'}
                },
                {
                    'id': f'{test_workflow_id}-block-2',
                    'workflow_id': test_workflow_id,
                    'type': 'agent',
                    'name': 'Test Agent Block',
                    'position_x': 300,
                    'position_y': 100,
                    'sub_blocks': {'model': 'gpt-4', 'systemPrompt': 'Test agent'}
                }
            ]
            
            blocks_response = client.table('workflow_blocks').insert(test_blocks).execute()
            
            if blocks_response.data:
                result['blocks_created'] = True
                print(f"✅ Test blocks created: {len(test_blocks)} blocks")
            else:
                result['error_details'].append("Failed to create test blocks")
                print("❌ Failed to create test blocks")
        else:
            result['error_details'].append("Failed to create test workflow")
            print("❌ Failed to create test workflow")
            
    except Exception as e:
        result['error_details'].append(f"Test workflow creation failed: {e}")
        print(f"❌ Test workflow creation failed: {e}")
    
    return result

def print_configuration_guide():
    """Print configuration guide for users"""
    print("\n" + "="*60)
    print("🔧 CONFIGURATION GUIDE")
    print("="*60)
    print("""
To fix database connection issues:

1. Set up Supabase Project:
   - Go to https://supabase.com/
   - Create a new project or access existing one
   - Go to Settings > API
   - Copy your Project URL and Service Role Key

2. Set Environment Variables:
   export SUPABASE_URL="https://your-project-id.supabase.co"
   export SUPABASE_SERVICE_KEY="your-service-role-key"
   export ANTHROPIC_API_KEY="your-anthropic-key"  # Optional
   export OPENAI_API_KEY="your-openai-key"        # Optional

3. For Vercel Deployment:
   - Add these variables in Vercel Dashboard
   - Go to Project Settings > Environment Variables
   - Add each variable with production scope

4. Run Database Schema:
   - Execute scripts/create_supabase_schema.sql in your Supabase SQL editor
   - This creates required tables and functions

5. Test Connection:
   python3 scripts/create_test_db_setup.py
""")

async def main():
    """Main setup and test function"""
    print("🚀 Agent Forge Database Setup & Connection Test")
    print("="*60)
    
    # Check environment variables
    print("\n📋 Checking Environment Variables...")
    env_status = check_environment_variables()
    
    for var_name, status in env_status['variables'].items():
        icon = "✅" if "SET" in status else "❌"
        print(f"{icon} {var_name}: {status}")
    
    if not env_status['all_configured']:
        print(f"\n❌ Missing variables: {', '.join(env_status['missing'])}")
        if env_status['issues']:
            for issue in env_status['issues']:
                print(f"⚠️  {issue}")
        print_configuration_guide()
        return
    
    # Test Supabase connection
    print("\n🔗 Testing Supabase Connection...")
    connection_result = await test_supabase_connection()
    
    # Print results
    print(f"\n📊 Connection Test Results:")
    print(f"Library Import: {connection_result['library_import']}")
    print(f"Client Creation: {connection_result['client_creation']}")
    print(f"Basic Query: {connection_result['basic_query']}")
    print(f"Table Access: {connection_result['table_access']}")
    
    if connection_result['connection_test'] == 'SUCCESS':
        print("\n✅ Database connection successful!")
        
        # Try to create test data
        print("\n📝 Creating Test Data...")
        test_result = await create_test_workflow()
        
        if test_result['workflow_created']:
            print(f"✅ Test workflow created: {test_result['workflow_id']}")
            if test_result['blocks_created']:
                print("✅ Test blocks created successfully")
            print("\n🎉 Database setup completed successfully!")
        else:
            print("⚠️  Test data creation failed, but connection works")
            for error in test_result['error_details']:
                print(f"   - {error}")
    else:
        print("\n❌ Database connection failed!")
        for error in connection_result['error_details']:
            print(f"   - {error}")
        print_configuration_guide()

if __name__ == "__main__":
    asyncio.run(main()) 
# CSV One-Time Migration Guide

## Overview

The Agent Forge State Generator includes a **ONE-TIME MIGRATION SYSTEM** that reads workflow data from CSV input tables and migrates them into proper Supabase output tables **WITH DUPLICATE PREVENTION**.

## 🔄 **Migration Architecture**

```
CSV INPUT (One-Time)          →    Migration Engine    →    Supabase OUTPUT (Permanent)
├── workflow_rows             →    CSV Processor       →    public.workflow
└── workflow_blocks_rows      →    Duplicate Prevention →    public.workflow_blocks
```

## ⚡ **Key Features**

✅ **One-Time Process**: CSV data is processed once, then stored permanently
✅ **Duplicate Prevention**: Intelligent skip logic prevents re-processing existing data  
✅ **Force Reprocess**: Option to rerun migration for testing/updates
✅ **Status Tracking**: Complete visibility into migration progress
✅ **Error Handling**: Robust error recovery and logging

## 🚀 **Quick Start**

### 1. Run One-Time Migration
```bash
# First time - processes all CSV data
POST /api/csv/process

# Response:
{
  "message": "CSV migration completed",
  "status": "success", 
  "processed_count": 3,
  "skipped_count": 0,
  "migration_type": "one_time_csv_to_supabase"
}
```

### 2. Check Migration Status
```bash
# Check if migration completed
GET /api/csv/status

# Response:
{
  "migration_status": {
    "completed": true,
    "input_data": {"csv_workflow_rows": 3, "csv_workflow_blocks_rows": 5},
    "output_data": {"supabase_workflows": 3, "supabase_workflow_blocks": 5},
    "migration_ratio": "3/3"
  }
}
```

### 3. View Migrated Data
```bash
# List all migrated workflows
GET /api/workflows

# Get specific workflow state
GET /api/workflows/{workflow_id}/state
```

## 🛡️ **Duplicate Prevention**

### **How It Works**
1. **Pre-Check**: Loads existing workflow/block IDs from output tables
2. **Skip Logic**: Automatically skips workflows that already exist
3. **Block-Level**: Prevents duplicate blocks even within partial workflows
4. **Logging**: Clear messages about what was skipped and why

### **Example Duplicate Prevention**
```bash
# First run - processes everything
POST /api/csv/process
→ "processed_count": 3, "skipped_count": 0

# Second run - skips duplicates  
POST /api/csv/process
→ "processed_count": 0, "skipped_count": 3
→ "status": "already_processed"
→ "message": "CSV migration already completed"
```

### **Force Reprocess**
```bash
# Override duplicate prevention for testing
POST /api/csv/process?force_reprocess=true
→ Will reprocess even existing workflows
```

## 📊 **Migration Status Tracking**

### **Migration States**
- ✅ **Not Started**: No workflows in output tables
- 🔄 **In Progress**: Some workflows migrated, some pending
- ✅ **Completed**: All CSV workflows successfully migrated
- ⚠️ **Partial**: Some workflows failed, some succeeded

### **Status API Response**
```json
{
  "migration_status": {
    "completed": true,
    "input_data": {
      "csv_workflow_rows": 3,
      "csv_workflow_blocks_rows": 5
    },
    "output_data": {
      "supabase_workflows": 3,
      "supabase_workflow_blocks": 5  
    },
    "migration_ratio": "3/3",
    "database_type": "supabase"
  },
  "instructions": {
    "first_time": "POST /api/csv/process",
    "check_status": "GET /api/csv/status",
    "force_rerun": "POST /api/csv/process?force_reprocess=true",
    "view_results": "GET /api/workflows"
  },
  "data_flow": "CSV Input → API Processing → Supabase Output"
}
```

## 🔧 **API Endpoints**

### **Migration Endpoints**

#### `POST /api/csv/process`
**One-time migration with duplicate prevention**
```bash
# Parameters:
# - force_reprocess (optional): boolean, default false

# First time migration
curl -X POST https://solidus-olive.vercel.app/api/csv/process

# Force reprocess for testing
curl -X POST "https://solidus-olive.vercel.app/api/csv/process?force_reprocess=true"
```

#### `GET /api/csv/status`
**Check migration status and progress**
```bash
curl https://solidus-olive.vercel.app/api/csv/status
```

#### `POST /api/csv/reset` (ADMIN)
**Reset migration for testing**
```bash
# WARNING: Clears output tables
curl -X POST https://solidus-olive.vercel.app/api/csv/reset
```

### **Data Access Endpoints**

#### `GET /api/workflows`
**List migrated workflows**
```bash
# All workflows
curl https://solidus-olive.vercel.app/api/workflows

# Filter by user
curl "https://solidus-olive.vercel.app/api/workflows?user_id=H2sjCYSjVkkhay0GpyXM53XmEWwDVgjc"
```

#### `GET /api/workflows/{id}/state`
**Get specific workflow state**
```bash
curl https://solidus-olive.vercel.app/api/workflows/79e8076f-0ae0-4b6f-9d14-65364ddae6d2/state
```

## 📋 **Migration Process Details**

### **Step 1: Input Validation**
- Checks if CSV input tables contain data
- Validates data structure and required fields
- Logs input data counts

### **Step 2: Duplicate Detection**
- Loads existing workflow IDs from output tables
- Loads existing block IDs from output tables
- Creates skip lists for duplicate prevention

### **Step 3: Data Processing**
- Processes each workflow from CSV input
- Skips duplicates (unless force_reprocess=true)
- Generates Agent Forge state JSON
- Validates block relationships

### **Step 4: Output Storage**
- Stores workflows in `public.workflow` table
- Stores blocks in `public.workflow_blocks` table
- Maintains referential integrity
- Uses INSERT for strict duplicate prevention

### **Step 5: Migration Summary**
- Reports processed vs skipped counts
- Provides detailed success/failure breakdown
- Logs completion status and metadata

## 🎯 **Use Cases**

### **Initial Setup**
```bash
# 1. Create Supabase tables
# Run scripts/create_supabase_schema.sql

# 2. Load CSV sample data  
# Run scripts/sample_data_inserts.sql

# 3. Run one-time migration
POST /api/csv/process

# 4. Verify results
GET /api/workflows
```

### **Development/Testing**
```bash
# Reset for clean testing
POST /api/csv/reset

# Rerun migration
POST /api/csv/process

# Test force reprocess
POST /api/csv/process?force_reprocess=true
```

### **Production Deployment**
```bash
# Check if migration needed
GET /api/csv/status

# Run migration if not completed
POST /api/csv/process

# Verify all data migrated
GET /api/workflows
```

## ⚠️ **Important Notes**

### **CSV Data is Input Only**
- CSV tables (`workflow_rows`, `workflow_blocks_rows`) are **INPUT SOURCES**
- Supabase tables (`workflow`, `workflow_blocks`) are **OUTPUT DESTINATIONS**
- After migration, applications should use OUTPUT tables only

### **One-Time Process**
- Migration is designed to run **ONCE** per dataset
- Subsequent runs automatically skip existing data
- Use `force_reprocess=true` only for testing/updates

### **Duplicate Prevention**
- Prevents accidental data duplication
- Maintains data integrity across runs
- Provides clear logging of skip decisions

### **Production Safety**
- Uses INSERT (not UPSERT) by default for strict duplicate prevention
- Comprehensive error handling and rollback
- Detailed logging for audit trails

## 🔍 **Troubleshooting**

### **No Data Processed**
```json
{
  "message": "CSV migration already completed",
  "status": "already_processed"
}
```
**Solution**: Data already migrated. Use `GET /api/workflows` to view results.

### **Partial Migration**
```json
{
  "processed_count": 2,
  "skipped_count": 1,
  "total_input_workflows": 3
}
```
**Solution**: Check logs for specific failures. Some workflows processed successfully.

### **Migration Failed**
```json
{
  "status": "error",
  "error": "Database connection failed"
}
```
**Solution**: Check database credentials and connectivity.

## 🏆 **Technical Interview Ready**

This one-time migration system demonstrates:

✅ **Data Engineering**: CSV → Database migration with proper schema mapping
✅ **Duplicate Prevention**: Intelligent skip logic and data integrity
✅ **Error Handling**: Robust failure recovery and detailed logging  
✅ **API Design**: RESTful endpoints with clear status reporting
✅ **Production Safety**: Safe migration practices with rollback options

**Perfect for demonstrating real-world data migration scenarios!** 
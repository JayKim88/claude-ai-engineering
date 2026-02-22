# Database Schema: {{PROJECT_NAME}}

**Version:** {{SCHEMA_VERSION}}
**Date:** {{DATE}}
**Database Lead:** {{DB_LEAD}}
**Database Type:** {{DB_TYPE}}

---

## Entity-Relationship Overview

```
{{ER_DIAGRAM}}
```

**Core Entities:**
- {{ENTITY_1}}
- {{ENTITY_2}}
- {{ENTITY_3}}
- {{ENTITY_4}}
- {{ENTITY_5}}

**Relationships:**
{{RELATIONSHIPS_SUMMARY}}

---

## Tables/Collections

### Table: {{TABLE_1_NAME}}

**Purpose:** {{TABLE_1_PURPOSE}}

**Schema:**

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | {{TABLE_1_ID_TYPE}} | PRIMARY KEY, AUTO_INCREMENT | - | {{TABLE_1_ID_DESC}} |
| {{TABLE_1_FIELD_1}} | {{TABLE_1_FIELD_1_TYPE}} | {{TABLE_1_FIELD_1_CONSTRAINTS}} | {{TABLE_1_FIELD_1_DEFAULT}} | {{TABLE_1_FIELD_1_DESC}} |
| {{TABLE_1_FIELD_2}} | {{TABLE_1_FIELD_2_TYPE}} | {{TABLE_1_FIELD_2_CONSTRAINTS}} | {{TABLE_1_FIELD_2_DEFAULT}} | {{TABLE_1_FIELD_2_DESC}} |
| {{TABLE_1_FIELD_3}} | {{TABLE_1_FIELD_3_TYPE}} | {{TABLE_1_FIELD_3_CONSTRAINTS}} | {{TABLE_1_FIELD_3_DEFAULT}} | {{TABLE_1_FIELD_3_DESC}} |
| {{TABLE_1_FIELD_4}} | {{TABLE_1_FIELD_4_TYPE}} | {{TABLE_1_FIELD_4_CONSTRAINTS}} | {{TABLE_1_FIELD_4_DEFAULT}} | {{TABLE_1_FIELD_4_DESC}} |
| {{TABLE_1_FIELD_5}} | {{TABLE_1_FIELD_5_TYPE}} | {{TABLE_1_FIELD_5_CONSTRAINTS}} | {{TABLE_1_FIELD_5_DEFAULT}} | {{TABLE_1_FIELD_5_DESC}} |
| created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | {{CREATED_AT_DESC}} |
| updated_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | {{UPDATED_AT_DESC}} |

**Indexes:**
- PRIMARY KEY: `id`
- INDEX: {{TABLE_1_INDEX_1}}
- INDEX: {{TABLE_1_INDEX_2}}
- UNIQUE INDEX: {{TABLE_1_UNIQUE_INDEX}}

**Foreign Keys:**
- {{TABLE_1_FK_1}}: References {{TABLE_1_FK_1_TABLE}}({{TABLE_1_FK_1_FIELD}}) ON DELETE {{TABLE_1_FK_1_ACTION}}
- {{TABLE_1_FK_2}}: References {{TABLE_1_FK_2_TABLE}}({{TABLE_1_FK_2_FIELD}}) ON DELETE {{TABLE_1_FK_2_ACTION}}

**Triggers:**
{{TABLE_1_TRIGGERS}}

**Sample Data:**
```sql
{{TABLE_1_SAMPLE_INSERT}}
```

---

### Table: {{TABLE_2_NAME}}

**Purpose:** {{TABLE_2_PURPOSE}}

**Schema:**

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | {{TABLE_2_ID_TYPE}} | PRIMARY KEY, AUTO_INCREMENT | - | {{TABLE_2_ID_DESC}} |
| {{TABLE_2_FIELD_1}} | {{TABLE_2_FIELD_1_TYPE}} | {{TABLE_2_FIELD_1_CONSTRAINTS}} | {{TABLE_2_FIELD_1_DEFAULT}} | {{TABLE_2_FIELD_1_DESC}} |
| {{TABLE_2_FIELD_2}} | {{TABLE_2_FIELD_2_TYPE}} | {{TABLE_2_FIELD_2_CONSTRAINTS}} | {{TABLE_2_FIELD_2_DEFAULT}} | {{TABLE_2_FIELD_2_DESC}} |
| {{TABLE_2_FIELD_3}} | {{TABLE_2_FIELD_3_TYPE}} | {{TABLE_2_FIELD_3_CONSTRAINTS}} | {{TABLE_2_FIELD_3_DEFAULT}} | {{TABLE_2_FIELD_3_DESC}} |
| {{TABLE_2_FIELD_4}} | {{TABLE_2_FIELD_4_TYPE}} | {{TABLE_2_FIELD_4_CONSTRAINTS}} | {{TABLE_2_FIELD_4_DEFAULT}} | {{TABLE_2_FIELD_4_DESC}} |
| {{TABLE_2_FIELD_5}} | {{TABLE_2_FIELD_5_TYPE}} | {{TABLE_2_FIELD_5_CONSTRAINTS}} | {{TABLE_2_FIELD_5_DEFAULT}} | {{TABLE_2_FIELD_5_DESC}} |
| {{TABLE_2_FIELD_6}} | {{TABLE_2_FIELD_6_TYPE}} | {{TABLE_2_FIELD_6_CONSTRAINTS}} | {{TABLE_2_FIELD_6_DEFAULT}} | {{TABLE_2_FIELD_6_DESC}} |
| created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | {{CREATED_AT_DESC}} |
| updated_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | {{UPDATED_AT_DESC}} |

**Indexes:**
- PRIMARY KEY: `id`
- INDEX: {{TABLE_2_INDEX_1}}
- INDEX: {{TABLE_2_INDEX_2}}
- COMPOSITE INDEX: {{TABLE_2_COMPOSITE_INDEX}}

**Foreign Keys:**
- {{TABLE_2_FK_1}}: References {{TABLE_2_FK_1_TABLE}}({{TABLE_2_FK_1_FIELD}}) ON DELETE {{TABLE_2_FK_1_ACTION}}

---

### Table: {{TABLE_3_NAME}}

**Purpose:** {{TABLE_3_PURPOSE}}

**Schema:**

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | {{TABLE_3_ID_TYPE}} | PRIMARY KEY, AUTO_INCREMENT | - | {{TABLE_3_ID_DESC}} |
| {{TABLE_3_FIELD_1}} | {{TABLE_3_FIELD_1_TYPE}} | {{TABLE_3_FIELD_1_CONSTRAINTS}} | {{TABLE_3_FIELD_1_DEFAULT}} | {{TABLE_3_FIELD_1_DESC}} |
| {{TABLE_3_FIELD_2}} | {{TABLE_3_FIELD_2_TYPE}} | {{TABLE_3_FIELD_2_CONSTRAINTS}} | {{TABLE_3_FIELD_2_DEFAULT}} | {{TABLE_3_FIELD_2_DESC}} |
| {{TABLE_3_FIELD_3}} | {{TABLE_3_FIELD_3_TYPE}} | {{TABLE_3_FIELD_3_CONSTRAINTS}} | {{TABLE_3_FIELD_3_DEFAULT}} | {{TABLE_3_FIELD_3_DESC}} |
| {{TABLE_3_FIELD_4}} | {{TABLE_3_FIELD_4_TYPE}} | {{TABLE_3_FIELD_4_CONSTRAINTS}} | {{TABLE_3_FIELD_4_DEFAULT}} | {{TABLE_3_FIELD_4_DESC}} |
| created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | {{CREATED_AT_DESC}} |
| updated_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | {{UPDATED_AT_DESC}} |

**Indexes:**
- PRIMARY KEY: `id`
- INDEX: {{TABLE_3_INDEX_1}}
- UNIQUE INDEX: {{TABLE_3_UNIQUE_INDEX}}

**Foreign Keys:**
- {{TABLE_3_FK_1}}: References {{TABLE_3_FK_1_TABLE}}({{TABLE_3_FK_1_FIELD}}) ON DELETE {{TABLE_3_FK_1_ACTION}}
- {{TABLE_3_FK_2}}: References {{TABLE_3_FK_2_TABLE}}({{TABLE_3_FK_2_FIELD}}) ON DELETE {{TABLE_3_FK_2_ACTION}}

---

### Table: {{TABLE_4_NAME}} (Junction/Join Table)

**Purpose:** {{TABLE_4_PURPOSE}}

**Schema:**

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| {{TABLE_4_FK_1}} | {{TABLE_4_FK_1_TYPE}} | NOT NULL | - | {{TABLE_4_FK_1_DESC}} |
| {{TABLE_4_FK_2}} | {{TABLE_4_FK_2_TYPE}} | NOT NULL | - | {{TABLE_4_FK_2_DESC}} |
| {{TABLE_4_FIELD_1}} | {{TABLE_4_FIELD_1_TYPE}} | {{TABLE_4_FIELD_1_CONSTRAINTS}} | {{TABLE_4_FIELD_1_DEFAULT}} | {{TABLE_4_FIELD_1_DESC}} |
| created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | {{CREATED_AT_DESC}} |

**Indexes:**
- PRIMARY KEY: ({{TABLE_4_FK_1}}, {{TABLE_4_FK_2}})
- INDEX: {{TABLE_4_INDEX_1}}

**Foreign Keys:**
- {{TABLE_4_FK_1}}: References {{TABLE_4_FK_1_REF_TABLE}}(id) ON DELETE CASCADE
- {{TABLE_4_FK_2}}: References {{TABLE_4_FK_2_REF_TABLE}}(id) ON DELETE CASCADE

---

### Table: {{TABLE_5_NAME}}

**Purpose:** {{TABLE_5_PURPOSE}}

**Schema:**

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | {{TABLE_5_ID_TYPE}} | PRIMARY KEY, AUTO_INCREMENT | - | {{TABLE_5_ID_DESC}} |
| {{TABLE_5_FIELD_1}} | {{TABLE_5_FIELD_1_TYPE}} | {{TABLE_5_FIELD_1_CONSTRAINTS}} | {{TABLE_5_FIELD_1_DEFAULT}} | {{TABLE_5_FIELD_1_DESC}} |
| {{TABLE_5_FIELD_2}} | {{TABLE_5_FIELD_2_TYPE}} | {{TABLE_5_FIELD_2_CONSTRAINTS}} | {{TABLE_5_FIELD_2_DEFAULT}} | {{TABLE_5_FIELD_2_DESC}} |
| {{TABLE_5_FIELD_3}} | {{TABLE_5_FIELD_3_TYPE}} | {{TABLE_5_FIELD_3_CONSTRAINTS}} | {{TABLE_5_FIELD_3_DEFAULT}} | {{TABLE_5_FIELD_3_DESC}} |
| {{TABLE_5_FIELD_4}} | {{TABLE_5_FIELD_4_TYPE}} | {{TABLE_5_FIELD_4_CONSTRAINTS}} | {{TABLE_5_FIELD_4_DEFAULT}} | {{TABLE_5_FIELD_4_DESC}} |
| {{TABLE_5_FIELD_5}} | {{TABLE_5_FIELD_5_TYPE}} | {{TABLE_5_FIELD_5_CONSTRAINTS}} | {{TABLE_5_FIELD_5_DEFAULT}} | {{TABLE_5_FIELD_5_DESC}} |
| created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | {{CREATED_AT_DESC}} |
| updated_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | {{UPDATED_AT_DESC}} |

**Indexes:**
- PRIMARY KEY: `id`
- INDEX: {{TABLE_5_INDEX_1}}
- INDEX: {{TABLE_5_INDEX_2}}

---

## Indexes Strategy

### Performance Indexes

| Table | Index Name | Columns | Type | Purpose |
|-------|------------|---------|------|---------|
| {{INDEX_TABLE_1}} | {{INDEX_NAME_1}} | {{INDEX_COLS_1}} | {{INDEX_TYPE_1}} | {{INDEX_PURPOSE_1}} |
| {{INDEX_TABLE_2}} | {{INDEX_NAME_2}} | {{INDEX_COLS_2}} | {{INDEX_TYPE_2}} | {{INDEX_PURPOSE_2}} |
| {{INDEX_TABLE_3}} | {{INDEX_NAME_3}} | {{INDEX_COLS_3}} | {{INDEX_TYPE_3}} | {{INDEX_PURPOSE_3}} |
| {{INDEX_TABLE_4}} | {{INDEX_NAME_4}} | {{INDEX_COLS_4}} | {{INDEX_TYPE_4}} | {{INDEX_PURPOSE_4}} |
| {{INDEX_TABLE_5}} | {{INDEX_NAME_5}} | {{INDEX_COLS_5}} | {{INDEX_TYPE_5}} | {{INDEX_PURPOSE_5}} |

### Full-Text Indexes

| Table | Columns | Purpose |
|-------|---------|---------|
| {{FT_TABLE_1}} | {{FT_COLS_1}} | {{FT_PURPOSE_1}} |
| {{FT_TABLE_2}} | {{FT_COLS_2}} | {{FT_PURPOSE_2}} |

---

## Relationships

### One-to-Many Relationships

| Parent Table | Child Table | Foreign Key | On Delete | Description |
|--------------|-------------|-------------|-----------|-------------|
| {{OTM_PARENT_1}} | {{OTM_CHILD_1}} | {{OTM_FK_1}} | {{OTM_DELETE_1}} | {{OTM_DESC_1}} |
| {{OTM_PARENT_2}} | {{OTM_CHILD_2}} | {{OTM_FK_2}} | {{OTM_DELETE_2}} | {{OTM_DESC_2}} |
| {{OTM_PARENT_3}} | {{OTM_CHILD_3}} | {{OTM_FK_3}} | {{OTM_DELETE_3}} | {{OTM_DESC_3}} |

### Many-to-Many Relationships

| Table 1 | Table 2 | Junction Table | Description |
|---------|---------|----------------|-------------|
| {{MTM_TABLE_1_1}} | {{MTM_TABLE_1_2}} | {{MTM_JUNCTION_1}} | {{MTM_DESC_1}} |
| {{MTM_TABLE_2_1}} | {{MTM_TABLE_2_2}} | {{MTM_JUNCTION_2}} | {{MTM_DESC_2}} |
| {{MTM_TABLE_3_1}} | {{MTM_TABLE_3_2}} | {{MTM_JUNCTION_3}} | {{MTM_DESC_3}} |

### One-to-One Relationships

| Table 1 | Table 2 | Foreign Key | Description |
|---------|---------|-------------|-------------|
| {{OTO_TABLE_1_1}} | {{OTO_TABLE_1_2}} | {{OTO_FK_1}} | {{OTO_DESC_1}} |
| {{OTO_TABLE_2_1}} | {{OTO_TABLE_2_2}} | {{OTO_FK_2}} | {{OTO_DESC_2}} |

---

## Data Types Reference

### Common Types

| Type | SQL Equivalent | Description | Example |
|------|----------------|-------------|---------|
| {{DTYPE_1}} | {{DTYPE_1_SQL}} | {{DTYPE_1_DESC}} | {{DTYPE_1_EXAMPLE}} |
| {{DTYPE_2}} | {{DTYPE_2_SQL}} | {{DTYPE_2_DESC}} | {{DTYPE_2_EXAMPLE}} |
| {{DTYPE_3}} | {{DTYPE_3_SQL}} | {{DTYPE_3_DESC}} | {{DTYPE_3_EXAMPLE}} |
| {{DTYPE_4}} | {{DTYPE_4_SQL}} | {{DTYPE_4_DESC}} | {{DTYPE_4_EXAMPLE}} |
| {{DTYPE_5}} | {{DTYPE_5_SQL}} | {{DTYPE_5_DESC}} | {{DTYPE_5_EXAMPLE}} |

---

## Migration Strategy

### Initial Migration

**Tool:** {{MIGRATION_TOOL}}
**Location:** {{MIGRATION_LOCATION}}

**Migration Workflow:**
1. {{MIGRATION_STEP_1}}
2. {{MIGRATION_STEP_2}}
3. {{MIGRATION_STEP_3}}
4. {{MIGRATION_STEP_4}}

### Migration Naming Convention

{{MIGRATION_NAMING}}

**Example:**
{{MIGRATION_EXAMPLE}}

### Rollback Strategy

{{ROLLBACK_STRATEGY}}

### Schema Versioning

**Current Version:** {{CURRENT_SCHEMA_VERSION}}
**Version History:** {{VERSION_HISTORY_TABLE}}

---

## Seed Data

### Required Seed Data

**Purpose:** {{SEED_PURPOSE}}

**Tables to Seed:**
- {{SEED_TABLE_1}}: {{SEED_TABLE_1_DESC}}
- {{SEED_TABLE_2}}: {{SEED_TABLE_2_DESC}}
- {{SEED_TABLE_3}}: {{SEED_TABLE_3_DESC}}

**Seed Script Location:** {{SEED_SCRIPT_LOCATION}}

### Sample Seed SQL

```sql
{{SEED_SQL_EXAMPLE}}
```

---

## Query Optimization

### Common Queries

#### Query 1: {{QUERY_1_NAME}}

**Purpose:** {{QUERY_1_PURPOSE}}

**Frequency:** {{QUERY_1_FREQUENCY}}

**SQL:**
```sql
{{QUERY_1_SQL}}
```

**Optimization:** {{QUERY_1_OPTIMIZATION}}

**Indexes Used:** {{QUERY_1_INDEXES}}

---

#### Query 2: {{QUERY_2_NAME}}

**Purpose:** {{QUERY_2_PURPOSE}}

**Frequency:** {{QUERY_2_FREQUENCY}}

**SQL:**
```sql
{{QUERY_2_SQL}}
```

**Optimization:** {{QUERY_2_OPTIMIZATION}}

**Indexes Used:** {{QUERY_2_INDEXES}}

---

#### Query 3: {{QUERY_3_NAME}}

**Purpose:** {{QUERY_3_PURPOSE}}

**Frequency:** {{QUERY_3_FREQUENCY}}

**SQL:**
```sql
{{QUERY_3_SQL}}
```

**Optimization:** {{QUERY_3_OPTIMIZATION}}

**Indexes Used:** {{QUERY_3_INDEXES}}

---

## Data Integrity

### Constraints

**Referential Integrity:**
{{REFERENTIAL_INTEGRITY}}

**Check Constraints:**
- {{CHECK_CONSTRAINT_1}}
- {{CHECK_CONSTRAINT_2}}
- {{CHECK_CONSTRAINT_3}}

**Unique Constraints:**
- {{UNIQUE_CONSTRAINT_1}}
- {{UNIQUE_CONSTRAINT_2}}
- {{UNIQUE_CONSTRAINT_3}}

### Triggers

| Trigger Name | Table | Event | Purpose |
|--------------|-------|-------|---------|
| {{TRIGGER_1}} | {{TRIGGER_1_TABLE}} | {{TRIGGER_1_EVENT}} | {{TRIGGER_1_PURPOSE}} |
| {{TRIGGER_2}} | {{TRIGGER_2_TABLE}} | {{TRIGGER_2_EVENT}} | {{TRIGGER_2_PURPOSE}} |
| {{TRIGGER_3}} | {{TRIGGER_3_TABLE}} | {{TRIGGER_3_EVENT}} | {{TRIGGER_3_PURPOSE}} |

---

## Backup & Recovery

**Backup Frequency:** {{BACKUP_FREQUENCY}}
**Backup Retention:** {{BACKUP_RETENTION}}
**Backup Location:** {{BACKUP_LOCATION}}

**Recovery Point Objective (RPO):** {{RPO}}
**Recovery Time Objective (RTO):** {{RTO}}

**Backup Strategy:**
{{BACKUP_STRATEGY}}

**Restore Procedure:**
{{RESTORE_PROCEDURE}}

---

## Security

### Access Control

**Users/Roles:**
- {{DB_USER_1}}: {{DB_USER_1_PERMISSIONS}}
- {{DB_USER_2}}: {{DB_USER_2_PERMISSIONS}}
- {{DB_USER_3}}: {{DB_USER_3_PERMISSIONS}}

### Encryption

**At Rest:** {{ENCRYPTION_AT_REST}}
**In Transit:** {{ENCRYPTION_IN_TRANSIT}}

### Sensitive Data

**PII Fields:**
- {{PII_FIELD_1}} in {{PII_TABLE_1}}
- {{PII_FIELD_2}} in {{PII_TABLE_2}}
- {{PII_FIELD_3}} in {{PII_TABLE_3}}

**Encryption Strategy:** {{PII_ENCRYPTION}}

**Masking Rules:**
{{DATA_MASKING}}

---

## Partitioning Strategy

**Partitioning Type:** {{PARTITION_TYPE}}

**Partitioned Tables:**

| Table | Partition Key | Strategy | Reason |
|-------|---------------|----------|--------|
| {{PART_TABLE_1}} | {{PART_KEY_1}} | {{PART_STRATEGY_1}} | {{PART_REASON_1}} |
| {{PART_TABLE_2}} | {{PART_KEY_2}} | {{PART_STRATEGY_2}} | {{PART_REASON_2}} |

---

## Archival Strategy

**Archive Trigger:** {{ARCHIVE_TRIGGER}}
**Archive Location:** {{ARCHIVE_LOCATION}}
**Archive Format:** {{ARCHIVE_FORMAT}}

**Tables to Archive:**
- {{ARCHIVE_TABLE_1}}: {{ARCHIVE_TABLE_1_CRITERIA}}
- {{ARCHIVE_TABLE_2}}: {{ARCHIVE_TABLE_2_CRITERIA}}

---

## Monitoring

**Metrics to Track:**
- {{DB_METRIC_1}}
- {{DB_METRIC_2}}
- {{DB_METRIC_3}}
- {{DB_METRIC_4}}

**Slow Query Threshold:** {{SLOW_QUERY_THRESHOLD}}

**Alert Conditions:**
- {{DB_ALERT_1}}
- {{DB_ALERT_2}}
- {{DB_ALERT_3}}

---

## Schema Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| {{SCHEMA_V1}} | {{SCHEMA_D1}} | {{SCHEMA_A1}} | {{SCHEMA_C1}} |
| {{SCHEMA_V2}} | {{SCHEMA_D2}} | {{SCHEMA_A2}} | {{SCHEMA_C2}} |
| {{SCHEMA_V3}} | {{SCHEMA_D3}} | {{SCHEMA_A3}} | {{SCHEMA_C3}} |

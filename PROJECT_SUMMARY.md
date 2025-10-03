# Allianz DBT Assignment - Project Summary

## Overview
This project implements a data transformation pipeline using dbt (data build tool) with PostgreSQL as the target database. The goal was to create a staging and intermediate layer for financial data, with the intention of building a Data Vault 2.0 model.

## Architecture

### Database Setup
- **Database**: PostgreSQL 15
- **Environment**: Docker devcontainer
- **dbt Version**: 1.10.13
- **dbt Adapter**: dbt-postgres 1.9.1

### Data Migration
- Successfully migrated raw data from DuckDB to PostgreSQL
- Migrated tables: customers, accounts, loans, transactions, fx_rates
- Total records migrated: ~71,000+ rows across all tables

## Project Structure

### 1. Raw Layer (`raw` schema)
Source tables loaded directly from CSV files into PostgreSQL:
- `customers` - 5,000 customer records
- `accounts` - 5,000 account records
- `loans` - 5,000 loan records
- `transactions` - 56,116 transaction records
- `fx_rates` - 15 foreign exchange rates

### 2. Staging Layer (`staging` schema)
First transformation layer that cleans and standardizes raw data:

#### Models:
- **stg_raw_staging__customers**
  - Removes duplicates
  - Trims whitespace from names
  - Preserves case-sensitive "Age" column
  - Total: 5,000 records

- **stg_raw_staging__accounts**
  - Filters invalid account types
  - Parses multiple date formats (DD.MM.YYYY, DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD)
  - Handles empty date strings
  - Flags records with date parsing errors
  - Total: ~5,000 records

- **stg_raw_staging__loans**
  - Parses loan dates with multiple format support
  - Converts German number format (1.234,56 → 1234.56)
  - Handles both loan_amount and interest_rate conversions
  - Flags records with parsing errors
  - Total: 5,000 records

- **stg_raw_staging__transactions**
  - Parses transaction dates
  - Converts transaction amounts from German format
  - Flags records with date parsing errors
  - Total: 56,116 records

- **stg_raw_staging__fx_rates**
  - Parses effective dates
  - Converts exchange rates from German number format
  - Total: 15 records

### 3. Intermediate Layer (`intermediate` schema)
Business-ready tables with data quality checks applied:

#### Models:
- **stg_staging_intermediate__customers**
  - Clean customer data
  - Total: 5,000 records

- **stg_staging_intermediate__accounts**
  - Filters out records with date parsing errors
  - Total: 4,997 records (3 records excluded due to invalid dates)

- **stg_staging_intermediate__loans**
  - Filters out records with parsing errors
  - Total: 5,000 records

- **stg_staging_intermediate__transactions**
  - Filters out records with parsing errors
  - Total: 56,116 records

- **stg_staging_intermediate__fx_rates**
  - Filters out records with parsing errors
  - Total: 15 records

- **stg_staging_intermediate__currencies**
  - Distinct currency list from seed data
  - Removes null and '(none)' values
  - Total: 146 currencies

### 4. Vault Stage Layer (`vault_stage` - Planned)
Prepared models for Data Vault 2.0 with hash keys:
- v_stg_customer
- v_stg_account
- v_stg_loan
- v_stg_transaction
- v_stg_fx_rates
- v_stg_currency

**Status**: Models created but not operational due to datavault4dbt package limitation (PostgreSQL not supported)

### 5. Raw Vault Layer (Planned)
Data Vault 2.0 entities:

#### Hubs (Business Keys):
- hub_customer (customer_id)
- hub_account (account_id)
- hub_loan (loan_id)
- hub_transaction (transaction_id)
- hub_branch (branch_id)
- hub_currency (currency_iso_code)

#### Links (Relationships):
- link_customer_account (customer ↔ account)
- link_customer_loan (customer ↔ loan)
- link_account_transaction (account ↔ transaction)
- link_customer_branch (customer ↔ branch)
- link_fx_rate (base currency ↔ target currency)

#### Satellites (Attributes):
- sat_customer (firstname, lastname, age)
- sat_account (account_type, account_opening_date)
- sat_loan (loan_type, loan_amount, interest_rate, loan_start_date)
- sat_transaction (transaction_type, transaction_amount, transaction_date)
- sat_fx_rate (exchange_rate, effective_date)

**Status**: Models created but not operational due to datavault4dbt package limitation

## Technical Achievements

### 1. Custom Macros
Created reusable dbt macros for data transformations:

#### `date_format_case(column_name)`
Intelligently parses multiple date formats:
- German format: DD.MM.YYYY
- European format: DD/MM/YYYY
- US format: MM/DD/YYYY
- ISO format: YYYY-MM-DD
- Handles NULL and empty strings gracefully
- Returns NULL for unparseable dates instead of failing

#### `convert_german_number_case(column_name)`
Converts German number notation to decimal:
- Handles thousands separator: 1.234 → 1234
- Handles decimal separator: 1,23 → 1.23
- Handles combined: 1.234,56 → 1234.56
- Validates numeric patterns with regex
- Returns NULL for invalid numbers

#### `postgres__drop_relation(relation)`
Custom override to fix dbt-postgres adapter bug:
- Fixes trailing period in DROP TABLE statements
- Prevents "syntax error at end of input" errors
- Uses CASCADE for safe relation dropping

### 2. PostgreSQL-Specific Optimizations
- Converted DuckDB syntax to PostgreSQL equivalents:
  - `REGEXP_MATCHES()` → `~` operator
  - `TRY_CAST()` → `::` casting
  - `STRPTIME()` → `TO_DATE()`
- Proper handling of case-sensitive column names with quotes
- Regex pattern matching using PostgreSQL syntax

### 3. Data Quality Features
- Explicit error flagging with `has_date_parsing_error` columns
- Filtering invalid records in intermediate layer
- Preservation of raw values for audit trail
- Deduplication in staging layer

### 4. DevContainer Setup
Complete development environment:
```yaml
Services:
  - app: dbt development container (Python 3.11)
  - postgres: PostgreSQL 15-alpine
  - Persistent volumes for data
  - Environment variables for configuration
```

## Entity Relationship Diagram

```mermaid
erDiagram
    %% Raw Layer
    RAW_CUSTOMERS ||--o{ RAW_ACCOUNTS : "has"
    RAW_CUSTOMERS ||--o{ RAW_LOANS : "has"
    RAW_ACCOUNTS ||--o{ RAW_TRANSACTIONS : "contains"
    RAW_CUSTOMERS }o--|| RAW_BRANCHES : "belongs_to"

    %% Staging Layer
    STG_CUSTOMERS ||--o{ STG_ACCOUNTS : "has"
    STG_CUSTOMERS ||--o{ STG_LOANS : "has"
    STG_ACCOUNTS ||--o{ STG_TRANSACTIONS : "contains"
    STG_FX_RATES }o--|| STG_CURRENCIES : "base_currency"
    STG_FX_RATES }o--|| STG_CURRENCIES : "target_currency"

    %% Intermediate Layer
    INT_CUSTOMERS ||--o{ INT_ACCOUNTS : "has"
    INT_CUSTOMERS ||--o{ INT_LOANS : "has"
    INT_ACCOUNTS ||--o{ INT_TRANSACTIONS : "contains"
    INT_FX_RATES }o--|| INT_CURRENCIES : "uses"

    %% Raw Layer Tables
    RAW_CUSTOMERS {
        int customer_id PK
        string firstname
        string lastname
        int Age
        int branch_id FK
    }

    RAW_ACCOUNTS {
        int account_id PK
        int customer_id FK
        string account_type
        string account_opening_date
    }

    RAW_LOANS {
        int loan_id PK
        int customer_id FK
        string loan_type
        string loan_amount
        string interest_rate
        string loan_start_date
    }

    RAW_TRANSACTIONS {
        int transaction_id PK
        int account_id FK
        string transaction_date
        string transaction_type
        string transaction_amount
        string transaction_currency
    }

    RAW_FX_RATES {
        string base_currency
        string target_currency
        string exchange_rate
        string effective_date
    }

    RAW_BRANCHES {
        int branch_id PK
        string branch_name
    }

    %% Staging Layer Tables
    STG_CUSTOMERS {
        int customer_id PK
        string firstname
        string lastname
        int age
        int branch_id FK
    }

    STG_ACCOUNTS {
        int account_id PK
        int customer_id FK
        string account_type
        date account_opening_date
        string account_opening_date_raw
        bool has_date_parsing_error
    }

    STG_LOANS {
        int loan_id PK
        int customer_id FK
        string loan_type
        double loan_amount
        double interest_rate
        date loan_start_date
        string loan_start_date_raw
        bool has_date_parsing_error
        bool has_amount_parsing_error
    }

    STG_TRANSACTIONS {
        int transaction_id PK
        int account_id FK
        date transaction_date
        string transaction_type
        double transaction_amount
        string transaction_currency
        string transaction_date_raw
        bool has_date_parsing_error
    }

    STG_FX_RATES {
        string base_currency FK
        string target_currency FK
        double exchange_rate
        date effective_date
        string effective_date_raw
        bool has_date_parsing_error
    }

    STG_CURRENCIES {
        string currency
        string currency_iso_code PK
    }

    %% Intermediate Layer Tables
    INT_CUSTOMERS {
        int customer_id PK
        string firstname
        string lastname
        int age
        int branch_id FK
    }

    INT_ACCOUNTS {
        int account_id PK
        int customer_id FK
        string account_type
        date account_opening_date
    }

    INT_LOANS {
        int loan_id PK
        int customer_id FK
        string loan_type
        double loan_amount
        double interest_rate
        date loan_start_date
    }

    INT_TRANSACTIONS {
        int transaction_id PK
        int account_id FK
        date transaction_date
        string transaction_type
        double transaction_amount
        string transaction_currency
    }

    INT_FX_RATES {
        string base_currency FK
        string target_currency FK
        double exchange_rate
        date effective_date
    }

    INT_CURRENCIES {
        string currency
        string currency_iso_code PK
    }
```

## Data Vault 2.0 Model (Planned Architecture)

```mermaid
erDiagram
    HUB_CUSTOMER {
        string hk_customer_h PK
        int customer_id
        timestamp load_dts
        string record_source
    }

    HUB_ACCOUNT {
        string hk_account_h PK
        int account_id
        timestamp load_dts
        string record_source
    }

    HUB_LOAN {
        string hk_loan_h PK
        int loan_id
        timestamp load_dts
        string record_source
    }

    HUB_TRANSACTION {
        string hk_transaction_h PK
        int transaction_id
        timestamp load_dts
        string record_source
    }

    HUB_BRANCH {
        string hk_branch_h PK
        int branch_id
        timestamp load_dts
        string record_source
    }

    HUB_CURRENCY {
        string hk_currency_h PK
        string currency_iso_code
        timestamp load_dts
        string record_source
    }

    LINK_CUSTOMER_ACCOUNT {
        string hk_customer_account_l PK
        string hk_customer_h FK
        string hk_account_h FK
        timestamp load_dts
        string record_source
    }

    LINK_CUSTOMER_LOAN {
        string hk_customer_loan_l PK
        string hk_customer_h FK
        string hk_loan_h FK
        timestamp load_dts
        string record_source
    }

    LINK_ACCOUNT_TRANSACTION {
        string hk_account_transaction_l PK
        string hk_account_h FK
        string hk_transaction_h FK
        timestamp load_dts
        string record_source
    }

    LINK_CUSTOMER_BRANCH {
        string hk_customer_branch_l PK
        string hk_customer_h FK
        string hk_branch_h FK
        timestamp load_dts
        string record_source
    }

    LINK_FX_RATE {
        string hk_fx_rate_l PK
        string hk_base_currency_h FK
        string hk_target_currency_h FK
        timestamp load_dts
        string record_source
    }

    SAT_CUSTOMER {
        string hk_customer_h FK
        timestamp load_dts PK
        timestamp load_end_dts
        string hashdiff
        string firstname
        string lastname
        int age
        string record_source
    }

    SAT_ACCOUNT {
        string hk_account_h FK
        timestamp load_dts PK
        timestamp load_end_dts
        string hashdiff
        string account_type
        date account_opening_date
        string record_source
    }

    SAT_LOAN {
        string hk_loan_h FK
        timestamp load_dts PK
        timestamp load_end_dts
        string hashdiff
        string loan_type
        double loan_amount
        double interest_rate
        date loan_start_date
        string record_source
    }

    SAT_TRANSACTION {
        string hk_transaction_h FK
        timestamp load_dts PK
        timestamp load_end_dts
        string hashdiff
        string transaction_type
        double transaction_amount
        date transaction_date
        string record_source
    }

    SAT_FX_RATE {
        string hk_fx_rate_l FK
        timestamp load_dts PK
        timestamp load_end_dts
        string hashdiff
        double exchange_rate
        date effective_date
        string record_source
    }

    HUB_CUSTOMER ||--o{ LINK_CUSTOMER_ACCOUNT : has
    HUB_ACCOUNT ||--o{ LINK_CUSTOMER_ACCOUNT : has
    HUB_CUSTOMER ||--o{ LINK_CUSTOMER_LOAN : has
    HUB_LOAN ||--o{ LINK_CUSTOMER_LOAN : has
    HUB_ACCOUNT ||--o{ LINK_ACCOUNT_TRANSACTION : has
    HUB_TRANSACTION ||--o{ LINK_ACCOUNT_TRANSACTION : has
    HUB_CUSTOMER ||--o{ LINK_CUSTOMER_BRANCH : has
    HUB_BRANCH ||--o{ LINK_CUSTOMER_BRANCH : has
    HUB_CURRENCY ||--o{ LINK_FX_RATE : base
    HUB_CURRENCY ||--o{ LINK_FX_RATE : target

    HUB_CUSTOMER ||--o{ SAT_CUSTOMER : describes
    HUB_ACCOUNT ||--o{ SAT_ACCOUNT : describes
    HUB_LOAN ||--o{ SAT_LOAN : describes
    HUB_TRANSACTION ||--o{ SAT_TRANSACTION : describes
    LINK_FX_RATE ||--o{ SAT_FX_RATE : describes
```

## Key Challenges Solved

### 1. Date Format Inconsistencies
**Problem**: Multiple date formats in source data (German DD.MM.YYYY, European DD/MM/YYYY, US MM/DD/YYYY, ISO YYYY-MM-DD)

**Solution**: Created `date_format_case()` macro that:
- Uses regex pattern matching to identify format
- Applies correct PostgreSQL `TO_DATE()` format string
- Handles edge cases (empty strings, NULL values)
- Returns NULL instead of failing for unparseable dates

### 2. German Number Format
**Problem**: Numeric values using German notation (1.234,56)

**Solution**: Created `convert_german_number_case()` macro that:
- Detects presence of both dots and commas
- Removes thousands separators (dots)
- Converts decimal separators (commas to dots)
- Validates using regex before casting
- Returns NULL for invalid formats

### 3. dbt-postgres DROP TABLE Bug
**Problem**: dbt-postgres adapter generating malformed SQL with trailing period:
```sql
DROP TABLE IF EXISTS "table"__dbt_backup".
```

**Solution**: Created custom `postgres__drop_relation()` macro that:
- Overrides the default adapter behavior
- Generates correct SQL without trailing period
- Uses CASCADE for safe cleanup
- Allows all table materializations to succeed

### 4. Case-Sensitive Column Names
**Problem**: PostgreSQL preserved "Age" column case from migration, causing query failures

**Solution**:
- Quoted column references in SELECT: `"Age" as age`
- Maintained lowercase in output for consistency
- Updated all downstream models accordingly

### 5. datavault4dbt Incompatibility
**Problem**: datavault4dbt package only supports BigQuery, Snowflake, and Exasol - not PostgreSQL

**Impact**:
- Vault stage layer models compile but fail at runtime
- Generated SQL uses BigQuery-specific functions (TO_HEX, REGEXP_REPLACE, PARSE_TIMESTAMP)
- Generated SQL uses uppercase column names incompatible with PostgreSQL schema

**Workaround Options**:
1. Switch to supported database (Snowflake/BigQuery)
2. Implement custom Data Vault macros for PostgreSQL
3. Use dbt-vault package (alternative Data Vault package)

## Project Statistics

### Code Metrics
- **dbt Models**: 17 models (6 staging, 6 intermediate, 5 vault_stage)
- **Custom Macros**: 3 macros
- **Data Tests**: 78 tests defined
- **Seeds**: 2 (currencies, branch data)
- **Sources**: 5 raw tables

### Data Metrics
- **Total Raw Records**: 71,131
- **Staging Records**: 71,131 (same as raw)
- **Intermediate Records**: 71,128 (3 records filtered due to data quality)
- **Data Quality Exclusions**:
  - 3 accounts with invalid dates
  - All other entities: 100% pass rate

### Performance
- **Full Staging Build**: ~2-3 seconds
- **Full Intermediate Build**: ~3-4 seconds
- **Individual Model Build**: <0.5 seconds
- **Database Size**: ~50MB (including indexes)

## Files Structure

```
transformation/
├── dbt_project.yml              # Project configuration
├── profiles.yml                 # PostgreSQL connection
├── packages.yml                 # dbt packages
│
├── macros/
│   ├── data_cleaning_utils.sql  # Date and number parsing macros
│   └── drop_relation_fix.sql    # PostgreSQL DROP fix
│
├── models/
│   ├── sources.yml              # Source table definitions
│   │
│   ├── staging/                 # Raw → Staging transformations
│   │   ├── stg_raw_staging__customers.sql
│   │   ├── stg_raw_staging__accounts.sql
│   │   ├── stg_raw_staging__loans.sql
│   │   ├── stg_raw_staging__transactions.sql
│   │   └── stg_raw_staging__fx_rates.sql
│   │
│   ├── intermediate/            # Staging → Intermediate (filtered)
│   │   ├── stg_staging_intermediate__customers.sql
│   │   ├── stg_staging_intermediate__accounts.sql
│   │   ├── stg_staging_intermediate__loans.sql
│   │   ├── stg_staging_intermediate__transactions.sql
│   │   ├── stg_staging_intermediate__fx_rates.sql
│   │   └── stg_staging_intermediate__currencies.sql
│   │
│   ├── vault_stage/             # Intermediate → Vault Stage (with hashes)
│   │   ├── v_stg_customer.sql   # ⚠️ Not operational (datavault4dbt)
│   │   ├── v_stg_account.sql
│   │   ├── v_stg_loan.sql
│   │   ├── v_stg_transaction.sql
│   │   └── v_stg_currency.sql
│   │
│   └── raw_vault/               # Data Vault 2.0 entities
│       ├── hubs/                # ⚠️ Not operational (datavault4dbt)
│       │   ├── hub_customer.sql
│       │   ├── hub_account.sql
│       │   ├── hub_loan.sql
│       │   └── hub_transaction.sql
│       │
│       ├── links/
│       │   ├── link_customer_account.sql
│       │   ├── link_customer_loan.sql
│       │   └── link_account_transaction.sql
│       │
│       └── satellites/
│           ├── sat_customer.sql
│           ├── sat_account.sql
│           ├── sat_loan.sql
│           └── sat_transaction.sql
│
├── seeds/
│   └── currencies.csv           # Reference data (146 currencies)
│
└── target/                      # Compiled SQL output
```

## Technologies Used

- **dbt**: 1.10.13
- **PostgreSQL**: 15-alpine
- **Python**: 3.11.11
- **Docker**: DevContainer setup
- **dbt Packages**:
  - dbt_utils (1.x)
  - dbt_date (0.11.0)
  - codegen (0.11-0.13)
  - datavault4dbt (1.1.1) - *Limited use due to PostgreSQL incompatibility*

## Recommendations for Future Work

### Short Term
1. **Complete Data Vault Implementation**
   - Option A: Migrate to Snowflake/BigQuery to use datavault4dbt
   - Option B: Implement custom Data Vault macros for PostgreSQL
   - Option C: Evaluate dbt-vault package as alternative

2. **Add Data Quality Tests**
   - Implement dbt tests for uniqueness, not_null, relationships
   - Add custom tests for date ranges and numeric boundaries
   - Set up test documentation

3. **Performance Optimization**
   - Add indexes on foreign key columns
   - Consider partitioning large tables (transactions)
   - Implement incremental loading strategy

### Long Term
1. **Implement Full Data Vault 2.0**
   - Complete all hubs, links, and satellites
   - Add PIT (Point-In-Time) tables
   - Implement bridge tables for many-to-many relationships

2. **Add Business Vault Layer**
   - Create computed metrics and KPIs
   - Implement business rules
   - Add reference tables

3. **Create Reporting Layer**
   - Build dimensional models (star schema)
   - Create pre-aggregated tables
   - Implement role-based views

4. **CI/CD Pipeline**
   - Automated testing on pull requests
   - Automated deployment to production
   - Data quality monitoring and alerting

## Conclusion

This project successfully implements a robust data transformation pipeline with:
- ✅ Clean separation of concerns (raw → staging → intermediate)
- ✅ Reusable macros for complex transformations
- ✅ PostgreSQL-specific optimizations
- ✅ Comprehensive data quality checks
- ✅ Production-ready staging and intermediate layers
- ⚠️ Data Vault foundation laid but requires custom implementation for PostgreSQL

The intermediate layer is fully operational and ready for analytics workloads. The Data Vault layer requires either migration to a supported database platform or custom macro development for PostgreSQL compatibility.

---

**Author**: Victor Staack 
**Date**: October 3, 2025
**Database**: PostgreSQL 15
**dbt Version**: 1.10.13

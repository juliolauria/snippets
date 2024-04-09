-- SQL_Snippets
-- Converting UTC time
SELECT 
TOP(100) 

CreatedDate
, CreatedDate AT TIME ZONE 'UTC'
, CreatedDate AT TIME ZONE 'UTC' AT TIME ZONE 'Central Europe Standard Time'
, CAST(CreatedDate AT TIME ZONE 'UTC' AT TIME ZONE 'Central Europe Standard Time' AS DATETIME)

FROM [Pacific].[Salesforce_api].[nbavs_CallReporting_c_t] C

-- list tables from databse v1

USE Pacific -- Or change database name here, ie Arctic
select schema_name(t.schema_id) as schema_name,
    t.name as table_name,
    t.create_date,
    t.modify_date
from sys.tables t
order by schema_name,
        table_name

-- List tables from database v2

SELECT
*
FROM
Pacific.INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_SCHEMA, TABLE_NAME
GO

-- Time zones Names
-- select * from sys.time_zone_info

-- cast date as YYYY-MM format
-- CAST(YEAR(Date) AS varchar(50)) + '-' + FORMAT(MONTH(Date), '00')

-- Rank by most recent entry (Over with Partition by)
-- ROW_NUMBER() OVER (PARTITION BY CaseId ORDER BY CreatedDate DESC) AS [Recent_rank]
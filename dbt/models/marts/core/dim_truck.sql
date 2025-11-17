SELECT
    T.TRUCK_ID AS TRUCK_SK,         
    T.TRUCK_ID,  
    T.MAKE,            
    T.TRUCK_OPENING_DATE as TRUCK_OPENING_YEAR,           
    T.MODEL,                       
    -- Calculated attribute: How old the truck is (as of the current year)
    (YEAR(CURRENT_DATE()) - YEAR(T.TRUCK_OPENING_DATE)) AS TRUCK_AGE_YEARS,
    -- Audit Columns
    CURRENT_TIMESTAMP() AS DW_LOAD_TIMESTAMP
FROM {{ ref('raw_pos_truck') }} T 
WHERE T.TRUCK_ID IS NOT NULL
    
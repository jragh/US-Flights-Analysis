-- Account for Average 
CREATE TABLE T100_SEGMENT_ALL_CARRIER_2023_FARES AS 

with fare_pairs as (
SELECT CITYMARKETID_1, CITYMARKETID_2,
AVG(CAST(FARE AS FLOAT)) as AVERAGE_FARE
FROM US_AIRFARE_CITY_PAIRS_2023
GROUP BY CITYMARKETID_1, CITYMARKETID_2),

a as  (
select [ORIGIN_CITY_MARKET_ID] MARKET_ID, ORIGIN_AIRPORT_ID AIRPORT_ID, [origin] AIRPORT_CODE, ORIGIN_CITY_NAME CITY_NAME 
from T100_CITY_MARKETID_LOOKUP
UNION
select [DEST_CITY_MARKET_ID] MARKET_ID, DEST_AIRPORT_ID AIRPORT_ID, [DEST] AIRPORT_CODE, DEST_CITY_NAME CITY_NAME
from T100_CITY_MARKETID_LOOKUP),

final_lookup as (

select b.CITYMARKETID_1, a.AIRPORT_ID AIRPORT_ID_1, a.AIRPORT_CODE AIRPORT_CODE_1,
b.CITYMARKETID_2, c.AIRPORT_ID AIRPORT_ID_2, c.AIRPORT_CODE AIRPORT_CODE_2,
b.AVERAGE_FARE

from fare_pairs b
left join a
on b.citymarketid_1 = a.MARKET_ID

left join a as c
on b.citymarketid_2 = c.MARKET_ID)

-- Will need to take the above query, and then do a double join against the T100 table
-- Check for both directions, and then take the non null side
-- Potentially do a union with this 
-- Also add in case statement for quarter based on month and year
select t.*, fl.AVERAGE_FARE from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP t
INNER join final_lookup fl
on t.ORIGIN_AIRPORT_ID = fl.AIRPORT_ID_1 AND T.ORIGIN = fl.AIRPORT_CODE_1
AND t.DEST_AIRPORT_ID = fl.AIRPORT_ID_2 AND T.DEST = fl.AIRPORT_CODE_2
where cast(t.DEPARTURES_PERFORMED as int) > 0 and CAST(T.PASSENGERS AS INT) > 0

UNION

select t.*, fl.AVERAGE_FARE from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP t
INNER join final_lookup fl
on t.ORIGIN_AIRPORT_ID = fl.AIRPORT_ID_2 AND T.ORIGIN = fl.AIRPORT_CODE_2
AND t.DEST_AIRPORT_ID = fl.AIRPORT_ID_1 AND T.DEST = fl.AIRPORT_CODE_1
where cast(t.DEPARTURES_PERFORMED as int) > 0 and CAST(T.PASSENGERS AS INT) > 0;


---- Query Below for Assessing Revenue By Carrier for Airport Pairs ----
---- Replace Denver and St Louis with Selected Airport 1 & Selected Airport 2 ----
with cte as (

select * from T100_SEGMENT_ALL_CARRIER_2023_FARES
where ORIGIN_AIRPORT_NAME = 'Los Angeles, CA: Los Angeles International'
AND DEST_AIRPORT_NAME = 'New York, NY: John F. Kennedy International' 
and CAST(PASSENGERS AS INT) > 0 and CAST(DEPARTURES_PERFORMED AS INT) > 0

UNION

select * from T100_SEGMENT_ALL_CARRIER_2023_FARES
where ORIGIN_AIRPORT_NAME = 'New York, NY: John F. Kennedy International' 
AND DEST_AIRPORT_NAME = 'Los Angeles, CA: Los Angeles International' 
and CAST(PASSENGERS AS INT) > 0 and CAST(DEPARTURES_PERFORMED AS INT) > 0

),

split_rank as (

select UNIQUE_CARRIER_NAME, 
SUM(CAST(PASSENGERS AS INT) * CAST(AVERAGE_FARE AS FLOAT)) as [Aggregate Revenue],
CASE WHEN SUM(CAST(PASSENGERS AS INT) * CAST(AVERAGE_FARE AS FLOAT)) < ((select SUM(CAST(PASSENGERS AS INT) * CAST(AVERAGE_FARE AS FLOAT)) from cte) / 100.00)
then 'Other Carriers' else UNIQUE_CARRIER_NAME end as [UNIQUE_CARRIER_SIMPLIFIED]
from cte
group by UNIQUE_CARRIER_NAME

)

select cte.UNIQUE_CARRIER_NAME, 
sr.[UNIQUE_CARRIER_SIMPLIFIED],
aclu.[Description] as AIRCRAFT_TYPE,
AVG(cast(cte.AVERAGE_FARE as float)) AS [Average Fare], 
SUM(CAST(cte.PASSENGERS AS INT) * CAST(cte.AVERAGE_FARE AS FLOAT)) as [Total Revenue],
SUM(CAST(cte.PASSENGERS AS INT)) as [Total Passengers],
SUM(CAST(cte.DEPARTURES_PERFORMED AS INT)) AS [Total Flights]
from cte
left join split_rank sr
on cte.UNIQUE_CARRIER_NAME = sr.UNIQUE_CARRIER_NAME

left join T100_SEGMENT_AIRCRAFT_TYPE_LOOKUP_2023 aclu
on cte.AIRCRAFT_TYPE = aclu.Code

GROUP BY cte.UNIQUE_CARRIER_NAME, 
sr.[UNIQUE_CARRIER_SIMPLIFIED],
aclu.[Description]
ORDER BY CAST(sr.[Aggregate Revenue] as int) desc, cte.AIRCRAFT_TYPE;


-- Airport Selection for Route Fares Information --
select ORIGIN_AIRPORT_NAME as [AIRPORT_NAME]
from T100_SEGMENT_ALL_CARRIER_2023_FARES
UNION
select DEST_AIRPORT_NAME as [AIRPORT_NAME]
from T100_SEGMENT_ALL_CARRIER_2023_FARES


-- Airport Selection for second Dropdown --
-- This is used for route Fares Information --
select ORIGIN_AIRPORT_NAME as [AIRPORT_NAME]
from T100_SEGMENT_ALL_CARRIER_2023_FARES
where DEST_AIRPORT_NAME == 'St. Louis, MO: St Louis Lambert International'
UNION
select DEST_AIRPORT_NAME as [AIRPORT_NAME]
from T100_SEGMENT_ALL_CARRIER_2023_FARES
where ORIGIN_AIRPORT_NAME == 'St. Louis, MO: St Louis Lambert International'
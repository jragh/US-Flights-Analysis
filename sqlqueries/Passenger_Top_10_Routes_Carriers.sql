select * from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP
where UNIQUE_CARRIER_NAME like '%Porter%'


-- Main Script to provide top 10 routes for carriers --
-- Will show seats, passengers, and Pct Utilization --
with main_grouping as (
select UNIQUE_CARRIER_NAME,
DEST_AIRPORT_NAME,
ORIGIN_AIRPORT_NAME,
SUM(CAST(PASSENGERS AS INT)) as [TOTAL_PASSENGERS],
SUM(CAST(SEATS AS INT)) as [TOTAL_SEATS]

from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP

where DEST_AIRPORT_NAME != ORIGIN_AIRPORT_NAME
and CAST(PASSENGERS as INT) > 0
and CAST(DEPARTURES_PERFORMED as INT) > 0

group by
UNIQUE_CARRIER_NAME,
DEST_AIRPORT_NAME,
ORIGIN_AIRPORT_NAME
),


-- Lynx Air Calgary & Orlando -- 
-- Orlando to Calgary: 1605 Passengers, 3024 Seats --
-- Calgary to ORlando: 1408 Passengers, 3024 Seats --

sorting as (
select *,
case 
    when DEST_AIRPORT_NAME > ORIGIN_AIRPORT_NAME THEN DEST_AIRPORT_NAME || '_&_' || ORIGIN_AIRPORT_NAME
    WHEN ORIGIN_AIRPORT_NAME > DEST_AIRPORT_NAME then ORIGIN_AIRPORT_NAME || '_&_' || DEST_AIRPORT_NAME
    else 3 end as [testing column]
from main_grouping
--where UNIQUE_CARRIER_NAME in ('1263343 Alberta Inc. d/b/a Lynx Air', 'Porter Airlines, Inc.')
)

select UNIQUE_CARRIER_NAME,
[testing column],
SUM(CAST(TOTAL_PASSENGERS as INT)),
SUM(CAST(TOTAL_SEATS as INT)),
ROW_NUMBER() OVER (PARTITION BY UNIQUE_CARRIER_NAME order by SUM(CAST(TOTAL_PASSENGERS as INT)) desc)

from sorting

group by UNIQUE_CARRIER_NAME,
[testing column]

order by UNIQUE_CARRIER_NAME, SUM(CAST(TOTAL_PASSENGERS as INT)) desc;




---- Trying to Optimize ----
---- Join Lookup on t100 segment table to speed up where query ----
CREATE TABLE [T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP]
as select a.*, 
b.[description] as [DEST_AIRPORT_NAME],
C.[description] as [ORIGIN_AIRPORT_NAME]

from [T100_SEGMENT_ALL_CARRIER_2023] a

left join T100_AIRPORT_CODE_LOOKUP_2023 b
on a.DEST_AIRPORT_ID = b.[CODE]

left join T100_AIRPORT_CODE_LOOKUP_2023 c
on a.ORIGIN_AIRPORT_ID = c.[CODE];


-- Solution joining in the Airport Lookup Table --
-- TRY TO GET THIS QUERY UNDER 1.1 SECOND FOR PERFORMANCE --
/*with a as(
select DEST_AIRPORT_ID,
DEST_AIRPORT_NAME,
ORIGIN_AIRPORT_ID, 
ORIGIN_AIRPORT_NAME,
SUM(CAST([PASSENGERS] as int)) as [ARRIVING PASSENGERS]
from [T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP]
where CAST([Passengers] as INT) > 0 
and CAST([DEPARTURES_PERFORMED] AS int) > 0
and [DEST_AIRPORT_NAME] = 'Albuquerque, NM: Albuquerque International Sunport'
group by DEST_AIRPORT_ID, DEST_AIRPORT_NAME, ORIGIN_AIRPORT_ID, ORIGIN_AIRPORT_NAME
),

totals as (
select a.[DEST_AIRPORT_ID], 
a.[DEST_AIRPORT_NAME], 
a.[ORIGIN_AIRPORT_ID], 
a.[ORIGIN_AIRPORT_NAME],
a.[ARRIVING PASSENGERS],
ROW_NUMBER () over (partition by a.[DEST_AIRPORT_ID] order by a.[ARRIVING PASSENGERS] DESC) as [ORIGIN AIRPORT RANKING]
from a),

carrier_dump as (

select DEST_AIRPORT_ID, 
ORIGIN_AIRPORT_ID,
UNIQUE_CARRIER_NAME, 
SUM(CAST([PASSENGERS] AS INT)) as [CARRIER TOTAL PASSENGERS]
from [T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP] x

where CAST([Passengers] as INT) > 0 
and CAST([DEPARTURES_PERFORMED] AS int) > 0
and [DEST_AIRPORT_NAME] = 'Albuquerque, NM: Albuquerque International Sunport'
group by DEST_AIRPORT_ID, ORIGIN_AIRPORT_ID, UNIQUE_CARRIER_NAME

)

select t.[DEST_AIRPORT_NAME], 
t.[ORIGIN_AIRPORT_NAME], 
SUM(CAST(c.[CARRIER TOTAL PASSENGERS] AS INT)) as [TOTAL_PASSENGERS]
from totals t
inner join carrier_dump c
on t.DEST_AIRPORT_ID = c.DEST_AIRPORT_ID and t.ORIGIN_AIRPORT_ID = c.ORIGIN_AIRPORT_ID
where CAST(t.[ORIGIN AIRPORT RANKING] as INT) <= 10

GROUP BY t.[DEST_AIRPORT_NAME], 
t.[ORIGIN_AIRPORT_NAME]

order by SUM(CAST(c.[CARRIER TOTAL PASSENGERS] AS INT)) desc
;



---- New Attempt at providing top 10 connection airports ----
---- Will be based on both arriving and departing connections ----
---- WORKING CURRENT ----
with origins as (

select [ORIGIN_AIRPORT_NAME],
SUM(CAST([PASSENGERS] AS INT)) as [TOTAL ORIGIN PASSENGERS]
from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP
where CAST([PASSENGERS] as int) > 0 
and CAST([DEPARTURES_PERFORMED] as int) > 0
and [DEST_AIRPORT_NAME] = 'Albuquerque, NM: Albuquerque International Sunport'
group by [ORIGIN_AIRPORT_NAME]),

destinations as (

select [DEST_AIRPORT_NAME],
SUM(CAST([PASSENGERS] AS INT)) as [TOTAL DEST PASSENGERS]
from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP
where CAST([PASSENGERS] as int) > 0 
and CAST([DEPARTURES_PERFORMED] as int) > 0
and [ORIGIN_AIRPORT_NAME] = 'Albuquerque, NM: Albuquerque International Sunport'
group by [DEST_AIRPORT_NAME]

),

window as (

select COALESCE(o.[ORIGIN_AIRPORT_NAME], d.[DEST_AIRPORT_NAME]) as [AIRPORT NAME],
COALESCE(cast(o.[TOTAL ORIGIN PASSENGERS] as int), 0) as [INBOUND PASSENGERS],
COALESCE(cast(d.[TOTAL DEST PASSENGERS] as int), 0) as [OUTBOUND PASSENGERS],
(COALESCE(cast(o.[TOTAL ORIGIN PASSENGERS] as int), 0) + COALESCE(cast(d.[TOTAL DEST PASSENGERS] as int), 0)) as [TOTAL PASSENGERS],

ROW_NUMBER() OVER (order by (COALESCE(cast(o.[TOTAL ORIGIN PASSENGERS] as int), 0) + COALESCE(cast(d.[TOTAL DEST PASSENGERS] as int), 0)) desc) as [PASSENGER RANKING]


from origins o
FULL OUTER JOIN destinations d
on o.[ORIGIN_AIRPORT_NAME] = d.[DEST_AIRPORT_NAME])

select * from window
where [PASSENGER RANKING] <= 10
order by CAST([TOTAL PASSENGERS] as int) desc;
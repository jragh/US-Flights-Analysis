-- Window will be setup for Passenger Utilization by Route --
-- SELECT THIS INTO A TABLE TO SPEED UP QUERY TIME FROM APPLICATION --
CREATE TABLE T100_AIRPORT_SELECTION AS
select ORIGIN_AIRPORT_NAME as [AIRPORT_NAME] 
from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 
where CAST(PASSENGERS AS INT) >= 1
and CAST([DEPARTURES_PERFORMED] AS INT) >= 1
and ORIGIN_AIRPORT_NAME is not null
union
select DEST_AIRPORT_NAME as [AIRPORT_NAME] 
from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 
where CAST(PASSENGERS AS INT) >= 1
and CAST([DEPARTURES_PERFORMED] AS INT) >= 1
and DEST_AIRPORT_NAME is not null;

select AIRPORT_NAME from T100_AIRPORT_SELECTION;



-- Query to calculate passenger utilization from passengers and seats --
-- Need 2 airport pairs --
-- Airport selection needs to exclude airports that are not connected to current airport --
with cte as (

select UNIQUE_CARRIER_NAME, 
cast(MONTH AS INT) AS [MONTH],
SUM(CAST(PASSENGERS AS INT)) AS [Total Passengers],
SUM(CAST(SEATS AS INT)) AS [Total Seats],
SUM(CAST([DEPARTURES_PERFORMED] AS INT)) AS [Total Flights]

FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

WHERE DEST_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
and ORIGIN_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
AND CAST(PASSENGERS AS INT) >= 1
and CAST([DEPARTURES_PERFORMED] AS INT) >= 1
group by  UNIQUE_CARRIER_NAME,CAST(MONTH as int)

), 


grouped_totals as (
select UNIQUE_CARRIER_NAME,
SUM(CAST(PASSENGERS AS INT)) as [TOTAL_PASSENGERS],
SUM(CAST(PASSENGERS AS FLOAT)) / (select SUM(CAST([PASSENGERS] AS FLOAT)) FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

WHERE DEST_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
and ORIGIN_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
AND CAST(PASSENGERS AS INT) >= 1
and CAST([DEPARTURES_PERFORMED] AS INT) >= 1) as [PCT_ANALYSIS]

FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

WHERE DEST_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
and ORIGIN_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
AND CAST(PASSENGERS AS INT) >= 1
and CAST([DEPARTURES_PERFORMED] AS INT) >= 1
group by UNIQUE_CARRIER_NAME
)


select
CASE WHEN CAST(gt.[PCT_ANALYSIS] as float) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end as [Unique Carrier Simplified],
CAST(cte.[Month] as int) as [Month Number],
mlu.MONTH_NAME_SHORT as [Month],
SUM(CAST(cte.[Total Passengers] as int)) as [Total Passengers],
SUM(CAST(cte.[Total Seats] as int)) as [Total Seats],
SUM(CAST(cte.[Total Flights] as int)) as [Total Flights]

from cte
left join grouped_totals gt
on cte.UNIQUE_CARRIER_NAME = gt.UNIQUE_CARRIER_NAME

left join MONTHS_LOOKUP mlu
on cte.[Month] = mlu.[Month]

group by CASE WHEN CAST(gt.[PCT_ANALYSIS] as float) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end,
CAST(cte.[Month] as int),
mlu.[MONTH_NAME_SHORT]











with cte as (

        select UNIQUE_CARRIER_NAME, 
        cast(MONTH AS INT) AS [MONTH],
        SUM(CAST(PASSENGERS AS INT)) AS [Total Passengers],
        SUM(CAST(SEATS AS INT)) AS [Total Seats],
        SUM(CAST([DEPARTURES_PERFORMED] AS INT)) AS [Total Flights]

        FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

        WHERE DEST_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
        and ORIGIN_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
        and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
        AND CAST(PASSENGERS AS INT) >= 1
        and CAST([DEPARTURES_PERFORMED] AS INT) >= 1
        group by  UNIQUE_CARRIER_NAME,CAST(MONTH as int)

        ), 


        grouped_totals as (
        select UNIQUE_CARRIER_NAME,
        SUM(CAST(PASSENGERS AS INT)) as [TOTAL_PASSENGERS],
        SUM(CAST(PASSENGERS AS FLOAT)) / (select SUM(CAST([PASSENGERS] AS FLOAT)) FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

        WHERE DEST_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
        and ORIGIN_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
        and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
        AND CAST(PASSENGERS AS INT) >= 1
        and CAST([DEPARTURES_PERFORMED] AS INT) >= 1) as [PCT_ANALYSIS]

        FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

        WHERE DEST_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
        and ORIGIN_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
        and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
        AND CAST(PASSENGERS AS INT) >= 1
        and CAST([DEPARTURES_PERFORMED] AS INT) >= 1
        group by UNIQUE_CARRIER_NAME
        )


        select
        CASE WHEN CAST(gt.[PCT_ANALYSIS] as float) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end as [Unique Carrier Simplified],
        CAST(cte.[Month] as int) as [Month Number],
        mlu.MONTH_NAME_SHORT as [Month],
        SUM(CAST(cte.[Total Passengers] as int)) as [Total Passengers],
        SUM(CAST(cte.[Total Seats] as int)) as [Total Seats],
        SUM(CAST(cte.[Total Flights] as int)) as [Total Flights]

        from cte
        left join grouped_totals gt
        on cte.UNIQUE_CARRIER_NAME = gt.UNIQUE_CARRIER_NAME

        left join MONTHS_LOOKUP mlu
        on cte.[Month] = mlu.[Month]

        group by CASE WHEN CAST(gt.[PCT_ANALYSIS] as float) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end,
        CAST(cte.[Month] as int),
        mlu.[MONTH_NAME_SHORT]
        



-- Query By Carrier by Month (Every available Month --
with cte as (

select UNIQUE_CARRIER_NAME, 
cast(MONTH AS INT) AS [MONTH],
SUM(CAST(PASSENGERS AS INT)) AS [Total Passengers],
SUM(CAST(SEATS AS INT)) AS [Total Seats],
SUM(CAST([DEPARTURES_PERFORMED] AS INT)) AS [Total Flights]

FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

WHERE DEST_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
and ORIGIN_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
AND CAST(PASSENGERS AS INT) >= 1
and CAST([DEPARTURES_PERFORMED] AS INT) >= 1
group by  UNIQUE_CARRIER_NAME,CAST(MONTH as int)

), 


grouped_totals as (
select UNIQUE_CARRIER_NAME,
SUM(CAST(PASSENGERS AS INT)) as [TOTAL_PASSENGERS],
SUM(CAST(PASSENGERS AS FLOAT)) / (select SUM(CAST([PASSENGERS] AS FLOAT)) FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

WHERE DEST_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
and ORIGIN_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
AND CAST(PASSENGERS AS INT) >= 1
and CAST([DEPARTURES_PERFORMED] AS INT) >= 1) as [PCT_ANALYSIS]

FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP 

WHERE DEST_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
and ORIGIN_AIRPORT_NAME in ('Los Angeles, CA: Los Angeles International', 'New York, NY: John F. Kennedy International')
and ORIGIN_AIRPORT_NAME <> DEST_AIRPORT_NAME
AND CAST(PASSENGERS AS INT) >= 1
and CAST([DEPARTURES_PERFORMED] AS INT) >= 1
group by UNIQUE_CARRIER_NAME
)


select
CASE WHEN CAST(gt.[PCT_ANALYSIS] as float) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end as [Unique Carrier Simplified],
CAST(cte.[Month] as int) as [Month Number],
mlu.MONTH_NAME_SHORT as [Month],
SUM(CAST(cte.[Total Passengers] as int)) as [Total Passengers],
SUM(CAST(cte.[Total Seats] as int)) as [Total Seats],
SUM(CAST(cte.[Total Flights] as int)) as [Total Flights]

from cte
left join grouped_totals gt
on cte.UNIQUE_CARRIER_NAME = gt.UNIQUE_CARRIER_NAME

left join MONTHS_LOOKUP mlu
on cte.[Month] = mlu.[Month]

where CASE WHEN CAST(gt.[PCT_ANALYSIS] as float) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end = 'American Airlines Inc.'

group by CASE WHEN CAST(gt.[PCT_ANALYSIS] as float) < 0.01 THEN 'Other Carriers' else cte.UNIQUE_CARRIER_NAME end,
CAST(cte.[Month] as int),
mlu.[MONTH_NAME_SHORT]




---- Testing for Airport Selection Query in dropdown list ----
---- Included where clause to add filters for passengers, seats, and departure counts ----
select ORIGIN_AIRPORT_NAME as [AIRPORT_NAME], Month, Passengers, Seats, Departures_Performed
from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP
where DEST_AIRPORT_NAME == 'Santiago, Chile: Arturo Merino Benitez International'
and CAST(Passengers as int) > 0 AND CAST(SEATS AS INT) > 0 and CAST(departures_performed as int) > 0
UNION
select DEST_AIRPORT_NAME as [AIRPORT_NAME], Month, Passengers, Seats, Departures_Performed
from T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP
where ORIGIN_AIRPORT_NAME == 'Santiago, Chile: Arturo Merino Benitez International'
and CAST(Passengers as int) > 0 AND CAST(SEATS AS INT) > 0 and CAST(departures_performed as int) > 0
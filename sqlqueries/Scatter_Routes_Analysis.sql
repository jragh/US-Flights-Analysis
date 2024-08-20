-- Query to be used when All Carriers Option Selected --
-- Highlights the Load factor for each airline in 2023 with specified criteria below --
select UNIQUE_CARRIER_NAME,
sum(cast(passengers as int)) as [Total Passengers],
sum(cast(seats as int)) as [Total Seats],
sum(cast(departures_performed as int)) as [Total Flights],
sum(cast(passengers as float)) / sum(cast(seats as float)) as [Load Factor Ratio]

FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP

where CAST(DEPARTURES_PERFORMED AS INT) > 0
and CAST(PASSENGERS AS INT) > 0
and DEST_AIRPORT_NAME <> ORIGIN_AIRPORT_NAME
AND CAST(SEATS AS INT) > 0

group by UNIQUE_CARRIER_NAME
having sum(cast(departures_performed as int)) >= 200
ORDER BY sum(cast(departures_performed as int)) DESC;


-- SETTING UP SCATTERPLOT QUERY FOR A SPECIFIC AIRLINE CARRIER WHEN SELECTED --
-- SPECIFIC AIRLINE QUERY --
select UNIQUE_CARRIER_NAME, 
CASE 
    WHEN DEST || ': ' || DEST_CITY_NAME > ORIGIN || ': ' || ORIGIN_CITY_NAME then DEST || ': ' || DEST_CITY_NAME || ' & ' || ORIGIN || ': ' || ORIGIN_CITY_NAME
    WHEN ORIGIN || ': ' || ORIGIN_CITY_NAME > DEST || ': ' || DEST_CITY_NAME THEN ORIGIN || ': ' || ORIGIN_CITY_NAME || ' & ' || DEST || ': ' || DEST_CITY_NAME
    ELSE ORIGIN || ': ' || ORIGIN_CITY_NAME || ' & ' || DEST || ': ' || DEST_CITY_NAME 
END AS AIRPORT_PAIR,
SUM(CAST(SEATS as INT)) as [Total Seats],
SUM(CAST(PASSENGERS as INT)) as [Total Passengers],
SUM(CAST(DEPARTURES_PERFORMED AS INT)) AS [Total Flights],
SUM(CAST(PASSENGERS as float)) / SUM(CAST(SEATS as float)) as [Load Factor Ratio]
FROM T100_SEGMENT_ALL_CARRIER_2023_AIRPORTS_LOOKUP
where CAST(DEPARTURES_PERFORMED AS INT) > 0
and CAST(PASSENGERS AS INT) > 0
and DEST_AIRPORT_NAME <> ORIGIN_AIRPORT_NAME
AND CAST(SEATS AS INT) > 0
AND UNIQUE_CARRIER_NAME = 'Southwest Airlines Co.'

group by UNIQUE_CARRIER_NAME, 
CASE 
    WHEN DEST || ': ' || DEST_CITY_NAME > ORIGIN || ': ' || ORIGIN_CITY_NAME then DEST || ': ' || DEST_CITY_NAME || ' & ' || ORIGIN || ': ' || ORIGIN_CITY_NAME
    WHEN ORIGIN || ': ' || ORIGIN_CITY_NAME > DEST || ': ' || DEST_CITY_NAME THEN ORIGIN || ': ' || ORIGIN_CITY_NAME || ' & ' || DEST || ': ' || DEST_CITY_NAME
    ELSE ORIGIN || ': ' || ORIGIN_CITY_NAME || ' & ' || DEST || ': ' || DEST_CITY_NAME 
END

-- 20 Flights Needed for this query to return values --
having SUM(CAST(DEPARTURES_PERFORMED AS INT)) > 20

ORDER BY SUM(CAST(DEPARTURES_PERFORMED AS INT)) DESC, SUM(CAST(SEATS AS INT)) DESC;



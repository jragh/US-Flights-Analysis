-- Group by for Airports with Basic Summary Stats --
select b.[DESCRIPTION] as [ORIGIN AIRPORT NAME],
a.[UNIQUE_CARRIER_NAME] as [UNIQUE CARRIER NAME],
SUM(CAST(a.[PASSENGERS] as INT)) as [TOTAL PASSENGERS],
SUM(CAST(a.[DEPARTURES_PERFORMED] as INT)) as [TOTAL DEPARTED FLIGHTS],
COUNT(distinct c.[DESCRIPTION]) as [TOTAL DESTINATION AIRPORTS]

FROM [T100_SEGMENT_ALL_CARRIER_2023] a
left join [T100_AIRPORT_CODE_LOOKUP_2023] b
on a.[ORIGIN_AIRPORT_ID] = b.[CODE]
left join [T100_AIRPORT_CODE_LOOKUP_2023] c
on a.[DEST_AIRPORT_ID] = c.[CODE]

WHERE CAST(a.[PASSENGERS] AS INT) > 0 
AND CAST([DEPARTURES_PERFORMED] AS INT) > 0
AND b.[DESCRIPTION] is not null
AND a.[ORIGIN_COUNTRY_NAME] = 'United States'


GROUP BY b.[DESCRIPTION], a.[UNIQUE_CARRIER_NAME]

order by SUM(CAST(a.[PASSENGERS] as INT)) desc;


-- Group By for Airport Filter List --
select b.[DESCRIPTION] as [CITY AIRPORT NAME], count(*) as [NUMBER OF RECORDS]
from [T100_SEGMENT_ALL_CARRIER_2023] a
left join T100_AIRPORT_CODE_LOOKUP_2023 b
on a.[ORIGIN_AIRPORT_ID] = b.[CODE]
where CAST(a.[PASSENGERS] AS INT) > 0
and CAST(a.[SEATS] AS INT) > 0
AND CAST(a.[DEPARTURES_PERFORMED] as int) > 0
and b.[DESCRIPTION] is not null
and a.[ORIGIN_COUNTRY_NAME] LIKE 'United States'
group by b.[DESCRIPTION]
ORDER BY b.[DESCRIPTION] ASC;
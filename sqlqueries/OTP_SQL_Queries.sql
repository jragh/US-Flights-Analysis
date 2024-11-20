select "MONTH",
SUM(case when "CARRIER_DELAY" is null then 1 else 0 end) as "Carrier Delays",
SUM(case when "WEATHER_DELAY" is null then 1 else 0 end) as "Weather Delays",
SUM(case when "NAS_DELAY" is null then 1 else 0 end) as "NAS Delays",
SUM(case when "SECURITY_DELAY" is null then 1 else 0 end) as "Security Delays",
SUM(case when "LATE_AIRCRAFT_DELAY" is null then 1 else 0 end) as "Late Aircraft Delays"


from public.t_ontime_reporting_2023 

group by "MONTH"

order by cast("MONTH" as real);


select * from public.t_ontime_reporting_2023 limit 1000;

select "OP_UNIQUE_CARRIER", COUNT(*) as "NUMBER OF RECORDS"
from public.t_ontime_reporting_2023
group by "OP_UNIQUE_CARRIER"
order by "OP_UNIQUE_CARRIER" asc; 


---- Line Graph with Confidence Intervals Per Carrier ----
---- Includes Daily Averages, Counts, and Split By Delay Type ----

with dfi_stats as (

select "OP_UNIQUE_CARRIER" as "Unique Carrier Code",
row_number() over (partition by "OP_UNIQUE_CARRIER" order by cast("FL_DATE" as DATE) asc) as "Date Ordering",
cast("FL_DATE" as date) as "Flight Date",
AVG(cast("ARR_DELAY" as real)) as "Average Arrival Delay",
stddev(cast("ARR_DELAY" as real)) as "Arrival Delay Stardard Deviation",
SUM(cast("FLIGHTS" as real)) as "Number of Flights",
-- Confidence Interval Daily --
AVG(cast("ARR_DELAY" as real)) + 1.96 * stddev(cast("ARR_DELAY" as real)) / sqrt(SUM(cast("FLIGHTS" as real))) as "CI Daily Upper",
AVG(cast("ARR_DELAY" as real)) - 1.96 * stddev(cast("ARR_DELAY" as real)) / sqrt(SUM(cast("FLIGHTS" as real))) as "CI Daily Lower" 

-- movMean + Z * movStd / np.sqrt(N)


from public.t_ontime_reporting_2023 
where "CANCELLED" = 0
-- and date_part('month', cast("FL_DATE" as date)) = 1

group by "OP_UNIQUE_CARRIER", cast("FL_DATE" as date)),

dfi_rolling_stats as (

select a.*,
AVG(a."Average Arrival Delay") over (partition by a."Unique Carrier Code" order by a."Flight Date" rows between 6 PRECEDING and current ROW) as "Grouped Rolling Average",
stddev_samp(a."Average Arrival Delay") over (partition by a."Unique Carrier Code" order by a."Flight Date" rows between 6 PRECEDING and current ROW) as "Grouped Standard Deviation"


from dfi_stats as a),


carrier_lookup as (

select distinct unique_carrier, unique_carrier_name
from public.t100_segment_all_carrier_2023)

select a.*,

b.unique_carrier_name as "Unique Carrier Name",
a."Grouped Rolling Average" + 1.96 * a."Grouped Standard Deviation" / sqrt(7) as "CI Grouped Upper",
a."Grouped Rolling Average" - 1.96 * a."Grouped Standard Deviation" / sqrt(7) as "CI Grouped Lower"

into public.otp_daily_average

from dfi_rolling_stats a
left join carrier_lookup b
on a."Unique Carrier Code" = b.unique_carrier

order by a."Unique Carrier Code", a."Flight Date" asc;

select distinct "Unique Carrier Name" from public.otp_daily_average oda order by "Unique Carrier Name"

order by "OP_UNIQUE_CARRIER", cast("FL_DATE" as date)

select count(distinct "FL_DATE") from public.t_ontime_reporting_2023

select * from public.t100_segment_all_carrier_2023 limit 1000



group by unique_carrier
--having count(*) > 1
order by count(*) desc;



---- Scatter Plot Joining On time performance vs passenger counts ----
-- T100 Data pull for Passenger & Flight Counts --
select 

unique_carrier,
unique_carrier_name, 
origin,
origin_airport_name,
dest,
dest_airport_name,
month,
SUM(cast(departures_performed as decimal(20, 2))) "Number of Flights",
SUM(cast(seats as decimal(20, 2))) "Number of Seats",
SUM(cast(passengers as decimal(20, 2))) "Number of Passengers"

from public.t100_segment_all_carrier_2023_airports_lookup
group by unique_carrier,
unique_carrier_name, 
origin,
origin_airport_name,
dest,
dest_airport_name,
month

order by unique_carrier, cast(month as real) asc;

-- OTP Data Pull --
-- non Cancelled Flights, count --
select * from public.t_ontime_reporting_2023 limit 1000;

select * from public.t_ontime_reporting_2023 where "CANCELLED" != 0  and "OP_UNIQUE_CARRIER" = 'AA'limit 1000;


select 

"OP_UNIQUE_CARRIER",
"ORIGIN",
"DEST",
"MONTH" as "MONTH",

SUM(cast("FLIGHTS" as decimal(20, 2))) as "Number of Flights OTP",

SUM(cast("ARR_DELAY" as DECIMAL(20, 2))) as "Total Arrival Performance",
SUM(case when "ARR_DELAY" is not null and cast("ARR_DELAY" as numeric(20,2)) > 0 then 1 else 0 end) as "Total Delays",

SUM(cast("CARRIER_DELAY" as DECIMAL(20, 2))) as "Carrier Delay Time",
SUM(case when "CARRIER_DELAY" is not null and cast("CARRIER_DELAY" as numeric(20,2)) > 0 then 1 else 0 end) as "Carrier Delays",

SUM(cast("WEATHER_DELAY" as DECIMAL(20, 2))) as "Weather Delay Time",
SUM(case when "WEATHER_DELAY" is not null and cast("WEATHER_DELAY" as numeric(20,2)) > 0 then 1 else 0 end) as "Weather Delays",

SUM(cast("NAS_DELAY" as DECIMAL(20, 2))) as "NAS Delay Time",
SUM(case when "NAS_DELAY" is not null and cast("NAS_DELAY" as numeric(20,2)) > 0 then 1 else 0 end) as "NAS Delays",

SUM(cast("SECURITY_DELAY" as DECIMAL(20, 2))) as "Security Delay Time",
SUM(case when "SECURITY_DELAY" is not null and cast("SECURITY_DELAY" as numeric(20,2)) > 0 then 1 else 0 end) as "Security Delays",

SUM(cast("LATE_AIRCRAFT_DELAY" as DECIMAL(20, 2))) as "Late Aircraft Delay Time",
SUM(case when "LATE_AIRCRAFT_DELAY" is not null and cast("LATE_AIRCRAFT_DELAY" as numeric(20,2)) > 0 then 1 else 0 end) as "Late Aircraft Delays"

from public.t_ontime_reporting_2023
where ("CANCELLED" is null or "CANCELLED" = 0)

group by "OP_UNIQUE_CARRIER",
"ORIGIN",
"DEST",
"MONTH"

order by "OP_UNIQUE_CARRIER" asc,
cast("MONTH" as real) asc,
"ORIGIN",
"DEST";


-- Averages, Sums, Possibly Medians for Scatter Plot Overall, Variance?? Standard Deviation?? --
-- No Group By Month as This is overall --
-- Scatterplot By Carrier With Histogram for Average Delays --
-- Y Axis will be number of flights --
-- X Axis will be Average Arrival Delay --
-- Dropdown for different delay metrics --

select 

"OP_UNIQUE_CARRIER",
"ORIGIN",
"DEST",

SUM(cast("FLIGHTS" as decimal(20, 2))) as "Number of Flights OTP",

SUM(cast("ARR_DELAY" as DECIMAL(20, 2))) as "Total Arrival Performance",
SUM(case when "ARR_DELAY" is not null and cast("ARR_DELAY" as numeric(20,2)) > 0 then 1 else 0 end) as "Total Delays",
AVG(cast(cast("ARR_DELAY" as DECIMAL(20, 2)) * 1.00 as FLOAT)) as "Average Arrival Delay Performance",

SUM(cast("CARRIER_DELAY" as DECIMAL(20, 2))) as "Carrier Delay Time",
SUM(case when "CARRIER_DELAY" is not null and cast("CARRIER_DELAY" as numeric(20,2)) > 0 then 1 else 0 end) as "Carrier Delays",
AVG(cast(cast("CARRIER_DELAY" as DECIMAL(20, 2)) * 1.00 as FLOAT)) as "Average Carrier Delay Performance",

SUM(cast("WEATHER_DELAY" as DECIMAL(20, 2))) as "Weather Delay Time",
SUM(case when "WEATHER_DELAY" is not null and cast("WEATHER_DELAY" as numeric(20,2)) > 0 then 1 else 0 end) as "Weather Delays",
AVG(cast(cast("WEATHER_DELAY" as DECIMAL(20, 2)) * 1.00 as FLOAT)) as "Average Weather Delay Performance",

SUM(cast("NAS_DELAY" as DECIMAL(20, 2))) as "NAS Delay Time",
SUM(case when "NAS_DELAY" is not null and cast("NAS_DELAY" as numeric(20,2)) > 0 then 1 else 0 end) as "NAS Delays",
AVG(cast(cast("NAS_DELAY" as DECIMAL(20, 2)) * 1.00 as FLOAT)) as "Average NAS Delay Performance",

SUM(cast("SECURITY_DELAY" as DECIMAL(20, 2))) as "Security Delay Time",
SUM(case when "SECURITY_DELAY" is not null and cast("SECURITY_DELAY" as numeric(20,2)) > 0 then 1 else 0 end) as "Security Delays",
AVG(cast(cast("SECURITY_DELAY" as DECIMAL(20, 2)) * 1.00 as FLOAT)) as "Average Security Delay Performance",

SUM(cast("LATE_AIRCRAFT_DELAY" as DECIMAL(20, 2))) as "Late Aircraft Delay Time",
SUM(case when "LATE_AIRCRAFT_DELAY" is not null and cast("LATE_AIRCRAFT_DELAY" as numeric(20,2)) > 0 then 1 else 0 end) as "Late Aircraft Delays",
AVG(cast(cast("LATE_AIRCRAFT_DELAY" as DECIMAL(20, 2)) * 1.00 as FLOAT)) as "Average Late Arrival Delay Performance"

from public.t_ontime_reporting_2023
where ("CANCELLED" is null or "CANCELLED" = 0)

group by "OP_UNIQUE_CARRIER",
"ORIGIN",
"DEST"

having SUM(cast("FLIGHTS" as decimal(20, 2))) > 24

order by "OP_UNIQUE_CARRIER" asc,
"ORIGIN",
"DEST";


---- Simple Graph Bar Chart Horizontal ----
---- Displays by Carrier how their delays are being generated ----
---- when there is a delay how many minutes caused by each category ----
select * from public.t_ontime_reporting_2023 limit 1000

select "OP_UNIQUE_CARRIER",
SUM(case when cast("ARR_DELAY" as decimal(20, 2)) > 0 then cast("ARR_DELAY" as decimal(20, 2)) else null end) as "Total Delay Neg",
SUM(cast("FLIGHTS" as decimal(20, 2))) as "Total Flights",

SUM(cast("CARRIER_DELAY" as DECIMAL(20, 2))) as "Carrier Delay Time",
SUM(cast("CARRIER_DELAY" as DECIMAL(20, 2))) /  SUM(case when cast("ARR_DELAY" as decimal(20, 2)) > 0 then cast("ARR_DELAY" as decimal(20, 2)) else null end) as "Pct Carrier Delay Mins",

SUM(cast("WEATHER_DELAY" as DECIMAL(20, 2))) as "Weather Delay Time",
SUM(cast("WEATHER_DELAY" as DECIMAL(20, 2))) /  SUM(case when cast("ARR_DELAY" as decimal(20, 2)) > 0 then cast("ARR_DELAY" as decimal(20, 2)) else null end) as "Pct Weather Delay Mins",

SUM(cast("NAS_DELAY" as DECIMAL(20, 2))) as "NAS Delay Time",
SUM(cast("NAS_DELAY" as DECIMAL(20, 2))) /  SUM(case when cast("ARR_DELAY" as decimal(20, 2)) > 0 then cast("ARR_DELAY" as decimal(20, 2)) else null end) as "Pct NAS Delay Mins",

SUM(cast("SECURITY_DELAY" as DECIMAL(20, 2))) as "Security Delay Time",
SUM(cast("SECURITY_DELAY" as DECIMAL(20, 2))) /  SUM(case when cast("ARR_DELAY" as decimal(20, 2)) > 0 then cast("ARR_DELAY" as decimal(20, 2)) else null end) as "Pct Security Delay Mins",

SUM(cast("LATE_AIRCRAFT_DELAY" as DECIMAL(20, 2))) as "Late Aircraft Delay Time",
SUM(cast("LATE_AIRCRAFT_DELAY" as DECIMAL(20, 2))) /  SUM(case when cast("ARR_DELAY" as decimal(20, 2)) > 0 then cast("ARR_DELAY" as decimal(20, 2)) else null end) as "Pct Late Aircraft Delay Mins"


from public.t_ontime_reporting_2023
group by "OP_UNIQUE_CARRIER"
order by SUM(case when cast("ARR_DELAY" as decimal(20, 2)) > 0 then cast("ARR_DELAY" as decimal(20, 2)) else null end) desc;


---- Average Delay Time, Median Delay Time, Number of Delayed Flights, Number of Scheduled Flights, % On Time ----
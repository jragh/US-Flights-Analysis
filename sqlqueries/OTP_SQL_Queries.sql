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

---- This needs to be selected into it's own table ----
---- By Carrier ----


with carrier as (

select unique_carrier, unique_carrier_name, count(*) as "Number of Records" 
from public.t100_segment_all_carrier_2023
where unique_carrier in (select distinct "OP_UNIQUE_CARRIER" from public.t_ontime_reporting_2023)
group by unique_carrier, unique_carrier_name

)

select 

b."unique_carrier_name" as "Carrier Name",

case 
	when c.description > d.description then CONCAT(c.description, ' - ', d.description)
	else CONCAT(d.description, ' - ', c.description)
end as "Route Description",

SUM(cast(a."FLIGHTS" as real)) as "Number of Flights OTP",

SUM(cast(a."ARR_DELAY" as real)) as "Total Arrival Performance",
SUM(case when a."ARR_DELAY" is not null and cast(a."ARR_DELAY" as real) > 0 then 1 else 0 end) as "Total Delays",
AVG(cast(cast(a."ARR_DELAY" as real) * 1.00 as FLOAT)) as "Average Arrival Delay Performance",

SUM(cast(a."CARRIER_DELAY" as real)) as "Carrier Delay Time",
SUM(case when a."CARRIER_DELAY" is not null and cast(a."CARRIER_DELAY" as real) > 0 then 1 else 0 end) as "Carrier Delays",
AVG(cast(cast(a."CARRIER_DELAY" as real) * 1.00 as FLOAT)) as "Average Carrier Delay Performance",

SUM(cast(a."WEATHER_DELAY" as real)) as "Weather Delay Time",
SUM(case when a."WEATHER_DELAY" is not null and cast(a."WEATHER_DELAY" as real) > 0 then 1 else 0 end) as "Weather Delays",
AVG(cast(cast(a."WEATHER_DELAY" as real) * 1.00 as FLOAT)) as "Average Weather Delay Performance",

SUM(cast(a."NAS_DELAY" as real)) as "NAS Delay Time",
SUM(case when a."NAS_DELAY" is not null and cast(a."NAS_DELAY" as real) > 0 then 1 else 0 end) as "NAS Delays",
AVG(cast(cast(a."NAS_DELAY" as real) * 1.00 as FLOAT)) as "Average NAS Delay Performance",

SUM(cast(a."SECURITY_DELAY" as real)) as "Security Delay Time",
SUM(case when a."SECURITY_DELAY" is not null and cast(a."SECURITY_DELAY" as real) > 0 then 1 else 0 end) as "Security Delays",
AVG(cast(cast(a."SECURITY_DELAY" as real) * 1.00 as FLOAT)) as "Average Security Delay Performance",

SUM(cast(a."LATE_AIRCRAFT_DELAY" as real)) as "Late Aircraft Delay Time",
SUM(case when a."LATE_AIRCRAFT_DELAY" is not null and cast(a."LATE_AIRCRAFT_DELAY" as real) > 0 then 1 else 0 end) as "Late Aircraft Delays",
AVG(cast(cast(a."LATE_AIRCRAFT_DELAY" as real) * 1.00 as FLOAT)) as "Average Late Arrival Delay Performance"

from public.t_ontime_reporting_2023 a
left join carrier b
on a."OP_UNIQUE_CARRIER" = b.unique_carrier
left join public.t100_airport_code_lookup_2023 c
on a."ORIGIN_AIRPORT_ID" = cast(c.code as integer) 
left join public.t100_airport_code_lookup_2023 d
on a."DEST_AIRPORT_ID" = cast(d.code as integer)



where (a."CANCELLED" is null or a."CANCELLED" = 0)

group by b."unique_carrier_name" ,
2

having SUM(cast(a."FLIGHTS" as real)) > 24

order by b."unique_carrier_name" asc,
2;



select * from public.t_ontime_reporting_2023
where "OP_UNIQUE_CARRIER" = '9E'
and "ORIGIN" in ('BUF', 'JFK')
and "DEST" in ('BUF', 'JFK')

select cast("code" as integer) as "code", "description"
from public.t100_airport_code_lookup_2023
where "code" in ('10792', '12478')

select * from public.us_airfare_carrier_lookup
where "code" = '9E'


select unique_carrier, unique_carrier_name, count(*) as "Number of Records" 
from public.t100_segment_all_carrier_2023
where unique_carrier in (select distinct "OP_UNIQUE_CARRIER" from public.t_ontime_reporting_2023)
group by unique_carrier, unique_carrier_name 
order by unique_carrier 

select * from public.t_ontime_reporting_2023


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


-- By Carrier View --
with all_otp as (
select *, 

case 
	when cast("ARR_DELAY" as decimal(20, 2)) < -10.0 then 'Early > 10 Mins'
	when cast("ARR_DELAY" as decimal(20, 2)) >= -10.0 and cast("ARR_DELAY" as decimal(20, 2)) < 0.00 then 'Early < 10 Mins'
	when cast("ARR_DELAY" as decimal(20, 2)) >= 0.00 and cast("ARR_DELAY" as decimal(20, 2)) < 10.00 then 'Late < 10 Mins'
	when cast("ARR_DELAY" as decimal(20, 2)) >= 10.00 then 'Late > 10 Mins'
end as "ARR_DELAY_CLASS"


from public.t_ontime_reporting_2023
where "CANCELLED" = 0
and "ORIGIN" <> "DEST"
and "ARR_DELAY" is not null),

carriers as (

select distinct unique_carrier, unique_carrier_name
from public.t100_segment_all_carrier_2023

)

select a."OP_UNIQUE_CARRIER" as "Unique Carrier Code",
c.unique_carrier_name as "Unique Carrier Name",
cast(a."MONTH" as real) as "Month Number",
b.month_name_short as "Month Name",
a."ARR_DELAY_CLASS" as "Arrival Delay Classification",

SUM(cast(a."FLIGHTS" as decimal(20, 2))) as "Total Flights"

--into public.otp_carrier_monthly_delay_class

from all_otp a
left join carriers c
on a."OP_UNIQUE_CARRIER" = c.unique_carrier

left join public.months_lookup b
on cast(a."MONTH" as real) = b.month

where a."CANCELLED" = 0
and a."ORIGIN" <> a."DEST"
and a."ARR_DELAY" is not null

group by a."OP_UNIQUE_CARRIER", c.unique_carrier_name, cast(a."MONTH" as real), b.month_name_short, a."ARR_DELAY_CLASS"

order by c.unique_carrier_name asc, cast(a."MONTH" as real) asc, a."ARR_DELAY_CLASS" asc;

-- Average Delay By Carrier with Confidence Intervals --
with carriers as (

select distinct unique_carrier, unique_carrier_name
from public.t100_segment_all_carrier_2023

)

select

a."OP_UNIQUE_CARRIER" as "Unique Carrier Code",
c.unique_carrier_name as "Unique Carrier Name",

cast(a."MONTH" as real) as "Month Number",
b.month_name_short as "Month Name",
AVG(cast(a."ARR_DELAY" as decimal(20, 2))) as "Average Delay",
SUM(cast(a."FLIGHTS" as decimal(20, 2))) as "Total Flights",
STDDEV(cast(a."ARR_DELAY" as decimal(20, 2))) as "Delay Standard Deviation",

AVG(cast(a."ARR_DELAY" as decimal(20, 2))) + (1.96 * (STDDEV(cast(a."ARR_DELAY" as decimal(20, 2))) / sqrt(SUM(cast(a."FLIGHTS" as decimal(20, 2)))))) as "CI Upper",
AVG(cast(a."ARR_DELAY" as decimal(20, 2))) - (1.96 * (STDDEV(cast(a."ARR_DELAY" as decimal(20, 2))) / sqrt(SUM(cast(a."FLIGHTS" as decimal(20, 2)))))) as "CI Lower"

into public.otp_carrier_monthly_average_ci

from public.t_ontime_reporting_2023 a
left join public.months_lookup b
on cast(a."MONTH" as real) = b.month

left join carriers c
on a."OP_UNIQUE_CARRIER"  = c.unique_carrier

where a."CANCELLED" = 0
and a."ORIGIN" <> a."DEST"
and a."ARR_DELAY" is not null

group by a."OP_UNIQUE_CARRIER" , c.unique_carrier_name, cast(a."MONTH" as real), b.month_name_short

order by c.unique_carrier_name asc, cast(a."MONTH" as real) asc;

select * from public.otp_carrier_monthly_average_ci

-- All Carriers View --
-- Delay By Categorization --
with all_otp as (
select *, 

case 
	when cast("ARR_DELAY" as decimal(20, 2)) < -10.0 then 'Early > 10 Mins'
	when cast("ARR_DELAY" as decimal(20, 2)) >= -10.0 and cast("ARR_DELAY" as decimal(20, 2)) < 0.00 then 'Early < 10 Mins'
	when cast("ARR_DELAY" as decimal(20, 2)) >= 0.00 and cast("ARR_DELAY" as decimal(20, 2)) < 10.00 then 'Late < 10 Mins'
	when cast("ARR_DELAY" as decimal(20, 2)) >= 10.00 then 'Late > 10 Mins'
end as "ARR_DELAY_CLASS"


from public.t_ontime_reporting_2023
where "CANCELLED" = 0
and "ORIGIN" <> "DEST"
and "ARR_DELAY" is not null)


select
cast(a."MONTH" as real) as "Month Number",
b.month_name_short as "Month Name",
a."ARR_DELAY_CLASS" as "Arrival Delay Classification",

SUM(cast(a."FLIGHTS" as decimal(20, 2))) as "Total Flights"

into public.otp_total_monthly_delay_class

from all_otp a

left join public.months_lookup b
on cast(a."MONTH" as real) = b.month

where a."CANCELLED" = 0
and a."ORIGIN" <> a."DEST"
and a."ARR_DELAY" is not null

group by cast(a."MONTH" as real), b.month_name_short, a."ARR_DELAY_CLASS"

order by cast(a."MONTH" as real) asc, a."ARR_DELAY_CLASS" asc;

select * from public.otp_total_monthly_delay_class


select
cast(a."MONTH" as real) as "Month Number",
b.month_name_short as "Month Name",
AVG(cast(a."ARR_DELAY" as decimal(20, 2))) as "Average Delay",
SUM(cast(a."FLIGHTS" as decimal(20, 2))) as "Total Flights", 

STDDEV(cast(a."ARR_DELAY" as decimal(20, 2))) as "Delay Standard Deviation",

AVG(cast(a."ARR_DELAY" as decimal(20, 2))) + (1.96 * (STDDEV(cast(a."ARR_DELAY" as decimal(20, 2))) / sqrt(SUM(cast(a."FLIGHTS" as decimal(20, 2)))))) as "CI Upper",
AVG(cast(a."ARR_DELAY" as decimal(20, 2))) - (1.96 * (STDDEV(cast(a."ARR_DELAY" as decimal(20, 2))) / sqrt(SUM(cast(a."FLIGHTS" as decimal(20, 2)))))) as "CI Lower"

into public.otp_total_monthly_average_ci

from public.t_ontime_reporting_2023 a
left join public.months_lookup b
on cast(a."MONTH" as real) = b.month

where a."CANCELLED" = 0
and a."ORIGIN" <> a."DEST"
and a."ARR_DELAY" is not null

group by cast(a."MONTH" as real), b.month_name_short

order by cast(a."MONTH" as real) asc;

select * from public.otp_total_monthly_average_ci



select * from public.otp_carrier_by_month_summary_delay

-- drop table if exists public.otp_carrier_by_month_summary_delay

with carriers as (

select distinct unique_carrier, unique_carrier_name
from public.t100_segment_all_carrier_2023)

select a."OP_UNIQUE_CARRIER" as "Unique Carrier Code",
c.unique_carrier_name as "Unique Carrier Name",
cast(a."MONTH" as real) as "Month Number",
b.month_name_short as "Month Name",
AVG(cast(a."ARR_DELAY" as decimal(20, 2))) as "Average Delay",
SUM(cast(a."FLIGHTS" as decimal(20, 2))) as "Total Flights",
SUM(case when cast(a."ARR_DELAY" as decimal(20, 2)) >= 10.0 then 1 else 0 end) as "Total Late > 10 Mins",
SUM(case when cast(a."ARR_DELAY" as decimal(20, 2)) >= 0.0 and cast(a."ARR_DELAY" as decimal(20, 2)) < 10.0 then 1 else 0 end) as "Total Late < 10 Mins",
SUM(case when cast(a."ARR_DELAY" as decimal(20, 2)) >= -10.0 and cast(a."ARR_DELAY" as decimal(20, 2)) < 0.0 then 1 else 0 end) as "Total Early < 10 Mins",
SUM(case when cast(a."ARR_DELAY" as decimal(20, 2)) < -10.0 then 1 else 0 end) as "Total Early > 10 Mins"

-- Section to include breakdown of late and on time flights --

-- into public.otp_carrier_by_month_summary_delay


from public.t_ontime_reporting_2023 a

left join public.months_lookup b
on cast(a."MONTH" as real) = b.month

left join carriers c
on a."OP_UNIQUE_CARRIER" = c.unique_carrier

where a."CANCELLED" = 0
and a."ORIGIN" <> a."DEST"
and a."ARR_DELAY" is not null

group by a."OP_UNIQUE_CARRIER", c.unique_carrier_name, cast(a."MONTH" as real), b.month_name_short

order by c.unique_carrier_name asc, cast(a."MONTH" as real) asc;





select * from public.otp_carrier_monthly_delay_class
order by "Unique Carrier Name" asc, cast("Month Number" as real) asc;

-- Selected Carrier Query --
with a as (

select "Unique Carrier Code", "Unique Carrier Name", "Month Number", "Month Name", 
SUM(case when "Arrival Delay Classification" like 'Late %' then cast("Total Flights" as real) else 0 end) as "Total Late Flights",
SUM(cast("Total Flights" as real)) as "Total Flights"
from public.otp_carrier_monthly_delay_class

where "Unique Carrier Name" = 'Alaska Airlines Inc.'

group by "Unique Carrier Code", "Unique Carrier Name", "Month Number", "Month Name")

select a.*, (a."Total Late Flights" * 1.00) / (a."Total Flights" * 1.00) as "Late Flight Percentage"
from a
order by "Unique Carrier Name", cast("Month Number" as real) asc;

-- All Carriers Query --
with a as (

select "Month Number", "Month Name", 
SUM(case when "Arrival Delay Classification" like 'Late %' then cast("Total Flights" as real) else 0 end) as "Total Late Flights",
SUM(cast("Total Flights" as real)) as "Total Flights"
from public.otp_carrier_monthly_delay_class
group by "Month Number", "Month Name")

select 'All Carriers' as "Unique Carrier Name", a.*, (a."Total Late Flights" * 1.00) / (a."Total Flights" * 1.00) as "Late Flight Percentage"
from a
order by cast("Month Number" as real) asc;

select * from a
order by "Unique Carrier Name", cast("Month Number" as real) asc


select * from public.otp_carrier_monthly_average_ci
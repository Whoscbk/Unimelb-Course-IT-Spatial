-- Part 1 Pattern Analysis of the check-ins' location and user's category(tourists or locals) in melbourne
-- Step 1: Analysis of location of first-time check-in
-- Find out where each user checked in for the first time.
WITH first_checkin AS
(
		SELECT temp.uid, temp.geom
		FROM
			(SELECT uid, 
					first_value(geom) over(PARTITION BY uid ORDER BY date, time) AS geom
			FROM spatial.checkins_melbourne) AS temp
		GROUP BY temp.uid, temp.geom
)
-- Utilize the cluster algorithm to identify the pattern
SELECT a.kmean_id, count(*), ST_MinimumBoundingCircle(ST_Collect(a.geom)) as clusters_first_checkin
FROM
(
    SELECT ST_ClusterKMeans(geom, 50) OVER() AS kmean_id, ST_Centroid(geom) as geom
    FROM first_checkin
) a
GROUP BY a.kmean_id
ORDER BY count(*) DESC
LIMIT 2;
-- Step 2: Analysis of location of last-time check-in
-- Find out where each user checked in for the last time.
WITH last_checkin AS
(
		SELECT temp.uid, temp.geom
		FROM
			(SELECT uid, 
					first_value(geom) over(PARTITION BY uid ORDER BY date, time DESC) AS geom
			FROM spatial.checkins_melbourne) AS temp
		GROUP BY temp.uid, temp.geom
)
-- Utilize the cluster algorithm to identify the pattern
SELECT a.kmean_id, count(*), ST_MinimumBoundingCircle(ST_Collect(a.geom)) as clusters_last_checkin
FROM
(
    SELECT ST_ClusterKMeans(geom, 50) OVER() AS kmean_id, ST_Centroid(geom) as geom
    FROM last_checkin
) a
GROUP BY a.kmean_id
ORDER BY count(*) DESC
LIMIT 2;

-- Part 2 Distribution Analysis of the check-ins in different months and time in melbourne
-- Summary the counts of user check-in in each month and analyze the change
WITH date_spilt AS
	(
	  SELECT b.poi,
			   (
				CASE
				WHEN b.date >= '2009-09-01' and b.date < '2009-10-01' THEN 'a.SEP/2009'
				WHEN b.date >= '2009-10-01' and b.date < '2009-11-01' THEN 'b.OCT/2009'
				WHEN b.date >= '2009-11-01' and b.date < '2009-12-01' THEN 'c.NOV/2009'
				WHEN b.date >= '2009-12-01' and b.date < '2010-01-01' THEN 'd.DEC/2009'
				WHEN b.date >= '2010-01-01' and b.date < '2010-02-01' THEN 'e.JAN/2010'
				WHEN b.date >= '2010-02-01' and b.date < '2010-03-01' THEN 'f.FEB/2010'
				WHEN b.date >= '2010-03-01' and b.date < '2010-04-01' THEN 'g.MAR/2010'
				WHEN b.date >= '2010-04-01' and b.date < '2010-05-01' THEN 'h.APR/2010'
				WHEN b.date >= '2010-05-01' and b.date < '2010-06-01' THEN 'i.MAY/2010'
				WHEN b.date >= '2010-06-01' and b.date < '2010-07-01' THEN 'j.JUN/2010'
				WHEN b.date >= '2010-07-01' and b.date < '2010-08-01' THEN 'k.JUL/2010'
				WHEN b.date >= '2010-08-01' and b.date < '2010-09-01' THEN 'm.AUG/2010'
				WHEN b.date >= '2010-09-01' and b.date < '2010-10-01' THEN 'n.SEP/2010'
				WHEN b.date >= '2010-10-01' and b.date < '2010-11-01' THEN 'o.OCT/2010'
				ELSE 'z.none'
				END
			   ) AS date
		FROM spatial.checkins_melbourne AS b
		ORDER BY b.date
	)
SELECT date, COUNT(*)
FROM date_spilt
GROUP BY date
ORDER BY date;
-- Summary the counts of user check-in in different time and analyze the change	
WITH time_spilt AS
	(
	  SELECT b.poi,
			   (
				CASE
				WHEN b.time >= '06:00:00' and b.time < '12:00:00' THEN 'a.Morning(6-12am)'
				WHEN b.time >= '12:00:00' and b.time < '18:00:00' THEN 'b.Afternoon(12-18pm)'
				WHEN b.time >= '18:00:00' and b.time < '24:00:00' THEN 'c.Night(18-24pm)'
				WHEN b.time >= '00:00:00' and b.time < '06:00:00' THEN 'd.Early morning(0-6am)'
				ELSE 'z.none'
				END
			   ) AS time
		FROM spatial.checkins_melbourne AS b
		ORDER BY b.time
	)
SELECT time, COUNT(*)
FROM time_spilt
GROUP BY time
ORDER BY time;


-- Part 3 Relation Analysis of the friend network and the spatial location of check-ins
-- Step 1: Data preparing
-- Create a table to store the user id of checkins_melbourne
DROP TABLE IF EXISTS user_melbourne;
CREATE TABLE user_melbourne AS
(SELECT DISTINCT uid FROM spatial.checkins_melbourne);
-- create a edges table for the friends network
DROP TABLE IF EXISTS friends_edges;
CREATE TABLE friends_edges
(
	id serial PRIMARY KEY NOT NULL,
	user_id int,
	friend_id int
);
INSERT INTO friends_edges(user_id, friend_id)
SELECT aid, bid
FROM spatial.friends;
-- Create test_data table to store the tested data
-- Create test_result table to store the correlation
DROP TABLE IF EXISTS test_data;
DROP TABLE IF EXISTS test_result;
CREATE TABLE test_data
(
	uid_a int,
	uid_b int,
	friend_distance int,
	spatial_distance int
);
CREATE TABLE test_result
(
	id serial PRIMARY KEY NOT NULL,
	correlation float 
);
-- Step 2: Data query and process
-- Create a function to query the target datas and insert them into the table created above
CREATE OR REPLACE function insert_testdata(x int)
returns void as $$
declare i int;
	begin
	i:=1;
	for i in 1..x loop
	-- create a friends network
	-- randomly select the tested samples
	-- compute the friend distance between the samples
	WITH friends_network AS
	(
		SELECT a.uid AS user_a, b.uid AS user_b, CAST(c.agg_cost as int) AS friend_distance
		FROM (SELECT * FROM user_melbourne ORDER BY RANDOM() LIMIT 1) AS a, 
			 (SELECT * FROM user_melbourne ORDER BY RANDOM() LIMIT 1) AS b,
			 pgr_dijkstraCost
			 (
				 'SELECT id, user_id as source, friend_id as target, 1 as cost
				  FROM friends_edges',
				 a.uid, b.uid, directed:= false
			 ) AS c
		WHERE a.uid <> b.uid
	)
	-- compute the spatial distance between the location of checkins for each samples
	-- and insert the data into teat_data table
	INSERT INTO test_data(uid_a, uid_b, friend_distance, spatial_distance)
	SELECT temp.uid_a, temp.uid_b, fn.friend_distance, 
		   -- Sum all the mimimum distance of user's checkin and get the average as the final spatial distance.
		   CAST(SUM(temp.distance)/COUNT(*) as int) AS spatial_distance
	FROM(
		SELECT t1.uid AS uid_a, t2.uid AS uid_b,
				-- For each user's checkin get the minimum distance among the friend's chenkins
				MIN(ST_Distance(t1.geom, t2.geom, true)) AS distance
		FROM (friends_network as f
				JOIN spatial.checkins_melbourne AS b
				ON f.user_a = b.uid) AS t1,
			 (friends_network as f
				JOIN spatial.checkins_melbourne AS b
				ON f.user_b = b.uid) AS t2
		GROUP BY t1.uid, t2.uid, t1.poi
		) AS temp,
		friends_network as fn
	WHERE temp.uid_a = fn.user_a AND
		  temp.uid_b = fn.user_b
	GROUP BY temp.uid_a, temp.uid_b, fn.friend_distance;
	i=i+1;
	end loop;
	-- Compute the correlation of tested data
	-- Insert the result into test_result table
	INSERT INTO test_result(correlation)
	SELECT corr(friend_distance, spatial_distance) FROM test_data;
	end;
$$ LANGUAGE plpgsql;
-- Carry out the function above
-- Inset 10 records each time
-- Repeat to get different data results.
SELECT insert_testdata(10)
-- Check the tested data
SELECT * FROM test_data;
-- Check the change of correlation for the tested data to find the final size of tested data
SELECT * FROM test_result;
-- Step 3: Export the teated data to python for fuether research
-- Drop all the table and complete this part
DROP TABLE IF EXISTS user_melbourne;
DROP TABLE IF EXISTS friends_edges;
DROP TABLE IF EXISTS test_data;
DROP TABLE IF EXISTS test_result;

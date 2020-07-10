-- Q1
SELECT 'Car' as mode_of_transport, SUM(c.cost) AS minimum_distance_m, 
		(CASE WHEN COUNT(c.edge) = 0 THEN null ELSE (COUNT(c.edge)-1) END) AS num_of_edges
FROM pgr_dijkstra('SELECT id, source, target, 
				   (CASE WHEN car = 0 then -1 ELSE ST_Length(geom,true) END) AS cost,
				   (CASE WHEN car_rev = 0 then -1 ELSE ST_Length(geom,true) END) AS reverse_cost
				   FROM spatial.unimelb_edges',
				   1335, 1811, directed:= true) AS c
UNION ALL
SELECT 'Bike' as mode_of_transport, SUM(b.cost) AS minimum_distance_m,
		(CASE WHEN COUNT(b.edge) = 0 THEN null ELSE (COUNT(b.edge)-1) END) AS num_of_edges
FROM pgr_dijkstra('SELECT id, source, target, 
				   (CASE WHEN bike = 0 then -1 ELSE ST_Length(geom,true) END) AS cost
				   FROM spatial.unimelb_edges',
				   1335, 1811, directed:= false) AS b
UNION ALL
SELECT 'Foot' as mode_of_transport, SUM(f.cost) AS minimum_distance_m,
		(CASE WHEN COUNT(f.edge) = 0 THEN null ELSE (COUNT(f.edge)-1) END) AS num_of_edges
FROM pgr_dijkstra('SELECT id, source, target, 
				   (CASE WHEN foot = 0 then -1 ELSE ST_Length(geom,true) END) AS cost
				   FROM spatial.unimelb_edges',
				   1335, 1811, directed:= false) AS f;
-- Q2
SELECT node AS destination_node, agg_cost AS distance_m
FROM pgr_drivingDistance('SELECT id, source, target, 
				   		(CASE WHEN foot = 0 then -1 ELSE ST_Length(geom,true) END) AS cost
				   		FROM spatial.unimelb_edges',
				   		550, 3000, directed:= false)
WHERE agg_cost >= 2400
ORDER BY agg_cost DESC;
-- Q3
SELECT COUNT(*)	 AS total_count
FROM (SELECT a.node, (a.agg_cost + b.agg_cost) AS total_cost
	  FROM pgr_drivingDistance('SELECT id, source, target, 
							   (CASE WHEN foot = 0 then -1 ELSE ST_Length(geom,true) END) AS cost
							   FROM spatial.unimelb_edges',
							   1811, 5*60*(10.0/3.6), directed:= false) AS a,
		   pgr_dijkstraCost('SELECT id, source, target, 
						     (CASE WHEN foot = 0 then -1 ELSE ST_Length(geom,true) END) AS cost 
						     FROM spatial.unimelb_edges', 
						     ARRAY(SELECT node 
								   FROM pgr_drivingDistance('SELECT id, source, target, 
									    (CASE WHEN foot = 0 then -1 ELSE ST_Length(geom,true) END) AS cost
									     FROM spatial.unimelb_edges',
									     1811, 5*60*(10.0/3.6), directed:= false)
								   WHERE node <> 1811), 
						    1811,false) AS b
	  WHERE a.node = b.start_vid) AS result
WHERE result.total_cost <= 5*60*(10.0/3.6);
-- Q4
SELECT CONCAT((CAST(ABS(onward.time-return.time) as int)/60), 
			  ' : ', 
			  (CAST(ABS(onward.time-return.time) as int)%60))
	   AS difference_mm_ss
FROM (SELECT SUM(cost)/(30.0/3.6)	AS time  
	  FROM pgr_dijkstra('SELECT id, source, target, 
					    (CASE WHEN car = 0 then -1 ELSE ST_Length(geom,true) END) AS cost,
					    (CASE WHEN car_rev = 0 then -1 ELSE ST_Length(geom,true) END) AS reverse_cost
					    FROM spatial.unimelb_edges',
					    252, 857, directed:= true)) AS onward,
	 (SELECT SUM(cost)/(30.0/3.6)	AS time  
	  FROM pgr_dijkstra('SELECT id, source, target, 
					    (CASE WHEN car = 0 then -1 ELSE ST_Length(geom,true) END) AS cost,
					    (CASE WHEN car_rev = 0 then -1 ELSE ST_Length(geom,true) END) AS reverse_cost
					    FROM spatial.unimelb_edges',
					    857, 252, directed:= true)) AS return;
-- Q5
SELECT COUNT(a.id) AS num_disconnected_nodes
FROM spatial.unimelb_nodes AS a
WHERE a.id NOT IN (SELECT node
				   FROM  pgr_drivingDistance('SELECT id, source, target, 
											  0 AS cost
				   							  FROM spatial.unimelb_edges',
				   							  34, 1 , directed:= false));
-- Q6
SELECT CONCAT('(', result.signage_node, ',', result.deadend_node, ')') AS signageNode_deadendNode
FROM (
		SELECT source AS signage_node, 
			   target AS deadend_node
		FROM spatial.unimelb_edges 
		WHERE car <> 0
			  AND
			  source between 1900 and 2000
			  AND
			  target between 1900 and 2000
			  AND
			  target NOT IN (SELECT source
							   FROM spatial.unimelb_edges)
			  AND
			  target IN (SELECT target
							FROM spatial.unimelb_edges 
							GROUP BY target
							HAVING COUNT(target) = 1)
		UNION ALL
		SELECT target AS signage_node, 
			   source AS deadend_node
		FROM spatial.unimelb_edges
		WHERE car <> 0 
			  AND
			  source between 1900 and 2000
			  AND
			  target between 1900 and 2000
			  AND
			  source NOT IN (SELECT target
							   FROM spatial.unimelb_edges)
			  AND
			  source IN (SELECT source
							FROM spatial.unimelb_edges
							WHERE car <> 0 
							GROUP BY source
							HAVING COUNT(source) = 1)
	) AS result;
-- Q7
SELECT COUNT(*) AS total_road_segments, 
	   (0.001*SUM(ST_Length(geom, true))) AS total_length_km
FROM spatial.unimelb_edges
WHERE id IN(SELECT edge 
			FROM pgr_bridges('SELECT id, source, target, 
						  	 (CASE WHEN car = 0 then -1 ELSE ST_Length(geom,true) END) AS cost
						  	 FROM spatial.unimelb_edges'));
-- Q8
SELECT ST_Area(ST_Buffer(ST_Union(ARRAY[path_1.line,path_2.line,path_3.line])::geography,
				 20, 'endcap=round join=round'), true)
	   AS contaminated_area_m2
FROM (SELECT ST_Union(a.geom) AS line
	  FROM  spatial.unimelb_edges AS a
		    JOIN
		    pgr_dijkstra('SELECT id, source, target, 
					     (CASE WHEN car = 0 then -1 ELSE ST_Length(geom,true) END) AS cost,
					     (CASE WHEN car_rev = 0 then -1 ELSE ST_Length(geom,true) END) AS reverse_cost
					     FROM spatial.unimelb_edges',
					     586, 655, directed:= true) AS b
		    ON a.id = b.edge
		    WHERE b.edge <> -1
	  ) AS path_1,
	 (SELECT ST_Union(a.geom) AS line
	  FROM  spatial.unimelb_edges AS a
		    JOIN
		    pgr_dijkstra('SELECT id, source, target, 
					     (CASE WHEN car = 0 then -1 ELSE ST_Length(geom,true) END) AS cost,
					     (CASE WHEN car_rev = 0 then -1 ELSE ST_Length(geom,true) END) AS reverse_cost
					     FROM spatial.unimelb_edges',
					     655, 1388, directed:= true) AS b
		    ON a.id = b.edge
		    WHERE b.edge <> -1
	  ) AS path_2,
	 (SELECT ST_Union(a.geom) AS line
	  FROM  spatial.unimelb_edges AS a
		    JOIN
		    pgr_dijkstra('SELECT id, source, target, 
					     (CASE WHEN car = 0 then -1 ELSE ST_Length(geom,true) END) AS cost,
					     (CASE WHEN car_rev = 0 then -1 ELSE ST_Length(geom,true) END) AS reverse_cost
					     FROM spatial.unimelb_edges',
					     1388, 1870, directed:= true) AS b
		    ON a.id = b.edge
		    WHERE b.edge <> -1
	  ) AS path_3;
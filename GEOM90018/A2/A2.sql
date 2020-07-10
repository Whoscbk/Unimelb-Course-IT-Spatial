-- Q1
SELECT c.cntry_name AS country_with_most_neighbouring_countries, n.cntry_name AS neigbouring_country, 
(0.001 * ST_Length(ST_Intersection(c.geom, n.geom), true)) AS length_shared_border_km
From spatial.world_countries as c JOIN spatial.world_countries as n
ON ST_Touches(c.geom, n.geom)
WHERE c.cntry_name = (SELECT a.cntry_name
					  From spatial.world_countries as a JOIN spatial.world_countries as b
					  ON ST_Touches(a.geom, b.geom)
					  WHERE a.cntry_name <> b.cntry_name
					  GROUP BY a.cntry_name
					  HAVING COUNT(*) = (SELECT MAX(temp.num)
										 From (SELECT COUNT(*) as num
											   FROM spatial.world_countries as c JOIN spatial.world_countries as d
											   ON ST_Touches(c.geom, d.geom)
											   WHERE c.cntry_name <> d.cntry_name
											   GROUP BY c.cntry_name) AS temp)) 
ORDER BY length_shared_border_km DESC;
-- Q2
SELECT n.cntry_name AS country_name,
CAST(n.pop_cntry/(0.000001 * ST_Area(n.geom, true)) AS Float) AS pop_density_km2
From spatial.world_countries as c JOIN spatial.world_countries as n
ON ST_Touches(c.geom, n.geom)
WHERE c.cntry_name = 'Austria'
AND ST_Length(ST_Intersection(c.geom, n.geom), true) = 
	(SELECT MAX(ST_Length(ST_Intersection(c.geom, n.geom), true))
	 From spatial.world_countries as c JOIN spatial.world_countries as n
	 ON ST_Touches(c.geom, n.geom)
	 WHERE c.cntry_name = 'Austria'
	 AND ST_Length(ST_Intersection(c.geom, n.geom), true) < 
	 	(SELECT MAX(ST_Length(ST_Intersection(a.geom, b.geom), true))
		 From spatial.world_countries as a JOIN spatial.world_countries as b
		 ON ST_Touches(a.geom, b.geom)
		 WHERE a.cntry_name = 'Austria'));
-- Q3
SELECT '1-North frigid zone' as zone_name, 
		CONCAT((north_frigid.area / total.area)*100, '%') AS landmass_percentage,
		north_frigid.num AS num_of_countries
FROM (SELECT SUM(ST_Area((geom), true)) as area
	  FROM spatial.world_countries) 
	  AS total,
	 (SELECT SUM(ST_Area(ST_Intersection(a.geom, nf.zone), true)) AS area, COUNT(*) AS num
	  FROM spatial.world_countries AS a 
	  JOIN (SELECT ST_MakePolygon(ST_MakeLine(ARRAY[ST_SetSRID(ST_MakePoint(-180, 66.5), 4326),
													ST_SetSRID(ST_MakePoint(180, 66.5), 4326),
													ST_SetSRID(ST_MakePoint(180, 90), 4326),
													ST_SetSRID(ST_MakePoint(-180, 90), 4326),
													ST_SetSRID(ST_MakePoint(-180, 66.5), 4326)])) AS zone) AS nf
	  ON ST_Intersects(a.geom, nf.zone)) 
	  AS north_frigid
UNION
SELECT '2-North temperate zone' as zone_name,
		CONCAT((north_temperate.area / total.area)*100, '%') AS landmass_percentage,
		north_temperate.num AS num_of_countries
FROM (SELECT SUM(ST_Area((geom), true)) as area
	  FROM spatial.world_countries) 
	  AS total,
	 (SELECT SUM(ST_Area(ST_Intersection(a.geom, nt.zone), true)) AS area, COUNT(*) AS num
	  FROM spatial.world_countries AS a 
	  JOIN (SELECT ST_MakePolygon(ST_MakeLine(ARRAY[ST_SetSRID(ST_MakePoint(-180, 23.5), 4326), 
													ST_SetSRID(ST_MakePoint(180, 23.5), 4326),
													ST_SetSRID(ST_MakePoint(180, 66.5), 4326), 
													ST_SetSRID(ST_MakePoint(-180, 66.5), 4326),
													ST_SetSRID(ST_MakePoint(-180, 23.5), 4326)])) AS zone) AS nt
	  ON ST_Intersects(a.geom, nt.zone)) 
	  AS north_temperate
UNION
SELECT '3-Torrid zone' as zone_name,
		CONCAT((torrid.area / total.area)*100, '%') AS landmass_percentage,
		torrid.num AS num_of_countries
FROM (SELECT SUM(ST_Area((geom), true)) as area
	  FROM spatial.world_countries) 
	  AS total,
	 (SELECT SUM(ST_Area(ST_Intersection(a.geom, t.zone), true)) AS area, COUNT(*) AS num
	  FROM spatial.world_countries AS a
	  JOIN (SELECT ST_MakePolygon(ST_MakeLine(ARRAY[ST_SetSRID(ST_MakePoint(-180, -23.5), 4326), 
													ST_SetSRID(ST_MakePoint(180, -23.5), 4326),
													ST_SetSRID(ST_MakePoint(180, 23.5), 4326), 
													ST_SetSRID(ST_MakePoint(-180, 23.5), 4326),
													ST_SetSRID(ST_MakePoint(-180, -23.5), 4326)])) AS zone) AS t
	  ON ST_Intersects(a.geom, t.zone)) 
	  AS torrid
UNION
SELECT '4-South temperate zone' as zone_name,
		CONCAT((south_temperate.area / total.area)*100, '%') AS landmass_percentage,
		south_temperate.num AS num_of_countries
FROM (SELECT SUM(ST_Area((geom), true)) as area
	  FROM spatial.world_countries) 
	  AS total,
	 (SELECT SUM(ST_Area(ST_Intersection(a.geom, st.zone), true)) AS area, COUNT(*) AS num
	  FROM spatial.world_countries AS a
	  JOIN (SELECT ST_MakePolygon(ST_MakeLine(ARRAY[ST_SetSRID(ST_MakePoint(-180, -66.5), 4326), 
													ST_SetSRID(ST_MakePoint(180, -66.5), 4326),
													ST_SetSRID(ST_MakePoint(180, -23.5), 4326), 
													ST_SetSRID(ST_MakePoint(-180, -23.5), 4326),
													ST_SetSRID(ST_MakePoint(-180, -66.5), 4326)])) AS zone) AS st
	  ON ST_Intersects(a.geom, st.zone)) 
	  AS south_temperate
UNION
SELECT '5-South frigid zone' as zone_name,
		CONCAT((south_frigid.area / total.area)*100, '%') AS landmass_percentage,
		south_frigid.num AS num_of_countries
FROM (SELECT SUM(ST_Area((geom), true)) as area
	  FROM spatial.world_countries) 
	  AS total,
	 (SELECT SUM(ST_Area(ST_Intersection(a.geom, sf.zone), true)) AS area, COUNT(*) AS num
	  FROM spatial.world_countries AS a
	  JOIN (SELECT ST_MakePolygon(ST_MakeLine(ARRAY[ST_SetSRID(ST_MakePoint(-180, -90), 4326), 
													ST_SetSRID(ST_MakePoint(180, -90), 4326),
													ST_SetSRID(ST_MakePoint(180, -66.5), 4326), 
													ST_SetSRID(ST_MakePoint(-180, -66.5), 4326),
													ST_SetSRID(ST_MakePoint(-180, -90), 4326)])) AS zone) AS sf
	  ON ST_Intersects(a.geom, sf.zone)) 
	  AS south_frigid
ORDER BY zone_name;
-- Q4
SELECT a.state AS least_populated_state
FROM spatial.us_states AS a
JOIN spatial.us_interstates AS b
ON ST_Intersects(a.geom, b.geom)
WHERE b.interstate = 'I80'
ORDER BY (a.totpop/(0.000001*ST_Area(a.geom, true)))
LIMIT 3;
-- Q5
SELECT t1.num AS zero_dimensional, t2.num AS one_dimensional
FROM (SELECT COUNT(*) AS num
	  FROM spatial.us_states AS a JOIN spatial.us_states AS b
	  ON ST_Touches(a.geom, b.geom)
	  WHERE a.id < b.id
	  AND (GeometryType(ST_Intersection(ST_MakeValid(a.geom), ST_MakeValid(b.geom))) = 'POINT'
		   OR GeometryType(ST_Intersection(ST_MakeValid(a.geom), ST_MakeValid(b.geom))) = 'MULTIPOINT')) AS t1, 
	 (SELECT COUNT(*) AS num
	  FROM spatial.us_states AS c JOIN spatial.us_states AS d
	  ON ST_Touches(c.geom, d.geom)
	  WHERE c.id < d.id
	  AND (GeometryType(ST_Intersection(ST_MakeValid(c.geom), ST_MakeValid(d.geom))) = 'LINESTRING'
		   OR GeometryType(ST_Intersection(ST_MakeValid(c.geom), ST_MakeValid(d.geom))) = 'MULTILINESTRING')) AS t2;
-- Q6
SELECT result.interstate_pair, result.shared_segment_km
FROM (SELECT CONCAT(a.interstate, ' - ', b.interstate) AS interstate_pair,
	  CAST((0.001 * ST_Length(ST_Intersection(a.geom, b.geom), true)) As DECIMAL(10,2)) AS shared_segment_km
	  FROM spatial.us_interstates AS a JOIN spatial.us_interstates AS b 
	  ON ST_Intersects(a.geom, b.geom)
	  WHERE a.interstate NOT LIKE '%/%' AND b.interstate NOT LIKE '%/%' 
	  AND a.id < b.id
	  ORDER BY shared_segment_km DESC
	  Limit 3) AS result
ORDER BY result.interstate_pair;
-- Q7
SELECT t.total_buildings, o.num_overlap_building, type.num AS num_of_types, s.minimum_area, s.maximum_area, s.average_area
FROM (SELECT COUNT(a.osm_id) AS total_buildings
	  FROM spatial.melbourne_osm_polygon AS a
	  WHERE a.building NOTNULL) 
	  AS t,
	  (SELECT COUNT(temp.overlap_building) AS num_overlap_building
	   FROM (SELECT DISTINCT b.osm_id as overlap_building
			 FROM spatial.melbourne_osm_polygon AS b JOIN spatial.melbourne_osm_polygon AS c
			 ON (ST_Equals(b.way, c.way) OR ST_Contains(b.way, c.way) 
				 OR ST_Within(b.way, c.way) OR ST_Overlaps(b.way, c.way))
			 WHERE b.building NOTNULL AND c.building NOTNULL
			 AND b.osm_id <> c.osm_id) AS temp) 
	  AS o,
	 (SELECT COUNT(p.tp) AS num
	  FROM (SELECT DISTINCT a.building as tp
			FROM spatial.melbourne_osm_polygon AS a
			WHERE a.building NOTNULL) AS p)
	  AS type,
	 (SELECT MIN(ST_Area(d.way)) AS minimum_area, MAX(ST_Area(d.way)) AS maximum_area, AVG(ST_Area(d.way)) AS average_area
	  FROM spatial.melbourne_osm_polygon AS d
	  WHERE d.building NOTNULL) 
	  AS s;
-- Q8
SELECT a.cntry_name
From spatial.world_countries as a JOIN spatial.world_countries as b
ON ST_Touches(a.geom, b.geom)
WHERE a.cntry_name <> b.cntry_name
GROUP BY a.cntry_name
HAVING COUNT(*) = 1
ORDER BY a.cntry_name ASC;
INSERT INTO review (id,  title, comment, rating, user_id, movie_id, created_at)
SELECT
    lower(hex(randomblob(16))) ,'Review for Movie ' || m.title,
    (SELECT
        CASE CAST(RANDOM() AS INTEGER) % 30 + 1  -- Generate random number 1-30
            WHEN 1 THEN 'Excellent movie!'  
            WHEN 2 THEN 'A must-see!'  
            WHEN 3 THEN 'Enjoyed it very much.'  
            WHEN 4 THEN 'Highly recommended!'  
            WHEN 5 THEN 'A cinematic masterpiece.'  
            WHEN 6 THEN 'Great acting and story.'  
            WHEN 7 THEN 'A visual delight!'  
            WHEN 8 THEN 'Kept me engaged throughout.'  
            WHEN 9 THEN 'Loved every moment!'  
            WHEN 10 THEN 'A thrilling experience.'  
            WHEN 11 THEN 'Emotional and powerful.'  
            WHEN 12 THEN 'A bit slow but worth watching.'  
            WHEN 13 THEN 'Fantastic direction and cinematography.'  
            WHEN 14 THEN 'A great blend of action and drama.'  
            WHEN 15 THEN 'Memorable performances.'  
            WHEN 16 THEN 'A fresh take on the genre.'  
            WHEN 17 THEN 'The soundtrack was amazing!'  
            WHEN 18 THEN 'Beautifully crafted film.'  
            WHEN 19 THEN 'A rollercoaster of emotions.'  
            WHEN 20 THEN 'Kept me on the edge of my seat.'  
            WHEN 21 THEN 'A perfect family movie.'  
            WHEN 22 THEN 'Unexpected twists and turns!'  
            WHEN 23 THEN 'A well-written script.'  
            WHEN 24 THEN 'A bit predictable but entertaining.'  
            WHEN 25 THEN 'A truly immersive experience.'  
            WHEN 26 THEN 'Will watch it again!'  
            WHEN 27 THEN 'A nostalgic and heartwarming film.'  
            WHEN 28 THEN 'Outstanding cinematography and visuals.'  
            WHEN 29 THEN 'A masterpiece in storytelling.'  
            WHEN 30 THEN 'A captivating story.' 
            ELSE 'A default comment' || m.title  -- In case you have fewer than 30 comments
        END),
    (ABS(RANDOM()) % 6) + 5,  -- Random rating 1-5
    u.id,
    m.id,
	DATETIME('now', '-' || ((ABS(RANDOM()) % 6) + 5) || ' days')
FROM
    (SELECT id FROM user ORDER BY RANDOM() LIMIT 80) AS u  -- Changed to 80
CROSS JOIN
    (SELECT id, title FROM movie ORDER BY RANDOM() LIMIT 800) AS m;
	
	
	
	
	
	

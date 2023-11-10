SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

6

SELECT * from ripeness;
SELECT * from users;
SELECT * from palm;

SELECT 
            p.palmname,
            p.ripeness_id,
            r.ripeness_level,
            p.oilContent
     FROM
            palm p
        JOIN
            ripeness r ON p.ripeness_id = r.id;
			
INSERT INTO palm (palmName, ripeness_id, oilContent)
VALUES ('palm_005', 3, 68.99);

DELETE FROM palm WHERE palmName = 'palm_005';

ALTER TABLE palm
RENAME COLUMN name TO palmName;

DELETE FROM palm

ALTER TABLE palm
ADD COLUMN timeCaptured TIMESTAMP,
ADD COLUMN img BYTEA;

CREATE TABLE users(
	user_id SERIAL PRIMARY KEY,
	username VARCHAR(50) UNIQUE,
	email VARCHAR(255) UNIQUE,
	user_password VARCHAR(255),
	firstname VARCHAR(50),
	lastname VARCHAR(50),
	date_created TIMESTAMP,
	last_login TIMESTAMP
);

CREATE TABLE new_palm (
	id SERIAL PRIMARY KEY,
	img_name VARCHAR(50),
	ripeness_id INTEGER REFERENCES ripeness(id),
	oil_content REAL,
	img BYTEA,
	time_captured TIMESTAMP,	
	last_edit TIMESTAMP,
	captured_by INTEGER REFERENCES users(user_id),
	edited_by INTEGER REFERENCES users(user_id)
)

DROP TABLE palm;

ALTER TABLE new_palm RENAME TO palm;

INSERT INTO users(username,email,user_password, firstname,lastname, date_created,last_login)
VALUES ('superadmin','wongsatorn.sung@hotmail.com', '12345678', 'Super', 'Admin', current_timestamp, current_timestamp);

INSERT INTO palm(img_name, ripeness_id, oil_content, img, time_captured, last_edit, captured_by, edited_by)
VALUES ('palm_001',2,40.5,'',current_timestamp, current_timestamp, 1,1);


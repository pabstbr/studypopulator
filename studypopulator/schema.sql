DROP TABLE IF EXISTS participant;
CREATE TABLE participant (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
	name TEXT NOT NULL, 
	age INTEGER NOT NULL, 
	hasSibling INTEGER DEFAULT 0, 
	environmentalExposure TEXT, 
	geneticMutation TEXT,
	reviewStatus INTEGER NOT NULL DEFAULT not_review
);

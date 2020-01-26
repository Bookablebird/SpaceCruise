CREATE DATABASE spacecruise;
USE spacecruise;
create user 'dbuser05'@'localhost' identified by 'dbpass';
grant select, insert, update, delete on spacecruise.* to dbuser05@localhost;

CREATE TABLE Room
(
  RoomID INT NOT NULL,
  Name varchar(40) NOT NULL,
  Details varchar(1000) NOT NULL,
  Details2 varchar(1000),
  PRIMARY KEY (RoomID)
);

CREATE TABLE Description
(
  ID INT NOT NULL,
  Name varchar(30) NOT NULL,
  Details varchar(1000) NOT NULL,
  RoomID INT NOT NULL,
  PRIMARY KEY (ID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Moving
(
  FromID INT NOT NULL,
  Direction varchar(40) NOT NULL,
  Locked INT,
  ToID INT NOT NULL,
  RoomID INT NOT NULL,
  PRIMARY KEY (FromID, ToID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Enemy
(
  ID INT NOT NULL,
  Name varchar(40) NOT NULL,
  Health_points INT NOT NULL,
  Health_points_max INT NOT NULL,
  Combat_difficulty INT NOT NULL,
  RoomID INT,
  PRIMARY KEY (ID)
);

CREATE TABLE Item_type
(
  ID INT NOT NULL,
  Name varchar(40) NOT NULL,
  HP_Effect INT,
  Attack_accuracy INT,
  Time_effect INT,
  Ammo INT,
  Details varchar(1000),
  PRIMARY KEY (ID)
);

CREATE TABLE Playable_character
(
  ID INT NOT NULL,
  Combat_difficulty INT NOT NULL,
  Health_points INT NOT NULL,
  Health_points_max INT NOT NULL,
  Time_current INT NOT NULL,
  Time_max INT NOT NULL,
  RoomID INT NOT NULL,
  PRIMARY KEY (ID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Item
(
  ID INT NOT NULL,
  RoomID INT,
  EnemyID INT,
  PlayerID INT,
  ItemTypeID INT NOT NULL,
  PRIMARY KEY (ID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID),
  FOREIGN KEY (EnemyID) REFERENCES Enemy(ID),
  FOREIGN KEY (PlayerID) REFERENCES Playable_character(ID),
  FOREIGN KEY (ItemTypeID) REFERENCES Item_type(ID)
);
#						(RoomID, Name, Details, Details2)
INSERT INTO Room VALUES (01,'Public bathroom','There are toilets, mirrors, sinks and a window.',NULL);
INSERT INTO Room VALUES (02,'Hallway 1','It’s a hallway with 5 doors. There is a large map of the ship on the wall.',NULL);
INSERT INTO Room VALUES (03,'Supply closet','It’s a small closet with some mops and other cleaning equipment.',NULL);
INSERT INTO Room VALUES (04,'Cabin 1','There is an unmade bed on the left, in front of you there is a mirror, and on your right, a small bathroom.',NULL);
INSERT INTO Room VALUES (041,'Bathroom','There is a mirror and a cluttered sink.',NULL);
INSERT INTO Room VALUES (05,'Cabin 2','There is an unmade bed on the left, in front of you there is a mirror, and on your right, a small empty bathroom.',NULL);
INSERT INTO Room VALUES (051,'Bathroom','It is a small empty bathroom, with a mirror and a sink.',NULL);
INSERT INTO Room VALUES (06,'Engine room','There is a large engine system, a large window and bunch of monitors. Two of the monitors are on: the info panel (which is blinking with red) and a status panel.',NULL);
INSERT INTO Room VALUES (07,'Hallway 2','It’s an L shaped hallway with 3 doors.',NULL);
INSERT INTO Room VALUES (08,'Crew cabin area','It’s a V shaped hallway, with two doors and a lounge. The door where you came from and one to the rest of the crew cabins. The second door is shut, and you can hear a loud strange noise behind it.',NULL);
INSERT INTO Room VALUES (09,'Suite','There is a bathroom on the right, couch and a tv in front of you and on your left, there is bedroom.',NULL);
INSERT INTO Room VALUES (091,'Bathroom','There is a toilet, a mirror, a shower and a sink.',NULL);
INSERT INTO Room VALUES (10,'Suite bedroom','There is a large bed that has bunch of stuff on it …Seems like there were some weird people on this cruise, good that I didn’t run into them yesterday…',NULL);
INSERT INTO Room VALUES (111,'Bathroom','It is a small bathroom with some stuff on the counter.',NULL);
INSERT INTO Room VALUES (11,'Presidential Suite','There is a space pirate with a shotgun tearing down the room.','There is a corpse in front of you, on the right a bathroom and on the left a large bed and a living room area.');
INSERT INTO Room VALUES (12,'Hallway 4','There is an elevator.',NULL);
INSERT INTO Room VALUES (13,'Control room','There are TWO pirates in the room!.','There are two bodies on the ground, a large window and in front of you there is a broken control panel.');
INSERT INTO Room VALUES (14,'Storage room','There are see through containers filled with sheets and such everywhere. You see a moving pile of sheets close to you, a head pokes out of it, and it’s a space pirate, on the table next to him there is an assault rifle.','There is a corpse wrapped in bloody sheets, on the shells there are containers filled with sheets, pillows and cleaning products.');
INSERT INTO Room VALUES (15,'Market 1','There is a space pirate going through the store… This shouldn’t even faze you anymore…','There is a corpse next to you, a window next to the entrence, the shelves around the store are mostly empty.');
INSERT INTO Room VALUES (16,'Market 2','There is a space pirate going through the store, he just found something interesting and is totally caught off guard.','There is a corpse in front of you, a window next to the entrence, the shelfs around the store are empty… How did this guy not hear the shooting next room?…');
INSERT INTO Room VALUES (17,'Market 3','A space pirate tries to shoot you, but his first shot just misses your head.','There is a corpse next to you, a window next to the entrence, the Shelfs around the store are mostly empty.');
INSERT INTO Room VALUES (18,'Storage area','You blew up the storage door. There is an enormous hole on the wall and that is the last thing you see before you get sucked to space.',NULL);
INSERT INTO Room VALUES (19,'Elevator','You take the elevator down, board the nearest espace pod and launch towards home. Somehow you managed to survive!.',NULL);



#					(FromID, Direction, Locked, ToID, RoomID)
INSERT INTO Moving VALUES (01,'1',0,02,01);
INSERT INTO Moving VALUES (02,'1',0,01,02);
INSERT INTO Moving VALUES (02,'2',0,03,02);
INSERT INTO Moving VALUES (02,'3',1,04,02);
INSERT INTO Moving VALUES (02,'4',1,05,02);
INSERT INTO Moving VALUES (02,'5',1,06,02);
INSERT INTO Moving VALUES (03,'1',0,02,03);
INSERT INTO Moving VALUES (04,'1',0,041,04);
INSERT INTO Moving VALUES (04,'2',0,02,04);
INSERT INTO Moving VALUES (041,'1',0,04,041);
INSERT INTO Moving VALUES (05,'1',0,02,05);
INSERT INTO Moving VALUES (05,'2',0,051,05);
INSERT INTO Moving VALUES (051,'1',0,05,051);
INSERT INTO Moving VALUES (06,'1',0,08,06);
INSERT INTO Moving VALUES (06,'2',0,02,06);
INSERT INTO Moving VALUES (07,'1',0,08,07);
INSERT INTO Moving VALUES (07,'2',2,09,07);
INSERT INTO Moving VALUES (07,'3',4,11,07);
INSERT INTO Moving VALUES (08,'1',0,07,08);
INSERT INTO Moving VALUES (08,'2',4,18,08);
INSERT INTO Moving VALUES (08,'3',0,06,08);
INSERT INTO Moving VALUES (09,'1',0,091,09);
INSERT INTO Moving VALUES (09,'2',0,10,09);
INSERT INTO Moving VALUES (09,'3',0,07,09);
INSERT INTO Moving VALUES (091,'1',0,09,091);
INSERT INTO Moving VALUES (10,'1',0,09,10);
INSERT INTO Moving VALUES (11,'1',0,111,11);
INSERT INTO Moving VALUES (11,'2',0,7,11);
INSERT INTO Moving VALUES (11,'3',0,15,11);
INSERT INTO Moving VALUES (111,'1',0,11,111);
INSERT INTO Moving VALUES (12,'1',3,19,12);
INSERT INTO Moving VALUES (12,'2',0,13,12);
INSERT INTO Moving VALUES (13,'1',0,12,13);
INSERT INTO Moving VALUES (13,'2',0,17,13);
INSERT INTO Moving VALUES (14,'1',0,15,14);
INSERT INTO Moving VALUES (15,'1',0,11,15);
INSERT INTO Moving VALUES (15,'2',0,14,15);
INSERT INTO Moving VALUES (15,'3',0,16,15);
INSERT INTO Moving VALUES (16,'1',0,15,16);
INSERT INTO Moving VALUES (16,'2',0,17,16);
INSERT INTO Moving VALUES (17,'1',0,16,17);
INSERT INTO Moving VALUES (17,'2',3,13,17);



#				(ID,Name, Health_points, Health_points_max, Combat_difficulty, RoomID)
INSERT INTO Enemy VALUES (01,'11',3,3,4,11);
INSERT INTO Enemy VALUES (02,'15',3,3,5,15);
INSERT INTO Enemy VALUES (03,'14',3,3,1,14);
INSERT INTO Enemy VALUES (04,'16',3,3,3,16);
INSERT INTO Enemy VALUES (05,'17',3,3,6,17);
INSERT INTO Enemy VALUES (06,'13',3,3,5,13);


#				(ID, Name, HP_Effect, Attack_accuracy, Time_effect, Ammo, Details)
INSERT INTO Item_type VALUES (01,'pistol',-2,3,NULL,0,"It's a laser pistol.");
INSERT INTO Item_type VALUES (02,'shotgun',-3,3,NULL,0,"It's a shotgun that shoots a laser");
INSERT INTO Item_type VALUES (03,'rifle',-2,4,NULL,0,"It's a laser assault rifle.");
INSERT INTO Item_type VALUES (04,'medkit',5,NULL,NULL,NULL,"It's a small red bag with some bandages and stuff inside..");
INSERT INTO Item_type VALUES (05,'energydrink',NULL,NULL,-8,NULL,"It's a small blue and silver can that has some red text on it.");
INSERT INTO Item_type VALUES (06,'helmet',NULL,NULL,NULL,NULL,"It's a green military type helmet.");
INSERT INTO Item_type VALUES (07,'keycard',NULL,NULL,NULL,NULL,"It's a plastic card with 'Level 1' printed on it.");
INSERT INTO Item_type VALUES (08,'grenade',NULL,NULL,NULL,NULL,"It's a green ball with a pin in it.");
INSERT INTO Item_type VALUES (09,'ammo',NULL,NULL,NULL,12,"It's a small box with 12 bullets in it.");
INSERT INTO Item_type VALUES (11,'keycard',NULL,NULL,NULL,NULL,"It's a plastic card with 'Level 2' printed on it.");
INSERT INTO Item_type VALUES (12,'keycard',NULL,NULL,NULL,NULL,"It's a plastic card with 'Level 3' printed on it.");


#								(ID, Name, Details, RoomID)
INSERT INTO Description VALUES (01,'toilet', "It’s empty.", 041);
INSERT INTO Description VALUES (02,'mirror', "You see yourself, there are bags under your eyes and a penis drawn to your forehead.", 041);
INSERT INTO Description VALUES (03,'mirror', "You see yourself, there are bags under your eyes and a penis drawn to your forehead.", 01);
INSERT INTO Description VALUES (04,'mirror', "You see yourself, there are bags under your eyes and a penis drawn to your forehead.", 051);
INSERT INTO Description VALUES (05,'mirror', "You see yourself, there are bags under your eyes and a penis drawn to your forehead.", 091);
INSERT INTO Description VALUES (06,'mirror', "You see yourself, there are bags under your eyes and a penis drawn to your forehead.", 111);
INSERT INTO Description VALUES (07,'toilet', "It’s empty.", 051);
INSERT INTO Description VALUES (08,'toilet', "It’s empty.", 091);
INSERT INTO Description VALUES (09,'toilet', "It’s empty.", 111);
INSERT INTO Description VALUES (10,'toilet', "It’s empty.", 01);
INSERT INTO Description VALUES (11,'status', "Breach in the storage area. Level 10 death hazard.", 06);
INSERT INTO Description VALUES (12,'info', "Destination -Alpha Centauri-, reaching destination in 70 time units... Hmmm… Isn’t Alpha Centauri the nearest star from here? ", 06);
INSERT INTO Description VALUES (13,'sink', "There is nothing in the sink.", 041);
INSERT INTO Description VALUES (14,'sink', "There is nothing in the sink.", 051);
INSERT INTO Description VALUES (15,'sink', "There is nothing in the sink.", 01);
INSERT INTO Description VALUES (16,'sink', "There is nothing in the sink.", 111);
INSERT INTO Description VALUES (17,'sink', "There is nothing in the sink.", 091);
INSERT INTO Description VALUES (18,'container', "There are sheets and pillows.", 014);
INSERT INTO Description VALUES (19,'tv', "Snakes on the plane is playing.", 09);
INSERT INTO Description VALUES (20,'shelfs', "There is nothing on the shelfs.", 15);
INSERT INTO Description VALUES (21,'shelfs', "There is nothing on the shelfs.", 16);
INSERT INTO Description VALUES (22,'shelfs', "There is nothing on the shelfs.", 17);
INSERT INTO Description VALUES (23,'corpse', "It's a dead pirate.", 11);
INSERT INTO Description VALUES (24,'corpse', "It's a dead pirate.", 15);
INSERT INTO Description VALUES (25,'corpse', "It's a dead pirate.", 16);
INSERT INTO Description VALUES (26,'corpse', "It's a dead pirate.", 17);
INSERT INTO Description VALUES (27,'corpse', "It's a dead pirate.", 13);
INSERT INTO Description VALUES (28,'corpse', "It's a dead pirate.", 14);
INSERT INTO Description VALUES (29,'corpse 2', "It's a dead pirate.", 13);
INSERT INTO Description VALUES (30,'window', "You see the black nothingness of space.", 01);
INSERT INTO Description VALUES (31,'window', "You see the black nothingness of space.", 06);
INSERT INTO Description VALUES (32,'window', "You see the black nothingness of space.", 15);
INSERT INTO Description VALUES (34,'window', "You see the black nothingness of space.", 16);
INSERT INTO Description VALUES (35,'window', "You see the black nothingness of space.", 17);
INSERT INTO Description VALUES (36,'window', "You see the black nothingness of space.", 13);
INSERT INTO Description VALUES (37,'control', "It's a broken control panel, trying to use it, is futile.", 13);
INSERT INTO Description VALUES (38,'cleaning', "There's some bleach and pipe cleaner.", 06);




#				(ID, RoomID, EnemyID, PlayerID, ItemTypeID)
INSERT INTO Item VALUES (01,041,NULL,NULL,01);
INSERT INTO Item VALUES (02,11,01,NULL,02);
INSERT INTO Item VALUES (03,14,NULL,NULL,03);
INSERT INTO Item VALUES (04,03,NULL,NULL,04);
INSERT INTO Item VALUES (05,09,NULL,NULL,05);
INSERT INTO Item VALUES (06,10,NULL,NULL,06);
INSERT INTO Item VALUES (07,01,NULL,NULL,07);
INSERT INTO Item VALUES (08,08,NULL,NULL,08);
INSERT INTO Item VALUES (09,NULL,NULL,NULL,09);
INSERT INTO Item VALUES (11,03,NULL,NULL,11);
INSERT INTO Item VALUES (12,10,NULL,NULL,01);
INSERT INTO Item VALUES (13,NULL,NULL,NULL,09);
INSERT INTO Item VALUES (14,111,NULL,NULL,04);
INSERT INTO Item VALUES (15,13,06,NULL,01);
INSERT INTO Item VALUES (17,15,02,NULL,02);
INSERT INTO Item VALUES (18,15,NULL,NULL,05);
INSERT INTO Item VALUES (19,16,04,NULL,01);
INSERT INTO Item VALUES (20,16,04,NULL,12);
INSERT INTO Item VALUES (21,17,05,NULL,03);
INSERT INTO Item VALUES (22,17,NULL,NULL,04);

#(ID, Combat_difficulty, Health_points, Health_points_max, Time_current, Time_max, RoomID)
INSERT INTO Playable_character VALUES (01,8,10,10,0,70,01);



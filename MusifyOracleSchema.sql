DROP TABLE M_ADMIN;
DROP TABLE USER_INFO;
DROP TABLE GENRE;
DROP TABLE TRACK;
DROP TABLE ALBUM;
DROP TABLE ARTIST;
DROP SEQUENCE users_sequence;
DROP SEQUENCE album_sequence;
DROP SEQUENCE artist_sequence;
DROP SEQUENCE track_sequence;
DROP SEQUENCE genre_sequence;

/*CREATE TABLE M_ADMIN
(
  ADMIN_ID INT NOT NULL PRIMARY KEY,
  USERNAME VARCHAR2(50) NOT NULL,
  ADMIN_PASSWORD VARCHAR2(50) NOT NULL
);*/

CREATE TABLE USER_INFO
(
  USERNAME VARCHAR2(100) NOT NULL,
  USER_PASSWORD VARCHAR2(100) NOT NULL,
  EMAIL_ADDR VARCHAR2(100) NOT NULL,
  ADDRESS VARCHAR2(100) NOT NULL,
  PHONE_NUM VARCHAR2(100) NOT NULL,
  USER_ID INT NOT NULL,
  PRIMARY KEY (USER_ID)
);
create sequence users_sequence start with 1 increment by 1;

CREATE TABLE ARTIST
(
  ARTIST_NAME VARCHAR2(100) NOT NULL,
  ARTIST_ID INT NOT NULL,
  PRIMARY KEY (ARTIST_ID)
);
create sequence artist_sequence start with 1 increment by 1;

CREATE TABLE ALBUM

(
  ALBUM_ID INT NOT NULL,
  ALBUM_NAME VARCHAR2(100) NOT NULL,
  ARTIST_ID INT NOT NULL,
  PRIMARY KEY (ALBUM_ID, ARTIST_ID),
  FOREIGN KEY (ARTIST_ID) REFERENCES ARTIST(ARTIST_ID)
);
create sequence album_sequence start with 1 increment by 1;


CREATE TABLE TRACK
(
  TRACK_ID INT NOT NULL,
  TRACK_NAME VARCHAR2(100) NOT NULL,
  CREATED_AT DATE NOT NULL,
  TRACK_NUM INT NOT NULL,
  ALBUM_ID INT NOT NULL,
  ARTIST_ID INT NOT NULL,
  PRIMARY KEY (TRACK_ID, ALBUM_ID, ARTIST_ID),
  FOREIGN KEY (ALBUM_ID, ARTIST_ID) REFERENCES ALBUM(ALBUM_ID, ARTIST_ID)
);

create sequence track_sequence start with 1 increment by 1;

CREATE TABLE GENRE
(
  GENRE_DESC VARCHAR2(100) NOT NULL,
  GENRE_ID INT NOT NULL,
  ALBUM_ID INT NOT NULL,
  ARTIST_ID INT NOT NULL,
  PRIMARY KEY (GENRE_ID),
  FOREIGN KEY (ALBUM_ID, ARTIST_ID) REFERENCES ALBUM(ALBUM_ID, ARTIST_ID)
);
create sequence genre_sequence start with 1 increment by 1;

INSERT INTO USER_INFO VALUES ('Bincy', 'bincy', 'bincy@gmail.com', '2155 Main St, #116', '530-518-4640', 1);
INSERT INTO USER_INFO VALUES ('Shweta','sdube','sdube@gmail.com','730 Nord station','530-591-3761',2);
INSERT INTO USER_INFO VALUES ('Pranoti','pkulkarni','kulpranoti@gmail.com','730 Nord station','530-591-3707',3);
COMMIT;

--Artist details
insert into artist values( 'Justin Bieber', artist_sequence.NEXTVAL);
insert into artist values( 'Meghan Trainor', artist_sequence.NEXTVAL);
insert into artist values( 'Ariana Grande', artist_sequence.NEXTVAL);
insert into artist values( 'Adele', artist_sequence.NEXTVAL);
insert into artist values( 'Rihanna', artist_sequence.NEXTVAL);
insert into artist values( 'Sia', artist_sequence.NEXTVAL);
insert into artist values( 'Selena Gomez', artist_sequence.NEXTVAL);
insert into artist values( 'Charlie Puth', artist_sequence.NEXTVAL);
insert into artist values( 'The Chainsmokers', artist_sequence.NEXTVAL);
insert into artist values( 'Drake', artist_sequence.NEXTVAL);
insert into artist values( 'Shawn Mendes', artist_sequence.NEXTVAL);
insert into artist values( 'Zayn Malik', artist_sequence.NEXTVAL);
insert into artist values( 'Justin Timberlake', artist_sequence.NEXTVAL);
insert into artist values( 'Beyonce', artist_sequence.NEXTVAL);
insert into artist values( 'Carrie Underwood', artist_sequence.NEXTVAL);
insert into artist values( 'Wiz Khalifa', artist_sequence.NEXTVAL);
insert into artist values( 'Ellie Goulding', artist_sequence.NEXTVAL);
insert into artist values( 'Usher', artist_sequence.NEXTVAL);
insert into artist values( 'Coldplay', artist_sequence.NEXTVAL);
insert into artist values( 'Calvin Harris', artist_sequence.NEXTVAL);
commit;

--Album details
insert into album values(album_sequence.NEXTVAL,'Purpose',1);
insert into album values(album_sequence.NEXTVAL,'Thank you',2);
insert into album values(album_sequence.NEXTVAL,'Yours truly',3);
insert into album values(album_sequence.NEXTVAL,'Twenty five',4);
insert into album values(album_sequence.NEXTVAL,'Anti',5);
insert into album values(album_sequence.NEXTVAL,'This is acting',6);
insert into album values(album_sequence.NEXTVAL,'Nine track mind',7);
insert into album values(album_sequence.NEXTVAL,'Collage',8);
insert into album values(album_sequence.NEXTVAL,'Views',9);
insert into album values(album_sequence.NEXTVAL,'Illuminate', 10);
insert into album values(album_sequence.NEXTVAL,'Mind of mine', 11);
insert into album values(album_sequence.NEXTVAL,'Recrimination', 12);
insert into album values(album_sequence.NEXTVAL,'Lemonade', 13);
insert into album values(album_sequence.NEXTVAL,'Storyteller', 14);
insert into album values(album_sequence.NEXTVAL,'Khalifa', 15);
insert into album values(album_sequence.NEXTVAL,'Delirium', 16);
insert into album values(album_sequence.NEXTVAL,'Confessions', 17);
insert into album values(album_sequence.NEXTVAL,'A head full of dreams', 18);
insert into album values(album_sequence.NEXTVAL,'Motion', 19);
insert into album values(album_sequence.NEXTVAL,'Summer', 20);
commit;

--Tracks of all the artists
insert into track values(track_sequence.NEXTVAL, 'Sorry', '12-JUN-2015', 1, 1, 1);
insert into track values(track_sequence.NEXTVAL, 'Me too', '08-MAR-2016', 2, 2, 2);
insert into track values(track_sequence.NEXTVAL, 'Almost is never enough', '08-MAR-2013', 3, 3, 3);
insert into track values(track_sequence.NEXTVAL, 'Hello', '08-MAR-2015', 4, 4, 4);
insert into track values(track_sequence.NEXTVAL, 'Work', '08-MAR-2016', 5, 5, 5);
insert into track values(track_sequence.NEXTVAL, 'Cheap thrills', '08-MAR-2016', 6, 6, 6);
insert into track values(track_sequence.NEXTVAL, 'Good for you', '08-MAR-2015', 7, 7, 7);
insert into track values(track_sequence.NEXTVAL, 'We dont talk anymore', '08-MAR-2016', 8, 8, 8);
insert into track values(track_sequence.NEXTVAL, 'Closer', '08-MAR-2016', 9, 9, 9);
insert into track values(track_sequence.NEXTVAL, 'Show you', '20-SEP-2016', 10, 10, 10);
insert into track values(track_sequence.NEXTVAL, 'Pillowtalk', '20-SEP-2015', 11, 11, 11);
insert into track values(track_sequence.NEXTVAL, 'Cant stop the feeling', '20-SEP-2016', 12, 12, 12);
insert into track values(track_sequence.NEXTVAL, 'Hold up', '21-SEP-2016', 13, 13, 13);
insert into track values(track_sequence.NEXTVAL, 'Church bells', '14-FEB-2016', 14, 14, 14);
insert into track values(track_sequence.NEXTVAL, 'See you again', '16-FEB-2016', 15, 15, 15);
insert into track values(track_sequence.NEXTVAL, 'on my mind', '01-MAR-2016', 16, 16, 16);
insert into track values(track_sequence.NEXTVAL, 'Yeah', '01-MAR-2016', 17, 17, 17);
insert into track values(track_sequence.NEXTVAL, 'Hymn for the weekend', '05-SEP-2016', 18, 18, 18);
insert into track values(track_sequence.NEXTVAL, 'Yellow', '05-SEP-2016', 19, 19, 19);
insert into track values(track_sequence.NEXTVAL, 'Blame', '05-SEP-2014', 20, 20, 20);
commit;


--Genres info
insert into genre values('Metalcore',genre_sequence.NEXTVAL,1, 1);
insert into genre values('Electro',genre_sequence.NEXTVAL,2, 2);
insert into genre values('Pop',genre_sequence.NEXTVAL,3, 3);
insert into genre values('Soul',genre_sequence.NEXTVAL,4, 4);
insert into genre values('Dancehall',genre_sequence.NEXTVAL,5, 5);
insert into genre values('Synthpop',genre_sequence.NEXTVAL,6, 6);
insert into genre values('pop',genre_sequence.NEXTVAL,7, 7);
insert into genre values('tropical house',genre_sequence.NEXTVAL,8, 8);
insert into genre values('EDM',genre_sequence.NEXTVAL,9, 9);
insert into genre values('EDM',genre_sequence.NEXTVAL,10, 10);
insert into genre values('soul-pop',genre_sequence.NEXTVAL,11, 11);
insert into genre values('soul-pop',genre_sequence.NEXTVAL,12, 12);
insert into genre values('hip hop',genre_sequence.NEXTVAL,13, 13);
insert into genre values('hip hop',genre_sequence.NEXTVAL,14, 14);
insert into genre values('pop',genre_sequence.NEXTVAL,15, 15);
insert into genre values('EDM',genre_sequence.NEXTVAL,16, 16);
insert into genre values('pop',genre_sequence.NEXTVAL,17, 17);
insert into genre values('dance hall',genre_sequence.NEXTVAL,18, 18);
insert into genre values('dancehall',genre_sequence.NEXTVAL,19, 19);
insert into genre values('pop',genre_sequence.NEXTVAL,20, 20);
commit;


select * from artist;
select * from album;
select * from genre;
select * from track;

/*delete from genre where GENRE_ID = 15;
delete from album where album_id = 134;
delete from artist where ARTIST_ID = 95;*/
DROP TABLE M_ADMIN;
DROP TABLE USER_INFO;
DROP TABLE GENRE;
DROP TABLE TRACK;
DROP TABLE ALBUM;
DROP TABLE ARTIST;

CREATE TABLE M_ADMIN
(
  ADMIN_ID INT NOT NULL PRIMARY KEY,
  USERNAME VARCHAR2(50) NOT NULL,
  ADMIN_PASSWORD VARCHAR2(50) NOT NULL
);

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

INSERT INTO USER_INFO VALUES ('bincy', 'bincy', 'bincy@gmail.com', '2155 Main St, #116', '530-518-4640', 1);
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
insert into album values(album_sequence.NEXTVAL,'Purpose',81);
insert into album values(album_sequence.NEXTVAL,'Thank you', 82);
insert into album values(album_sequence.NEXTVAL,'Yours truly', 83);
insert into album values(album_sequence.NEXTVAL,'Twenty five', 84);
insert into album values(album_sequence.NEXTVAL,'Anti', 85);
insert into album values(album_sequence.NEXTVAL,'This is acting', 86);
insert into album values(album_sequence.NEXTVAL,'Nine track mind', 87);
insert into album values(album_sequence.NEXTVAL,'Collage', 88);
insert into album values(album_sequence.NEXTVAL,'Views', 89);
insert into album values(album_sequence.NEXTVAL,'Illuminate', 90);
insert into album values(album_sequence.NEXTVAL,'Mind of mine', 91);
insert into album values(album_sequence.NEXTVAL,'Recrimination', 92);
insert into album values(album_sequence.NEXTVAL,'Lemonade', 93);
insert into album values(album_sequence.NEXTVAL,'Storyteller', 94);
insert into album values(album_sequence.NEXTVAL,'Khalifa', 95);
insert into album values(album_sequence.NEXTVAL,'Delirium', 96);
insert into album values(album_sequence.NEXTVAL,'Confessions', 97);
insert into album values(album_sequence.NEXTVAL,'A head full of dreams', 98);
insert into album values(album_sequence.NEXTVAL,'Motion', 99);
insert into album values(album_sequence.NEXTVAL,'Summer', 100);
commit;

--Tracks of all the artists
insert into track values(track_sequence.NEXTVAL, 'Sorry', '12-JUN-2015', 1, 120, 81);
insert into track values(track_sequence.NEXTVAL, 'Me too', '08-MAR-2016', 2, 121, 82);
insert into track values(track_sequence.NEXTVAL, 'Almost is never enough', '08-MAR-2013', 3, 122, 83);
insert into track values(track_sequence.NEXTVAL, 'Hello', '08-MAR-2015', 4, 123, 84);
insert into track values(track_sequence.NEXTVAL, 'Work', '08-MAR-2016', 5, 124, 85);
insert into track values(track_sequence.NEXTVAL, 'Cheap thrills', '08-MAR-2016', 6, 125, 86);
insert into track values(track_sequence.NEXTVAL, 'Good for you', '08-MAR-2015', 7, 126, 87);
insert into track values(track_sequence.NEXTVAL, 'We dont talk anymore', '08-MAR-2016', 8, 127, 88);
insert into track values(track_sequence.NEXTVAL, 'Closer', '08-MAR-2016', 9, 128, 89);
insert into track values(track_sequence.NEXTVAL, 'Show you', '20-SEP-2016', 10, 129, 90);
insert into track values(track_sequence.NEXTVAL, 'Pillowtalk', '20-SEP-2015', 11, 130, 91);
insert into track values(track_sequence.NEXTVAL, 'Cant stop the feeling', '20-SEP-2016', 12, 131, 92);
insert into track values(track_sequence.NEXTVAL, 'Hold up', '21-SEP-2016', 13, 132, 93);
insert into track values(track_sequence.NEXTVAL, 'Church bells', '14-FEB-2016', 14, 133, 94);
insert into track values(track_sequence.NEXTVAL, 'See you again', '16-FEB-2016', 15, 134, 95);
insert into track values(track_sequence.NEXTVAL, 'on my mind', '01-MAR-2016', 16, 135, 96);
insert into track values(track_sequence.NEXTVAL, 'Yeah', '01-MAR-2016', 17, 136, 97);
insert into track values(track_sequence.NEXTVAL, 'Hymn for the weekend', '05-SEP-2016', 18, 137, 98);
insert into track values(track_sequence.NEXTVAL, 'Yellow', '05-SEP-2016', 19, 138, 99);
insert into track values(track_sequence.NEXTVAL, 'Blame', '05-SEP-2014', 20, 139, 100);
commit;


--Genres info
insert into genre values('Metalcore',genre_sequence.NEXTVAL,120, 81);
insert into genre values('Electro',genre_sequence.NEXTVAL,121, 82);
insert into genre values('Pop',genre_sequence.NEXTVAL,122, 83);
insert into genre values('Soul',genre_sequence.NEXTVAL,123, 84);
insert into genre values('Dancehall',genre_sequence.NEXTVAL,124, 85);
insert into genre values('Synthpop',genre_sequence.NEXTVAL,125, 86);
insert into genre values('pop',genre_sequence.NEXTVAL,126, 87);
insert into genre values('tropical house',genre_sequence.NEXTVAL,127, 88);
insert into genre values('EDM',genre_sequence.NEXTVAL,128, 89);
insert into genre values('EDM',genre_sequence.NEXTVAL,129, 90);
insert into genre values('soul-pop',genre_sequence.NEXTVAL,130, 91);
insert into genre values('soul-pop',genre_sequence.NEXTVAL,131, 92);
insert into genre values('hip hop',genre_sequence.NEXTVAL,132, 93);
insert into genre values('hip hop',genre_sequence.NEXTVAL,133, 94);
insert into genre values('pop',genre_sequence.NEXTVAL,134, 95);
insert into genre values('EDM',genre_sequence.NEXTVAL,135, 96);
insert into genre values('pop',genre_sequence.NEXTVAL,136, 97);
insert into genre values('dance hall',genre_sequence.NEXTVAL,137, 98);
insert into genre values('dancehall',genre_sequence.NEXTVAL,138, 99);
insert into genre values('pop',genre_sequence.NEXTVAL,139, 100);
commit;


select * from artist;
select * from album;
select * from genre;
select * from track;

delete from genre where GENRE_ID = 15;
delete from album where album_id = 134;
delete from artist where ARTIST_ID = 95;
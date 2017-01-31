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


INSERT INTO USER_INFO VALUES ('bincy', 'bincy', 'bincy@gmail.com', '2155 Main St, #116', '530-518-4640', 1);
COMMIT;

insert into artist values( 'The Pretty Reckless', artist_sequence.NEXTVAL);
insert into artist values( 'High Valley', artist_sequence.NEXTVAL);
commit;

insert into album values(album_sequence.NEXTVAL,'Brave', 127);
insert into album values(album_sequence.NEXTVAL,'Who You Selling for', 145);
insert into album values(album_sequence.NEXTVAL,'Dear Life', 147);
commit;

insert into track values(track_sequence.NEXTVAL, 'Ready to Run', '12-JUN-2001', 3, 28, 63);
insert into track values(track_sequence.NEXTVAL, 'Fools Gold', '08-MAR-2011', 3, 28, 63);
insert into track values(track_sequence.NEXTVAL, 'Where Do Broken Hearts Go', '08-MAR-2011', 3, 28, 63);
insert into track values(track_sequence.NEXTVAL, 'No Control', '08-MAR-2011', 3, 28, 63);
insert into track values(track_sequence.NEXTVAL, 'Night Changes', '08-MAR-2011', 3, 28, 63);
insert into track values(track_sequence.NEXTVAL, 'White Horse', '08-MAR-2010', 1, 4, 21);
insert into track values(track_sequence.NEXTVAL, 'Best Day', '08-MAR-2010', 2, 4, 21);
insert into track values(track_sequence.NEXTVAL, 'Fearless', '08-MAR-2010', 6, 4, 21);
insert into track values(track_sequence.NEXTVAL, 'Love Story', '08-MAR-2010', 7, 4, 21);
insert into track values(track_sequence.NEXTVAL, 'Wild City', '20-SEP-1988', 1, 141, 145);
insert into track values(track_sequence.NEXTVAL, 'Prisoner', '20-SEP-1988', 2, 141, 145);
insert into track values(track_sequence.NEXTVAL, 'Mad Love', '20-SEP-1988', 3, 141, 145);
insert into track values(track_sequence.NEXTVAL, 'Love Story', '21-SEP-1988', 4, 141, 145);
insert into track values(track_sequence.NEXTVAL, 'Dear Life', '14-FEB-2016', 1, 143, 147);
insert into track values(track_sequence.NEXTVAL, 'Making you Mine', '16-FEB-2016', 2, 143, 147);
insert into track values(track_sequence.NEXTVAL, 'I Be U Be', '01-MAR-2016', 3, 143, 147);
insert into track values(track_sequence.NEXTVAL, 'The Only', '01-MAR-2016', 4, 143, 147);
insert into track values(track_sequence.NEXTVAL, 'Dont Stop', '05-SEP-2016', 5, 143, 147);
insert into track values(track_sequence.NEXTVAL, 'Soldier', '05-SEP-2016', 6, 143, 147);
insert into track values(track_sequence.NEXTVAL, 'Young Forever', '05-SEP-2016', 7, 143, 147);
commit;


insert into genre values('Soul/folk',genre_sequence.NEXTVAL,49, 92);
insert into genre values('Pop rock',genre_sequence.NEXTVAL,28, 63);
insert into genre values('Pop',genre_sequence.NEXTVAL,32, 96);
insert into genre values('Pop',genre_sequence.NEXTVAL,63, 104);
insert into genre values('Soul/folk',genre_sequence.NEXTVAL,49, 92);
insert into genre values('Hard Rock',genre_sequence.NEXTVAL,141, 145);
insert into genre values('Country Music',genre_sequence.NEXTVAL,143, 147);
commit;


select * from artist;
select * from album;
select * from genre;
select * from track;

delete from genre where GENRE_ID = 23;
delete from album where album_id = 142;
delete from artist where ARTIST_ID = 142;
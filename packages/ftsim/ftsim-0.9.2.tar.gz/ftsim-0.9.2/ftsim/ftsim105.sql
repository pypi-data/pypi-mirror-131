---
---		ftsim105.sql
---
---		FTSIM	

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

-- Because of the foreign keys this command deletes the complete project
-- delete from project where prjid = 105;
	
INSERT INTO project VALUES(105, 30, 20, 25);

INSERT INTO ft VALUES(105, 'a' , 'FT',  6,   3);
INSERT INTO ft VALUES(105, 'k1', 'KP',  0,   4);
INSERT INTO ft VALUES(105, 'b' , 'FT', 12,   8);
INSERT INTO ft VALUES(105, 's' , 'LB',  4,   9);

insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a01', 'a',  3,  4);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a02', 'a',  4,  4);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a03', 'a',  5,  4);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a04', 'a',  6,  4);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a05', 'a',  7,  4);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a06', 'a',  8,  4);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a07', 'a',  9,  4);

insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a08', 'a',  9,  5);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a09', 'a',  9,  6);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a10', 'a',  8,  6);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a11', 'a',  7,  6);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a12', 'a',  6,  6);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a13', 'a',  5,  6);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a14', 'a',  4,  6);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a15', 'a',  3,  6);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a16', 'a',  2,  6);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a17', 'a',  2,  5);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'a18', 'a',  2,  4);

insert into lf(prjid,lfname,ftname,xkor,ykor,lftyp) values (105, 'k11', 'k1',  1,  5, 'KP');

insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b01', 'b', 10,  4);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b02', 'b', 11,  4);

insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b03', 'b', 11,  5);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b04', 'b', 11,  6);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b05', 'b', 11,  7);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b06', 'b', 11,  8);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b07', 'b', 11,  9);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b08', 'b', 11, 10);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b09', 'b', 11, 11);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b10', 'b', 10, 11);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b11', 'b',  9, 11);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b12', 'b',  9, 10);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b13', 'b',  9,  9);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b14', 'b',  9,  8);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 'b15', 'b',  9,  7);

insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 's01', 's',  8,  9);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 's02', 's',  7,  8);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 's03', 's',  7,  9);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 's04', 's',  7, 10);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 's05', 's',  6,  8);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 's06', 's',  6,  9);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 's07', 's',  6, 10);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 's08', 's',  5,  8);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 's09', 's',  5,  9);
insert into lf(prjid,lfname,ftname,xkor,ykor) values ( 105, 's10', 's',  5, 10);

insert into lfalt values  ( 105, 'a18', 'a01');

insert into lfalt values  ( 105, 'a17', 'k11');
insert into lfalt values  ( 105, 'k11', 'a17');

insert into lfalt values  ( 105, 'a07', 'b01');
insert into lfalt values  ( 105, 'b15', 'a09');

insert into lfalt values  ( 105, 'b13', 's01');
insert into lfalt values  ( 105, 's01', 'b13');

insert into lfziel values ( 105, 'k11', 'k1');
insert into lfziel values ( 105, 'b01', 'b' );
insert into lfziel values ( 105, 'b01', 's' );
insert into lfziel values ( 105, 'a09', 'b' );
insert into lfziel values ( 105, 's01', 's' );

insert into le(prjid,leid, lfname, ftziel) values ( 105, 'L01', 'a06', 'k1');
insert into le(prjid,leid, lfname, ftziel) values ( 105, 'L02', 'b07', 'b' );
insert into le(prjid,leid, lfname, ftziel) values ( 105, 'L03', 'b12', 's' );
insert into le(prjid,leid, lfname, ftziel) values ( 105, 'L04', 's07', NULL);
insert into le(prjid,leid, lfname, ftziel) values ( 105, 'L05', 's08', NULL);
insert into le(prjid,leid, lfname, ftziel) values ( 105, 'L06', 's09', NULL);


update lf set leid = (select leid from le where lf.prjid=le.prjid and lf.lfname=le.lfname)
where exists (select 1 from le where prjid = lf.prjid and lfname = lf.lfname and prjid = 105);

COMMIT;

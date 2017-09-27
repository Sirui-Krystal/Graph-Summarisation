/*This document is the recover script for the ACM_Small database*/
set datestyle to MDY;

create table author(
Aid int not null primary key,
PersonId text not null,
AuthorProfileID bigint, 
FName text,
MName text,
LName text,
Affiliation text,
Email text);

create table publisher(
PUid int not null primary key,
PublisherId text not null,
Name text,
ZipCode text,
City text,
State text,
Country text);

create table journal(
JOid int not null primary key,
JournalId text not null,
Name text,
Periodical_Type text,
Publication_Date date,
PUid int,
foreign key (PUid) references publisher (PUid));

create table proceeding(
PRid int not null primary key,
ProceedingId bigint not null,
Title text,
Subtitle text,
Proc_Desc text,
Con_City text,
Con_State text,
Con_Country text,
Con_Start_Date date,
Con_End_Date date,
Publication_Date date,
PUid int,
foreign key (PUid) references publisher (PUid));

create table paper(
Pid int not null primary key,
ArticleId bigint not null,
Title text,  
Publication_Date date,
JOid int,
PRid int,
foreign key (JOid) references journal (JOid),
foreign key (PRid) references proceeding (PRid));

create table writes(
Aid int not null,
Pid int not null,
primary key (Aid, Pid),
foreign key (Aid) references AUTHOR (Aid),
foreign key (Pid) references PAPER (Pid));

create table cites(
Pid int not null,
CitedPid int not null,
primary key (Pid, CitedPid),
foreign key (Pid) references PAPER (Pid),
foreign key (CitedPid) references PAPER (Pid));

COPY author from '/home/minjian/Documents/ACM_Small_CSV/author.csv' with CSV header;
COPY publisher from '/home/minjian/Documents/ACM_Small_CSV/publisher.csv' with CSV header;
COPY journal from '/home/minjian/Documents/ACM_Small_CSV/journal.csv' with CSV header;
COPY proceeding from '/home/minjian/Documents/ACM_Small_CSV/proceeding.csv' with CSV header;
COPY paper from '/home/minjian/Documents/ACM_Small_CSV/paper.csv' with CSV header;
COPY writes from '/home/minjian/Documents/ACM_Small_CSV/writes.csv' with CSV header;
COPY cites from '/home/minjian/Documents/ACM_Small_CSV/cites.csv' with CSV header;

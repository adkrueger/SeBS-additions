# STATEFUL SQL APP

This benchmark is meant to mimic a data analysis application that works on a couple of SQL tables and performs various operations on them, then stores the result of those operations in a third table. This is stateful in that the state and execution f the application depends on the contents of the SQL tables.

The SQL tables consist of the following:
`create table sys.city1 (`
&emsp;`id int,`
&emsp;`ssid int,`
&emsp;`name varchar(255),`
&emsp;`address varchar(255),`
&emsp;`balance int,`
&emsp;`primary key (ssid)`
`);`

`create table sys.city2 (`
&emsp;`id int,`
&emsp;`ssid int,`
&emsp;`name varchar(255),`
&emsp;`address varchar(255),`
&emsp;`balance int,`
&emsp;`primary key (ssid)`
`);`

`create table sys.results (`
&emsp;`count int,`
&emsp;`total int,`
&emsp;`temp varchar(255)`
`);`

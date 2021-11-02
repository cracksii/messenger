create database if not exists db;

use db;

drop procedure if exists DeleteClient;
drop procedure if exists DeleteAllClients;
drop procedure if exists DeleteParty;
drop procedure if exists DeleteAllParties;
drop procedure if exists CreateClientsTable;
drop procedure if exists CreatePartiesTable;
drop procedure if exists Reset;

DELIMITER $$
create procedure CreateClientsTable()
	begin
		drop table if exists clients;
		create table clients
		(
			client_id int primary key auto_increment,
			username varchar(50) not null,     		
			private_key varchar(64) not null,	
			creation_date char(10) not null,
			last_seen char(19) not null,
			status varchar(100) not null,
			image varchar(500) not null
		);
    end$$

create procedure CreatePartiesTable()
	begin
		drop table if exists parties;
		create table parties
		(
			party_id int primary key auto_increment,
            name varchar(50) not null,
			owner int not null,
            description varchar(150) not null,
            creation_date char(10) not null
		);
    end$$

create procedure DeleteClient(print char, id int)
	begin
		delete from clients where client_id = id;
		set @dynamic_sql = concat("drop table if exists ", concat(id, "_parties"));
		prepare stmt from @dynamic_sql;
		execute stmt;
        if print = "t" then select concat("Succesfully deleted client with id ", id) as "";
        end if;
	end$$
    
create procedure DeleteAllClients()
	begin
		declare max_id int; 
        set max_id = (select auto_increment from information_schema.tables where table_schema = 'db' and table_name = 'clients');
        
		while max_id != 0 do
			call DeleteClient('f', max_id);
			set max_id = max_id - 1;
		end while;
        # select "Deleted all clients" as "";
    end$$

create procedure DeleteParty(print char, id int)
	begin
		delete from clients where client_id = id;
		set @dynamic_sql = concat("drop table if exists ", concat(id, "_members"));
		prepare stmt from @dynamic_sql;
		execute stmt;
        if print = "t" then select concat("Succesfully deleted group with id ", id) as "";
        end if;
	end$$

create procedure DeleteAllParties()
	begin
		declare max_id int; 
        set max_id = (select auto_increment from information_schema.tables where table_schema = 'db' and table_name = 'parties');
        
		while max_id != 0 do
			call DeleteParty('f', max_id);
			set max_id = max_id - 1;
		end while;
        # select "Deleted all clients" as "";
    end$$
    
create procedure Reset()
	begin
		drop database db;
        create database db;
        create table clients
		(
			client_id int primary key auto_increment,
			username varchar(50) not null,     		
			private_key varchar(64) not null,	
			creation_date char(10) not null,
			last_seen char(19) not null,
			status varchar(100) not null,
			image varchar(500) not null
		);
        create table parties
		(
			party_id int primary key auto_increment,
            name varchar(50) not null,
			owner int not null,
            description varchar(150) not null,
            creation_date char(10) not null
		);
	end$$
DELIMITER ;

call Reset();

create database if not exists db;

use db;

drop procedure if exists AddClient;
drop procedure if exists DeleteClient;
drop procedure if exists DeleteAllClients;
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
			party_table varchar(60) not null,
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
            message_table varchar(60) not null,
            member_table varchar(60) not null
		);
    end$$

create procedure AddClient(username varchar(50), private_key varchar(60), status varchar(100), image varchar(500))
	begin
		declare party_table_name varchar(100);
        declare id int;
		
		set id = (select auto_increment from information_schema.tables where table_schema = 'db' and table_name = 'clients');
        if id is null then
			set id = "1";
		end if;
		set party_table_name = concat(id, "_party_ids");
		select (select auto_increment from information_schema.tables where table_schema = 'db' and table_name = 'clients') as "";
		insert into db.clients (username, private_key, creation_date, last_seen, party_table, status, image)
		values (username, private_key, replace(current_date(), "-", "."), replace(now(), "-", "."), party_table_name, status, image);
		
		set @dynamic_sql = concat("create table ", party_table_name, " (party_id int primary key)");

		prepare stmt from @dynamic_sql;
		execute stmt;
        
        select concat("Successfully created client with id ", id) as ""; 
	end$$

create procedure DeleteClient(print char, id int)
	begin
		delete from clients where client_id = id;
		set @dynamic_sql = concat("drop table if exists ", concat(id, "_party_ids"));
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
    
create procedure Reset()
	begin
		call DeleteAllClients();
		call CreateClientsTable();
        call CreatePartiesTable();
	end$$
DELIMITER ;

call Reset();

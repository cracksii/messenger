select * from clients where username="TestUser"                                                    # 2021.11.01 16:57:33
select * from clients where username="Other User"                                                  # 2021.11.01 16:57:59
select * from parties where party_id=1                                                             # 2021.11.01 16:58:22
select client_id from 1_members                                                                    # 2021.11.01 16:58:22
insert into 1_messages (content, author, timestamp) values ("Some annoying message you don't like", 1, "01.11.2021 16:58:22")# 2021.11.01 16:58:22
select * from clients where username="TestUser"                                                    # 2021.11.01 16:59:29
select * from clients where username="Other User"                                                  # 2021.11.01 16:59:33
select * from parties where party_id=1                                                             # 2021.11.01 16:59:38
select client_id from 1_members                                                                    # 2021.11.01 16:59:38
insert into 1_messages (content, author, timestamp) values ("Lul a message", 1, "01.11.2021 16:59:38")# 2021.11.01 16:59:38
select * from clients where username="TestUser"                                                    # 2021.11.01 17:00:34
select * from clients where username="Other User"                                                  # 2021.11.01 17:00:37
select * from parties where party_id=1                                                             # 2021.11.01 17:00:39
select client_id from 1_members                                                                    # 2021.11.01 17:00:39
insert into 1_messages (content, author, timestamp) values ("EWasda", 1, "01.11.2021 17:00:39")    # 2021.11.01 17:00:39
select * from clients where username="TestUser"                                                    # 2021.11.01 17:01:25
select * from clients where username="Other User"                                                  # 2021.11.01 17:01:28
select * from parties where party_id=1                                                             # 2021.11.01 17:01:33
select client_id from 1_members                                                                    # 2021.11.01 17:01:33
insert into 1_messages (content, author, timestamp) values ("oigdiogc", 1, "01.11.2021 17:01:33")  # 2021.11.01 17:01:33
select * from clients where username="TestUser"                                                    # 2021.11.01 17:02:51
select * from clients where username="Other User"                                                  # 2021.11.01 17:02:55
select * from parties where party_id=1                                                             # 2021.11.01 17:03:03
select client_id from 1_members                                                                    # 2021.11.01 17:03:03
insert into 1_messages (content, author, timestamp) values ("Test", 1, "01.11.2021 17:03:03")      # 2021.11.01 17:03:03
select * from clients where username="TestUser"                                                    # 2021.11.01 17:03:48
select * from clients where username="Other User"                                                  # 2021.11.01 17:03:53
select * from parties where party_id=1                                                             # 2021.11.01 17:03:56
select client_id from 1_members                                                                    # 2021.11.01 17:03:56
insert into 1_messages (content, author, timestamp) values ("Hiii ", 2, "01.11.2021 17:03:56")     # 2021.11.01 17:03:56
select * from parties where party_id=1                                                             # 2021.11.01 17:05:08
select client_id from 1_members                                                                    # 2021.11.01 17:05:08
insert into 1_messages (content, author, timestamp) values ("Second", 2, "01.11.2021 17:05:08")    # 2021.11.01 17:05:08
show tables                                                                                        # 2021.11.01 17:06:07
drop table 1_members                                                                               # 2021.11.01 17:06:07
drop table 1_messages                                                                              # 2021.11.01 17:06:07
drop table 1_parties                                                                               # 2021.11.01 17:06:08
drop table 2_parties                                                                               # 2021.11.01 17:06:08
drop table clients                                                                                 # 2021.11.01 17:06:08
drop table parties                                                                                 # 2021.11.01 17:06:08
create table clients(
                            client_id int primary key auto_increment,
                            username varchar(50) not null,
                            private_key varchar(64) not null,
                            creation_date char(10) not null,
                            last_seen char(19) not null,
                            status varchar(250) not null,
                            image varchar(500) not null)# 2021.11.01 17:06:08
create table parties(
                            party_id int primary key auto_increment,
                            name varchar(50) not null,
                            owner int not null,
                            description varchar(250) not null,
                            creation_date char(10) not null)# 2021.11.01 17:06:08
select auto_increment from information_schema.tables WHERE table_name='clients'                    # 2021.11.01 17:06:09
insert into clients (username, private_key, creation_date, last_seen, status, image) values ('TestUser', 'd713884fffad4dc8dd5da087efde228724ad833c43965f992f0dd2033a2522ed', '01.11.2021', '01.11.2021 17:06:07', 'online like a boss', 'image.png')# 2021.11.01 17:06:09
create table 1_parties (id int primary key auto_increment, party_id int)                           # 2021.11.01 17:06:09
select auto_increment from information_schema.tables WHERE table_name='clients'                    # 2021.11.01 17:06:09
insert into clients (username, private_key, creation_date, last_seen, status, image) values ('Other User', 'd713884fffad4dc8dd5da087efde228724ad833c43965f992f0dd2033a2522ed', '01.11.2021', '01.11.2021 17:06:07', 'online like a boss', 'image.png')# 2021.11.01 17:06:09
create table 2_parties (id int primary key auto_increment, party_id int)                           # 2021.11.01 17:06:09
select party_id from parties where name='TestParty' and owner='1'                                  # 2021.11.01 17:06:09
insert into parties (name, owner, description, creation_date) values('TestParty', '1', 'No desc', '01.11.2021')# 2021.11.01 17:06:09
select party_id from parties where name='TestParty' and owner='1' and description='No desc'        # 2021.11.01 17:06:09
create table 1_members (id int primary key auto_increment, client_id int)                          # 2021.11.01 17:06:09
create table 1_messages (id int primary key auto_increment, content text, author int, timestamp char(19))# 2021.11.01 17:06:09
insert into 1_parties (party_id) values (1)                                                        # 2021.11.01 17:06:09
insert into 1_members (client_id) values (1)                                                       # 2021.11.01 17:06:09
select party_id from parties where name='Second Party' and owner='2'                               # 2021.11.01 17:06:09
insert into parties (name, owner, description, creation_date) values('Second Party', '2', 'Long desc', '01.11.2021')# 2021.11.01 17:06:09
select party_id from parties where name='Second Party' and owner='2' and description='Long desc'   # 2021.11.01 17:06:09
create table 2_members (id int primary key auto_increment, client_id int)                          # 2021.11.01 17:06:09
create table 2_messages (id int primary key auto_increment, content text, author int, timestamp char(19))# 2021.11.01 17:06:09
insert into 1_parties (party_id) values (2)                                                        # 2021.11.01 17:06:09
insert into 2_members (client_id) values (1)                                                       # 2021.11.01 17:06:09
insert into 2_parties (party_id) values (2)                                                        # 2021.11.01 17:06:09
insert into 2_members (client_id) values (2)                                                       # 2021.11.01 17:06:09
insert into 2_parties (party_id) values (1)                                                        # 2021.11.01 17:06:09
insert into 1_members (client_id) values (2)                                                       # 2021.11.01 17:06:09
select * from clients                                                                              # 2021.11.01 17:06:09
select * from parties                                                                              # 2021.11.01 17:06:09
select * from clients where username="Other User"                                                  # 2021.11.01 17:06:34
select * from clients where username="TestUser"                                                    # 2021.11.01 17:06:36
select * from parties where party_id=1                                                             # 2021.11.01 17:06:45
select client_id from 1_members                                                                    # 2021.11.01 17:06:45
insert into 1_messages (content, author, timestamp) values ("Hello My Frendo", 2, "01.11.2021 17:06:45")# 2021.11.01 17:06:45
select * from parties where party_id=2                                                             # 2021.11.01 17:07:01
select client_id from 2_members                                                                    # 2021.11.01 17:07:01
insert into 2_messages (content, author, timestamp) values ("Secondo frendo", 2, "01.11.2021 17:07:01")# 2021.11.01 17:07:01
select * from clients where username="TestUser"                                                    # 2021.11.01 17:11:49
select * from clients where username="TestUser"                                                    # 2021.11.01 17:11:54
select * from clients where username="TestUser"                                                    # 2021.11.01 17:12:18
select * from clients where username="TestUser"                                                    # 2021.11.01 17:12:49
select * from clients where username="TestUser"                                                    # 2021.11.01 17:13:42
select * from clients where username="Other User"                                                  # 2021.11.01 17:19:04
select * from clients where username="TestUser"                                                    # 2021.11.01 17:19:19
select * from clients where username="TestUser"                                                    # 2021.11.01 17:19:53
select * from clients where username="TestUser"                                                    # 2021.11.01 17:20:28
select * from clients where username="TestUser"                                                    # 2021.11.01 17:20:45
select * from clients where username="TestUser"                                                    # 2021.11.01 17:22:07
select * from clients where username="TestUser"                                                    # 2021.11.01 17:22:17
select * from clients where username="TestUser"                                                    # 2021.11.01 17:22:38
select * from clients where username="TestUser"                                                    # 2021.11.01 17:23:07
select * from clients where username="TestUser"                                                    # 2021.11.01 17:23:19
select * from clients where username="TestUser"                                                    # 2021.11.01 17:24:42
select * from clients where username="TestUser"                                                    # 2021.11.01 17:24:50
select * from clients where username="TestUser"                                                    # 2021.11.01 17:25:13
select * from clients where username="TestUser"                                                    # 2021.11.01 17:25:21
select * from clients where username="TestUser"                                                    # 2021.11.01 17:26:11
select * from clients where username="TestUser"                                                    # 2021.11.01 17:26:17
select * from clients where username="TestUser"                                                    # 2021.11.01 17:29:52
select * from clients where username="TestUser"                                                    # 2021.11.01 17:29:58
select * from clients where username="TestUser"                                                    # 2021.11.01 17:30:42
select * from clients where username="Other User"                                                  # 2021.11.01 21:25:30
select * from clients where username="Other User"                                                  # 2021.11.01 21:25:53
select * from clients where username="Other User"                                                  # 2021.11.01 21:26:17
select * from clients where username="Other User"                                                  # 2021.11.01 21:27:04
select * from clients where username="Other User"                                                  # 2021.11.01 21:27:14
select party_id from 2_parties                                                                     # 2021.11.01 21:27:14
select * from clients where username="Other User"                                                  # 2021.11.01 21:28:41
select party_id from 2_parties                                                                     # 2021.11.01 21:28:41
select * from clients where username="Other User"                                                  # 2021.11.01 21:32:02
select * from clients where username="Other User"                                                  # 2021.11.01 21:32:44
select party_id from 2_parties                                                                     # 2021.11.01 21:32:44
select * from parties where party_id=2                                                             # 2021.11.01 21:32:44
select client_id from 2_members                                                                    # 2021.11.01 21:32:44
select * from parties where party_id=1                                                             # 2021.11.01 21:32:44
select client_id from 1_members                                                                    # 2021.11.01 21:32:44
select * from clients where username="Other User"                                                  # 2021.11.01 21:33:02
select party_id from 2_parties                                                                     # 2021.11.01 21:33:02
select * from parties where party_id=2                                                             # 2021.11.01 21:33:02
select client_id from 2_members                                                                    # 2021.11.01 21:33:02
select * from parties where party_id=1                                                             # 2021.11.01 21:33:02
select client_id from 1_members                                                                    # 2021.11.01 21:33:02
select * from clients where username="Other User"                                                  # 2021.11.02 10:44:38
select * from clients where username="TestUser"                                                    # 2021.11.02 10:44:43
select * from parties where party_id=1                                                             # 2021.11.02 10:44:49
select client_id from 1_members                                                                    # 2021.11.02 10:44:49
insert into 1_messages (content, author, timestamp) values ("Hello", 2, "02.11.2021 10:44:49")     # 2021.11.02 10:44:49
select * from parties where party_id=1                                                             # 2021.11.02 10:45:19
select client_id from 1_members                                                                    # 2021.11.02 10:45:19
insert into 1_messages (content, author, timestamp) values ("wasd", 2, "02.11.2021 10:45:19")      # 2021.11.02 10:45:19

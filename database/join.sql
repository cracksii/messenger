use db;

drop table if exists customer;
drop table if exists fruits;

create table customer 
(
	id int primary key,
    fruit_id int,
    name varchar(25)
    # tom could get his own table (no particular limit for fruits). this would be referenced with its name in another property called eg fruit_table_name
);

create table fruits
(
	fruit_id int primary key,
    fruit varchar(25)
);

insert into customer (id, fruit_id, name) values (1, 10, "Tom");
insert into customer (id, fruit_id, name) values (2, 5, "Sabine");

insert into fruits (fruit_id, fruit) values (10, "Banana");
insert into fruits (fruit_id, fruit) values (5, "Apfel");

select fruits.fruit_id, fruits.fruit
from customer 
inner join fruits 
on customer.fruit_id = fruits.fruit_id
group by id;

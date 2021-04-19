create table accounts(
    id int(8) unsigned not null auto_increment,
    email varchar(255) not null,
    password varchar(255) not null,
    name varchar(255) not null,
    phone varchar(255),
    loginStatus tinyint(1),
    created_at TIMESTAMP,
    PRIMARY KEY(id)
)AUTO_INCREMENT = 1;

create table customers(
    id int(8) unsigned not null auto_increment, 
    address varchar(255),
    account_id int(8) unsigned,
    PRIMARY KEY(id),
    FOREIGN KEY (account_id) REFERENCES accounts(id)
)AUTO_INCREMENT = 1;

create table sellers(
    id int(8) unsigned not null auto_increment,
    account_id int(8) unsigned,
    third_party TINYINT(1),
    organization_id int(8) unsigned,
    PRIMARY KEY(id),
    FOREIGN KEY (account_id) REFERENCES accounts(id)
)AUTO_INCREMENT = 1;

create table organizations(
    id int(8) unsigned not null auto_increment,
    email varchar(255),
    name varchar(255),
    description varchar(255),
    PRIMARY KEY(id)
)AUTO_INCREMENT = 1;

create table products(
    id int(8) unsigned not null auto_increment,
    seller_id int(8) unsigned,
    product_name varchar(255),
    price decimal(10,5),
    genre varchar(255),
    description varchar(255),
    quantity integer,
    third_party tinyint(1),
    PRIMARY KEY(id),
    FOREIGN KEY (seller_id) REFERENCES sellers(id)
)AUTO_INCREMENT = 1;

create table basket(
    id int(8) unsigned not null auto_increment,
    customer_id int(8) unsigned,
    product_id int(8) unsigned,
    quantity integer,
    created_at TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)AUTO_INCREMENT = 1;

create table orders(
    id int(8) unsigned not null auto_increment,
    product_id int(8) unsigned,
    customer_id int(8) unsigned,
    quantity integer,
    delivery_method varchar(255),
    created_at TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)AUTO_INCREMENT = 1;

create table payPalRecords(
    id int(8) unsigned not null auto_increment,
    customer_id int(8) unsigned,
    email varchar(255),
    password varchar(255),
    created_at TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)AUTO_INCREMENT = 1;

create table creditCardRecords(
    id int(8) unsigned not null auto_increment,
    customer_id int(8) unsigned,
    card_no varchar(255),
    card_name varchar(255),
    card_cvc varchar(255),
    exp_date varchar(255),
    created_at TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)AUTO_INCREMENT = 1;


drop table accounts
drop table customers
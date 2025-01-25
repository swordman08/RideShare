create table rideshare.driver
(
    driver_id    int auto_increment
        primary key,
    name         varchar(50)          null,
    email        varchar(100)         null,
    phone_number varchar(15)          null,
    car_details  varchar(100)         null,
    driver_mode  tinyint(1) default 0 null,
    rating       float      default 0 null,
    constraint email
        unique (email)
);


create table rideshare.ride
(
    ride_id          int auto_increment
        primary key,
    rider_id         int          null,
    driver_id        int          null,
    pickup_location  varchar(100) null,
    dropoff_location varchar(100) null,
    ride_timestamp   datetime     null,
    rating           float        null,
    constraint ride_ibfk_1
        foreign key (rider_id) references rideshare.rider (rider_id),
    constraint ride_ibfk_2
        foreign key (driver_id) references rideshare.driver (driver_id)
);

create index driver_id
    on rideshare.ride (driver_id);

create index rider_id
    on rideshare.ride (rider_id);


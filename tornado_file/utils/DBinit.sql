create database itcast default character set utf8;

use itcast;

create table it_usr_info(
  ui_user_id bigint unsigned auto_increment comment '用户ID',
  ui_name varchar(64) not null comment '用户名',
  ui_passwd varchar(128) not null comment '密码',
  ui_age int null comment '年龄',
  ui_mobile char(11) not null comment '手机号',
  ui_avatar varchar(128) null comment '头像',
  ui_ctime datetime default current_timestamp comment '创建时间',
  ui_utime datetime not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (ui_user_id),
  unique (ui_mobile)
)engine=InnoDB default charset=utf8 comment '用户表';

create table it_house_info(
  hi_house_id bigint unsigned auto_increment comment '房屋id',
  hi_user_id bigint unsigned not null comment '用户ID',
  hi_name varchar(64) not null comment '房屋名',
  hi_address varchar(256) not null comment '地址',
  hi_price int unsigned not null comment '价格',
  hi_ctime datetime not null default current_timestamp comment '创建时间',
  hi_utime datetime not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (hi_house_id),
  constraint foreign key (hi_user_id) references it_usr_info(ui_user_id)
)engine =InnoDB default charset=utf8 comment '房屋信息表';

create table it_house_image(
  hi_image_id bigint unsigned auto_increment comment '房屋id',
  hi_house_id bigint unsigned comment '房屋id',
  hi_url varchar(128) not null comment '图片url',
  hi_ctime datetime not null default current_timestamp comment '创建时间',
  hi_utime datetime not null default current_timestamp on update current_timestamp comment '更新时间',
  primary key (hi_image_id),
  constraint foreign key (hi_house_id) references it_house_info(hi_house_id)
)engine = InnoDB default charset=utf8 comment '房屋图片';

drop table it_house_image;
drop table it_house_info;
drop table it_usr_info;


insert into it_usr_info(ui_name, ui_passwd, ui_age, ui_mobile)
values
       ('a','a',20,'12345678900'),
       ('b','a',20,'12345678901'),
       ('c','a',20,'12345678902'),
       ('d','a',21,'12345678903');

insert into it_house_info(hi_user_id,hi_name,hi_address,hi_price)
values (1,'a的房子','aaaaa',50000),
       (1,'a的房子b','bbbb',30000),
       (3,'c的房子','cccc',10000),
       (4,'d的房子','dddd',50000);


insert into it_house_image(hi_house_id, hi_url)
VALUES(1,'/a/url'),
      (2,'/a/url'),
      (1,'/a/url');


select distinct ui_age from it_usr_info where ui_age>20;
# 范围查找
select * from it_usr_info where ui_age in (20,22);
# 统计
select count(*) as '总数' from it_usr_info;
# 范围查找
select * from it_usr_info where ui_age between 20 and 23 order by ui_age limit 2,1;
# 分组
select ui_age,count(ui_age) from it_usr_info group by ui_age;
# 增加数据表的列
alter table it_usr_info add ui_area_id varchar(10) not null comment '区域id';
#删除数据表的列
alter table it_usr_info drop ui_area_id;
# 更新
update it_usr_info set ui_area_id=1 where ui_user_id=1;
# 内连接
select * from it_usr_info inner join it_house_info on it_usr_info.ui_user_id=it_house_info.hi_user_id;
select * from it_usr_info inner join it_house_info on it_usr_info.ui_user_id =it_house_info.hi_user_id left join it_house_image ihi on it_house_info.hi_house_id = ihi.hi_house_id;
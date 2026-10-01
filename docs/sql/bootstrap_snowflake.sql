-- Run as a Snowflake administrator, then set a real password out of band.
-- The portfolio loader and transformer roles are separated intentionally.

create warehouse if not exists claims_wh
  warehouse_size = 'XSMALL'
  auto_suspend = 60
  auto_resume = true
  initially_suspended = true;

create database if not exists claims_analytics;
create schema if not exists claims_analytics.raw;
create schema if not exists claims_analytics.analytics_dev;

create role if not exists claims_loader;
create role if not exists claims_transformer;

grant usage on warehouse claims_wh to role claims_loader;
grant usage on database claims_analytics to role claims_loader;
grant usage on schema claims_analytics.raw to role claims_loader;
grant create table on schema claims_analytics.raw to role claims_loader;
grant select, insert, update, delete, truncate
  on all tables in schema claims_analytics.raw to role claims_loader;
grant select, insert, update, delete, truncate
  on future tables in schema claims_analytics.raw to role claims_loader;

grant usage on warehouse claims_wh to role claims_transformer;
grant usage on database claims_analytics to role claims_transformer;
grant usage on schema claims_analytics.raw to role claims_transformer;
grant select on all tables in schema claims_analytics.raw
  to role claims_transformer;
grant select on future tables in schema claims_analytics.raw
  to role claims_transformer;
grant usage, create table, create view
  on schema claims_analytics.analytics_dev to role claims_transformer;

alter warehouse claims_wh suspend;

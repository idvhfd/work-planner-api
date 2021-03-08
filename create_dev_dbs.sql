/*------------------     BEGIN PLANNER    -------------------*/
create user planner with password 'planner';
create database planner;
create database planner_test;
grant all privileges on database planner to planner;
grant all privileges on database planner_test to planner;
/*---------------------     END PLANNER    ------------------*/

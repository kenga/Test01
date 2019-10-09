# Test for Data Engineer

## Q1. Access Log analytics
Running environment
- Linux
- Python 3.6+

Instruction
1. download the access and unzip it to directory ```q1/data/```. 
(URL: ftp://ita.ee.lbl.gov/traces/NASA_access_log_Aug95.gz)
2. change directory to ```q1/```
3. run ```python count_http.py``` to count the total number of HTTP requests
4. run ```python count_top10_hosts.py``` to find the top-10 (host) hosts makes most requests from 18th Aug to 20th Aug
5. run ```python count_country.py``` to find out the country with most requests 

Remark
- For finding out the country with most requests, its assumed that the country of a server can be deduced from the 
domain name, which may not be true in reality.

## Q2. RDBMS
Running environment
- MySQL 
- Docker

Instruction for environment setup
1. install docker and init swarm
2. change directory to ```q2/``` and issue command ```docker stack deploy -c docker-compose.yml mysql```
3. connect local database with port 3308
4. run sql statements in table_schema.sql and test_data.sql
5. run the 2 statement in ans.sql the answer of question 2

 
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

## Q3. Simple (but hard) counter
Thought process on the design:
1. For solving this problem, the server for accepting the voting requests needs to be horizontally 
   scalable. 
2. Besides the backend server, the data storage needs to be scalable too. Otherwise, the data 
   storage will still become the bottleneck. NoSQL that do sharding / partitioning should be used. 
3. Initially, I planned to use docker swarm to solve this problem. Docker swarm can help scaling out, 
   but manual update of deployment config is need to do so. This requires monitoring and deployment 
   effort. It turns out using docker swarm is probably not a good solution.
4. Given that the logic of the backend server is not complicated and need not to be stateful, 
   serverless approach should be more suitable.

Design:
- Frontend for voting: a static web-page, with button that issues ajax call for voting on click
  - Information included in the ajax call: chosen candidate, kiosk ID (or simply the IP address
    of the kiosk if the IP address can identify the kiosk)
- Backend server for processing voting requests: use AWS Lambda (with python) for implementation
  - Upon a voting request is received, the python script will insert a record to DynamoDB. The 
    record will include the candidate ID and the current timestamp. 
- Data storage: DynamoDB would be used
  - partition key: concatenated string of the kiosk ID and the timestamp 
  - sort key: timestamp 
  - some thought about choosing the partition key:
    - candidate ID would not be suitable for scalability, reasons:
      - only 3 possible values
      - the values are not evenly populated
    - kiosk ID should not be suitable too, as some kiosks in densely populated area may get many 
      votes
    - Concatenating kiosk ID with timestamp can further scatter the records into different 
      partitions more evenly. This also avoid possible collision on primary key.
- Frontend for viewing voting result: a static web-page with ajax call to get voting results
- Backend server to give voting result: use AWS Lambda for implementation
  - For retrieving voting result of last 10 minutes, a scan with timestamp as filter should be used.
  - For retrieving the accumulated voting result, scan is still needed. However, full table scan for
    each of this request should be unnecessarily expensive. The result and the latest timestamp 
    should be cached. And the next request can start from the last cached timestamp and increment 
    from the last result.
 
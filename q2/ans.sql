# 1: Find the top-10 articles (title, ID and like received) with most LIKE received from user on 2017-04-01
select s.objectId, a.title, s.likes
from (
         select objectId, count(userId) as likes
         FROM clickstream
         where action = 'LIKE_ARTICLE'
           and date(time) = date('2017-04-01')
         group by objectId
         order by likes desc
         limit 10) s
         join articles a on s.objectId = a.id;

# 2: Find the count of users who install the app (i.e. with FIRST_INSTALL event) on
# 2017-04-01 and use our app at least once (i.e. with any event) between 2017-04-02
# and 2017-04-08
select count(*) as num_users
from (
         select distinct userId
         from clickstream
         where userId in (
             select userId
             from clickstream
             where action = 'FIRST_INSTALL'
               and date(time) = date('2017-04-01')
         )
           and date(time) >= date('2017-04-02')
           and date(time) <= date('2017-04-08')
     ) s;
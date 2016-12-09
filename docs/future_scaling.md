# Future Scaling

### Ingestion Layer
There are only two ongoing data sources at this point, the injuryfx data and the gameday data. As such, the daily ingestion process takes no more than a few minutes. With this fact in front of us we didn't find it a good use of resources to create a full blown ingestion system such as Storm or Kafka. A couple events could increase the amount of ingested data. It's possible in the future more baseball specific datasources could be tapped for data. But even if we tripled the number of new sources, the ingestion process for a day would likely take under ten minutes to complete and remain batch appropriate. A more likely scenario that would require a more complex injection system is if we decided to expand the number of sports we analyzed. For instance, if we started tracking football, basketball, hockey, soccer, track & field, swimming, golf, tennis, etc with as much detail as we currently do with baseball then a more advanced ingestion system would become appropriate. In this case we would potentially stand up a Kafka or Storm cluster to handle such an advanced ingestion from so many disperate services. However, without current access to such data flows we can't commit to exactly what the future architecture would look like.

### MySQL and Service Layer
The MySQL Databases have the following sizes:  
gameday:  1750.44MB  
injuryfx: 77.20MB    
retro: 130.81MB

This contains data for all sources from 2009 to 2016, seven years of data in less than 2GB. MySQL is routinely used in production systems to store databases with up to 1TB of data. At our current ingestion rate MySQL should suffice for many years into the future unless the sources start producing much more data with each ingestion. The most likely aspect of the system that would need scaling is the web front end and its multiple concurrent accesses of MySQL. Since all of our analystics are done in realtime the MySQL server with enough traffic could see significant slow down. The site in its current incarnation doesn't require any ACID transactions nor state management; its basically a read only system, which MySQL is quite good at. But if the site did experience significant traffic, copies of the AMI could be spun up with a proxy server in front of all of them to distribute load across multiple servers. This approach would no longer be appropriate if the site were updated to maintain user state or start to require a non-trivial number of writes. If the real time analytics started to be a drag on the system even with smaller numbers of users we could preprocess injury windows results or cache the results as they're requested. If we expanded to more sports each could live on its own server and database so such an additional load wouldn't necessarily make our service layer more complex even as it made or ingestion layer more complex.


[Return to Documentation Index](index.md)

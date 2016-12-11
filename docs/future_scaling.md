# Future Scaling

### Ingestion Layer

InjuryFX has two ongoing data sources—the MLB transaction data, and the Gameday data, including PitchF/X. As such, the daily ingestion process is low volume, and takes no more than a few minutes. A full queueing or streaming ingestion system such as Storm or Kafka would be excessive.

We may add more baseball data sources, but even if we tripled the number of new sources, the ingestion process for a day would likely take under ten minutes to complete and remain batch appropriate.

The greatest impact to scale would be the public release of Statcast data, which uses an array of high speed cameras to track exact location and orientation of the ball and players at all times. This data is currently proprietary to the league, and would require more advanced aggregation technology such as Spark to manage. 

A more likely scenario that would require a more complex injection system is if we decided to expand the number of sports we analyzed. For instance, if we started tracking football, basketball, hockey, soccer, track & field, swimming, golf, tennis, etc with as much detail as we currently do with baseball, then a more advanced ingestion system would become appropriate. In this case we would potentially make use of a Kafka or Storm cluster to handle such an advanced ingestion from so many disparate services.

### MySQL and Service Layer

The MySQL Databases have the following sizes:  
gameday:  1750.44MB  
injuryfx: 77.20MB    
retro: 130.81MB

This contains data for all sources from 2009 to 2016, seven years of data in less than 2GB. MySQL is routinely used in production systems to store databases with up to 1TB of data. At our current ingestion rate MySQL should suffice for many years into the future unless the sources start producing much more data with each ingestion.

The most likely need for database scaling is in the read-only aggregations produced by the Flask front end. Since all of our analytics are done in real-time, with enough concurrent usage, the MySQL server could see significant slow down.

Since the writes to the system are low-volume and done in overnight batches, and there is no user state management, the system could easily scale to a single-master replication across multiple servers.

If user state information, such as saved analyses and user accounts, becomes a part of the application, a non-trivial number of writes would be needed, and a more complex replication setup may be required.

We have observed some slowness in the dynamic aggregation, particularly when integrating a combination of Retrosheet and Gameday data. If this becomes a significant problem at higher load, we may integrate pre-processed injury window results, or cache the results as they're requested.

If there is significant need to scale, we may also consider a move to [MySQL Cluster](MySQL Cluster: https://www.mysql.com/products/cluster/) or [Postgres Cluster](https://www.postgresql.org/docs/9.5/static/creating-cluster.html).

[Next > Sample Tools](sample_tools.md)  

[Return to Documentation Index](index.md)

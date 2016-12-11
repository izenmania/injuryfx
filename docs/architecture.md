# Architecture

![Architecture Diagram](images/architecture.jpg)

**Presentation Layer - Apache/Flask** 

- Justifications: Apache is the de facto open source standard for industrial strength security and performance in serving web pages. Flask allowed us to quickly put together a dynamic web site using the same programming language as our ingestion layer.
- Limitations: If the site sees high traffic volume, a single Apache instance could become a bottleneck. Future growth may necessitate a reverse proxy such as nginx to distribute traffic across multiple cloned web servers.

**Serving Layer - MySQL**

- Justifications: Some of our open source ingestion scripts, specifically py-gameday, are built with the assumption that you'll be importing your data into a MySQL database. After making this realization we did an analysis of features that we needed our database to support, specifically comparing MySQL with Postgres to see if it was worth rewriting parts of py-gameday to work with Postgres. Other than ingestion time we would not be doing a lot of writes to the database and we would not be doing ACID transactions. Mostly we will be performing parallel reads. This is the sort of tasks that MySQL shines at. We also considered database size. Our current DB didn't even reach 2GB; a size either MySQL or Postgres could handle. We do not have plans to do super advanced SQL queries so the subset of SQL supported by MySQL was sufficient for our needs. With all these facts in mind we opted to run MySQL rather than Postgres.
- Limitations: If we later implemented functionality that required ACID transaction and started to do a lot of writes then the performance and stability of MySQL might become a liability. With that in mind we developed our code in such a manner that the ingestion scripts and the presentation layer scripts did not access the database APIs directly but instead used a facade API. If we later change to Postgres the source code need only be updated in a small number of places.

**Python Ingestion Scripts with Batch Processing**

- Justifications: The ingestion scripts are written in Python for consistency across the application stack and because it's generally a great Data Science language. The ingestion is done in batches rather than in a more advanced queuing system like Storm or Kafka because there there are only two events per day and each take less than two minutes to run. There is no worry about the system running out of resources and not being able to keep up with intake data.
- Limitations: If we ever had a lot more data we would have to adjust this strategy. Given the state of open source sports data there currently isn't a lot of existing options for more data to ingest. See [Future Scaling](future_scaling.md) for an in depth discussion about vectors that could increase our ingestion rates as well as what we would do to compensate for that additional data flow.

**S3 Datalake**

- Justifications: In its current incarnation our data-lake is basically a backup store in case the data-sources ever disappear all together. The main requirement is that the data be resilient and accessible in the future. It will rarely, if ever be accessed, so speed of access is not a major factor of consideration.
- Limitations: Not the fastest data-lake implementation, but speed is nonessential for our proposed use.

[Return to Documentation Index](index.md)

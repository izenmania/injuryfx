# Architecture

![Architecture Diagram](images/architecture.jpg)

Presentation Layer - Apache/Flask 
- Justifications: Apache is the defacto open source standard for industrial strength security and performance in serving web pages. Flask allowed us to quickly put together a dynamic web site using the same programming language as our ingestion layer.
- Limitations: None that cause great worry. 

Serving Layer - MySQL 
- Justifications: Some of our open source ingestion scripts, specifically py-gameday, are built with the assumption that you'll be importing your data into a MySQL database. After making this realization we did an analaysis of features that we needed our database to support, specifically comparing MySQL with Postgres to see if it was worth rewriting parts of py-gameday to work with Postgres. Other than ingestion time we would not be doing a lot of writes to the database and we would not be doing ACID transactions. Mostly we will be performing parallel reads. This is the sort of tasks that MySQL shines at. We also considered database size. Our current DB didn't even reach 2GB; a size either MySQL or Postgres could handle. We do not have plans to do super advanced SQL queries so the subset of SQL supported by MySQL was sufficient for our needs. With all these facts in mind we opted to run MySQL rather than Postgres.
- Limitations: If we later implemented functionality that required ACID transaction and started to do a lot of writes then the performance and stability of MySQL might become a liability. With that in mind we developed our code in such a manner that the ingestion scripts and the presentation layer scripts did not access the database APIs directly but instead used a facade API. If we later change to Postgres the source code need only be updated in a small number of places.

Python Ingestion Scripts with Batch Processing
- Justifications:
- Limitations:

S3 Datalake
- Justifications: In its current incarnation our datalake is basically a backup store in case the datasources ever disapear all together. The main requirment is that the data be resilient and accessible in the future. It will rarely, if ever be accessed, so speed of access is not a major factor of consideration.
- Limitations: Not the fastest datalake implementation, but speed is not essention for our proposed use.

[Return to Documentation Index](index.md)

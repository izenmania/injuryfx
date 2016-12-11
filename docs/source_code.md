# Source Code Guide

In this document you'll find high level details about the source code directory structure.

### Directory: app
Contains Python files and static files used for configuration and running of Flask.

### Directory: aws
Contains Python files for connecting to aws services. 

### Directory: credentials
Contains Python and YAML files to config database and aws credentials.

### Directory: db
Contains Python files for connecting to and managing MySql database connections.

### Directory: docs
Contains markdown files describing the application.

### Directory: injury
Contains Python scripts for parsing the raw injuryfx data. Used in conjunction with the scripts directory.

### Directory: py-gameday
A near clone of py-gameday github repository with some minor changes to suit our specific import purposes.

### Directory: scripts
Contains Python files used in the ingestion of injuryfx data. Has dependencies on the "injury" directory.

### Directory: stats
Contains Python files that retrieve injury, game, pitch, atbat, and player data and converts it to useful and interesting displayable data, from stat splits to heat maps to pre and post injury pitch selection graphs. 

### Root Directory
Contains a couple files for bootstrapping the applications logging and configuration when Flask starts up.

[Next > Data Sources](datasources.md)  

[Return to Documentation Index](index.md)

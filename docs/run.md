# How to Run the Application

### Getting the Environment Setup

1. Start an AWS instance with the publicly available AMI named `InjuryFX-W205-Ubuntu-Final`. For the purposes of exploring the application the t2.large instance type is sufficient. Select your root drive size to be 80GB.
2. Use a security group with ports 80 and 22 open to any addresses that will be accessing the website and SSH.
3. Connect as the ubuntu user. This is the default user and is referenced in the "Connect" button for your instance in the AWS dashboard. Once logged in you'll be placed in `/home/ubuntu`.
4. Apache and MySQL start automatically so there is nothing to run.
5. Confirm you see injuryfx in the home directory. This is a clone of the main application repository.

All though the instance is available relativel quickly, we are taking advantage of caching features on MySQL that load at startup that prevent the system from performing quickly until after the caching service has completed. It's not a quick task; taking about ten minutes to complete. You can monitor the caching service progress at `/tmp/flask.log`. You can use the web tool prior to the caching completion but it will be slower.

### Test Flask

1. From your browser visit http://your.aws.url/ (It may take a minute for the first page to render while the system is starting up).
2. Confirm you see the home page graphic.
![Home Page Graphic](images/homepage.png)
3. Click the Players link at the top right.
4. You can view various players if you want to see the generated graphics and slash lines.

### Run an import

1. SSH to the ubuntu user on your AWS instance, and run `cd injuryfx`.
2. From the project folder, run `python scripts/transaction-daily-load.py`. This will detect the most recent data loaded into the system, and import from that day to current.

### Connect to the MySQL Database

1. run the command ```mysql -u root -p```.
2. Enter the password: ```w205ifx```
3. Databases of greatest interest: gameday, retrosheet, and injuryfx

[Next > Architecture](architecture.md)

[Return to Documentation Index](index.md)

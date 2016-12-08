# How to Run the Application

- Getting the Environment Setup 
  1. Start an AWS instance with the publicly available AMI named ```InjuryFX-W205-Final```. For the purposes of exploring the application the t2.large instance type is sufficiant. Select your root drive size to be 80GB.
  2. Make sure you open port 80 in your security group to everyone or at least your own IP address as part of your instance start up.
  3. Connect as the ubuntu user. This is the default user and is referenced in the "Connect" button for your instance in the AWS dashboard. Once logged in you'll be placed in ```/home/ubuntu```.
  4. Flask and MySQL start automatically so there is nothing to run.
  4. Confirm you see injuryfx in the home directory. This is a clone of this repository so that you don't have to clone it yourself.
- Test Flask
  1. From your browser visit http://your_aws_url/injury
  2. Confirm you see the home page graphic.
  3. Click the Players link at the top right.
  4. You can view various players if you want to see the generated graphics and slash lines.
- Run an import
  1. In your AWS terminal JOE ADD DIRECTIONS WHEN DONE 
- Connect to the MySQL Database
  1. run the command ```mysql -u root -p```.
  2. Enter the password: ```w205ifx```
  3. Databases of greatest interest: gameday, retrosheet, and injuryfx


[Return to Documentation Index](index.md)

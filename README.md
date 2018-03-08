# Devops challenge

## What

This contains python code that is run within a docker container.
The Code shows information of S3 buckets that are available on your AWS account.
The current project should be enough to give a basic idea of my engineering skill level.
There is definately room for improvement but due to my current (running) obligations I do not have to luxery to spent more time on this challenge...that being said, it was fun.
My own critisism/ todo:
   * use pandas lib/framework to model and query data, making the data model sortable and groupable
   * double check code
   * more testcases
   * integrate with logging /splunk/ graphana...maybe persist result for big data analysis to search for trends
   * need to know more about the AWS API, pretty sure it can be more efficient....this was my 1st playtime with AWS
   * abstracter, make code more maintainable, better documentation
   * secrets should be accessed via a vault (HSM solution)
   * results in webapp need to be json to html ..with nice CSS, so it can be sortable and groupable as well

# How 
   * Build the container with the following command: docker build -t [your desired dockername]:[your desired releasenr] .
   * Test if you can use the container and if the code is working:
      * docker run -e AWS_ACCESS_KEY_ID="YOUR SECRET ID GOES HERE" -e AWS_SECRET_ACCESS_KEY="YOUR SECRET PWD GOES HERE"  [NAME OF YOUR IMAGE:RELEASE]  /usr/bin/python3.5 devops_test/test_all.py
   * Test if you can use the cli
      * docker run -e AWS_ACCESS_KEY_ID="YOUR SECRET ID GOES HERE" -e AWS_SECRET_ACCESS_KEY="YOUR SECRET PWD GOES HERE"  [NAME OF YOUR IMAGE:RELEASE]  /usr/bin/python3.5 devops_backend/challenge.py [1st parameter is either: B KB MB GB] [2nd parameter should contain filer... '' takes all]
   * Test if you can use the web/ rest api
      * docker run -p 7777:7777 -e AWS_ACCESS_KEY_ID="YOUR SECRET ID GOES HERE" -e AWS_SECRET_ACCESS_KEY="YOUR SECRET PWD GOES HERE"  [NAME OF YOUR IMAGE:RELEASE]  /usr/bin/python3.5  devops_restwrapper/app.py
      * check if you can see the swagger API documentation: http://localhost:7777/api/
      * check the get buckinfo with the following link: http://localhost:7777/api/aws/bucketlister/list or curl -X GET --header 'Accept: application/json' 'http://localhost:7777/api/aws/bucketlister/list'

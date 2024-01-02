# Ride Pooling Cloud Application - RideShare


Developed the backend for a cloud based ​RideShare​ application​, ​that can be used to pool rides. The ​RideShare ​application allows the users to create a new ride if they are travelling from point A to point B. The application can: 
* Add a new user
* Delete an existing user
* Create a new Ride
* Search for an existing ride between a source and a destination
* Join an existing ride
* Delete a ride

<hr>

* Phase1:
  * Developed the backend processing of ​RideShare ​using REST APIs on EC2 AWS instance.
  * All endpoints were implemented using proper status codes
  * Deployed the Flask code using Gunicorn, running behind an NginX web server using WSGI


* Phase2:
  * The monolithic REST service created in Phase 1 is split up into two microservices​ - one catering to the user management, and another catering to the ride management.
  * These two microservices are started in separate docker containers, running on one AWS instance.
  * The microservices talk to each other via their respective REST interfaces.


* Phase3:
  * The two microservices (containers) are put into two different AWS EC2 instances.
  * Made them accessible from under the same public IP address and also the same port (80).
  * Used a load balancer supporting path-based routing (AWS Application Load Balancer) to distribute incoming HTTP requests to one of the two EC2 instances based on the URL route of the request.

Specifications of each phase can be found under the respective folders. 

# Where is my thief ![license][license-badge]
Welcome to the Where is my Thief project.
With this application you are able to create a ["My-Thief"-Tracker](./Tracker/README.md) which you may put on your bike or any other vehicle. This device sends its GPS-Data over to your ["Where is my Thief"-Backend](./Backend/README.md). There these data is stored and managed. You can view all these data wihtin the ["Where is my Thief"-Frontend"](./Frontend/README.md)

## Content
- [Where is my Thief-API](./API/README.md)
-- This API is a OpenAPI deinfiton which defines how to communicate to our Backend

- [Where is my Thief-Frontend](./Frontend/README.md) 
-- This part is an implementation which displays data from our Backend-Applicaiton

- [Where is my Thief-Backend](./Backend/README.md)
--This part of Where is my Thief implments all database and usermanagment stuff.

- [Where is my Thief-Server](./Server/README.md)
--This part unifies both our frontend and backend into asingle application.

- [My Thief-Tracker](./Tracker/README.md)
--This part gives all information on how to create your "My thief"-Device. It contains part 


## Launch
you can launch the whole system by doing following on your server launching this application:
- Install [mongoDB-Compass](https://www.mongodb.com/)
- Install [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/)
- once installed, run `docker-compose up` wihtin this repositories folder

## Contribution
If you want to contribute to this project look at each compontent on how to do this!

[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg

# TravelSalesman
## Installation and Deploying

Basically, docker will install and deploy everything, you don't need extra efford.

    docker-compose up

If you add new libraries into django, you should build Dockerfile again.

## How to Use
You can find TravelSalesman.postman_collection.json file in directory.
- import the file into Postman
- there is only one api with examples
- you can try those examples with different parameters.(i.e max_travel_distance or num_vehicles)

**IMPORTANT NOTE**: Response is just for developing purposes, just to see solution of problem.

## Test

If you want to test rest_api, you can list of container and exec bash, then you can run tests
    
    docker ps
    docker exec -ti <container_id_of_rest_api_image> bash
    python manage.py test

and for pubsub application test

    docker ps
    docker exec -ti <container_id_of_rest_api_image> bash
    python -m unittest tests.test

## Future Works

- Database can be implemented to store problems and solutions.
- Celery may be implemented to ensure no loss of solutions (Problem can have status, thus Celery can check if it is solved or still waiting).
- Optimization of TSP .
- Unittest coverage can be enhanced. 
- Authentication system can be implemented.
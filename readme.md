# Lendingblock Python Exercise
by [Tudor Munteanu](mailto:tudor@mowostudios.com)

# The Service

The intention was to keep the architecture of the service very basic and
have no external dependencies, even though deploying Flask would have been
much quicker.

I have always been curious about using the standard `http` module to run 
a simple HTTP server, so I took this opportunity to dive into this part of Python.

The logic for the endpoints can be found in `exchange.py`, the data models in `models.py` and misc helpers functions in `helpers.py`.

Start the service with:
```
python3 app.py
```

`requirements.txt` is not actually needed by the project.

## Tests
Using the standard `unittest` module, the tests cover the main API endpoints, as well
as some behaviour of the data models.

```
python3 exchange_test.py
```

## Caveats

Due to the very rudimentary HTTP server, URL routing is not as powerful as in Flask or
Django. This can be improved, if required.

Since no persistent database is used, the Storage class is only storing data in memory. Once the server is shut down, the created orders disappear.

# Docker

A very basic Docker container based on Ubuntu Xenial can be found in this project.
The App is mounted as an external volume, so code changes can be made without rebuilding the container.
To build the container, run:

```
./deploy/container/exercise/docker-build.sh
```
after which you can either run:
```
docker run -i -p 5000:8081 -v `pwd`:/app --entrypoint /app/docker-entrypoint.sh -t exercise:latest
```
or 
```
cd deploy
deploy-compose up
```

The development HTTP server is used currently, but in production we can configure uwsgi+nginx or gunicorn+nginx.

# Postman

Please import `Lendingblock.postman_collection.json` in Postman to manually run some tests on the endpoints. The URLs are pointing to the port 5000 exposed by the Docker container.

# Final note

There might be some CORS issues that are not handled by default in this exercise.

I was not sure what you meant by:

"Handling of orders which cross mid-price (for example buy 200 @ 20 and sell 50 @ 19)". I think it might be related to the logic used to aggregate the orderbook."

Any further clarifications are welcome.

Thank you,

Tudor

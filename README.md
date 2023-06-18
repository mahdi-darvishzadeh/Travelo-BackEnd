<h1 align="center">Travelo</h1>
<h1 align="center">Do not go alone with Travolo</h1>

#### Startup idea: 
A large number of people such as students, working people need to travel due to work and study issues
Constantly traveling between different cities. Due to the frequency of these trips, the cost of these trips with private vehicles is high
If the costs can be divided among different people, this trip can be done more economically.

#### Perspective: 
A program through which you can coordinate with different people who are all planning to travel to the same destination and with
The cost is lower than private taxis, he made this trip with a private vehicle.

#### Persona:
Mehdi, a computer engineering student at the university.

#### Story:
Mehdi returns to his hometown every year for vacation. But this time he had to come alone to see his family.
Mehdi is looking for a way to minimize his travel expenses. By searching the Internet, he found Travolo
came across and used the opportunity to travel to his destination city with another person.

#### scenario:
Mehdi enters the Travelo website and enters his travel information.
Travolo system finds another passenger traveling to the same destination.
Mehdi can check various travel suggestions, including departure date, price and car type.
After selecting another passenger, Mehdi will call him to check and plan the details of the trip.
After the final confirmation, Mahdi and another traveler travel to the destination city and after the end of the trip, they will give their opinions about
They share the journey with each other.

#### By using Travelo, Mehdi minimizes his travel expenses and also meets another person.

# Development usage
You'll need to have [Docker installed](https://docs.docker.com/get-docker/).
It's available on Windows, macOS and most distros of Linux. 

If you're using Windows, it will be expected that you're following along inside
of [WSL or WSL
2](https://nickjanetakis.com/blog/a-linux-dev-environment-on-windows-with-wsl-2-docker-desktop-and-more).

That's because we're going to be running shell commands. You can always modify
these commands for PowerShell if you want.


#### Clone this repo anywhere you want and move into the directory:

```sh
git clone https://github.com/mahdi-darvishzadeh/Travelo-BackEnd.git
```

#### Enviroment Varibales are included in docker-compose.yml file for debugging mode and you are free to change commands inside:

```docker
version: "3.9"

services:
  db:
    container_name: postgress_db
    image: postgres:13-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - envs/dev/db/.env
    restart: always

  backend:
    build:
      context: .
      dockerfile: dockerfiles/dev/django/Dockerfile
    container_name: django
    command: >
      sh -c "python manage.py makemigrations &&
             python manage.py migrate && 
             python manage.py create_superuser &&
             python manage.py check_database &&
             python manage.py trip_data_fa &&
             python manage.py gallary_data_fa &&
             python manage.py chat_data_fa &&
             python manage.py message_data_fa &&
             python manage.py notification_data_fa &&
             python manage.py runserver 0.0.0.0:8000"
    volumes:
      - ./core:/app
    ports:
      - "8000:8000"
    env_file:
      - envs/dev/django/.env
    restart: always

volumes:
  postgres_data:
```

#### Build everything:

*The first time you run this it's going to take 5-10 minutes depending on your
internet connection speed and computer's hardware specs. That's because it's
going to download a few Docker images and build the Python + requirements dependencies.*

```sh
docker compose up --build
```

Now that everything is built and running we can treat it like any other Django
app.

#### Swagger:
Enter the following url to access swagger

```url
http://localhost:8000/swagger
```

#### Admin-Panel:
Enter the following url to access the admin panel:

```url
http://localhost:8000/admin
```

#### Note:

If you receive an error about a port being in use? Chances are it's because
something on your machine is already running on port 8000. then you have to change the docker-compose.yml file according to your needs.
#### Check it out in a browser:

Visit <http://localhost:8000> in your favorite browser.

# Testing

To run the tests, type the following command in the terminal to run the program tests:

```sh
docker compose exec backend /bin/bash -c "pytest ."  
```
# End

You can use the following command to end the program:

```sh
docker compose down --volume  
```

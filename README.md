# Pokemon_api
Small Django + DRF application to show information about Pokémon

## Instructions for development:

#### 1. Create virtualenv:
```
mkvirtualenv pokemon_api
```
#### 2. Link project dir to postactivate:
```
setvirtualenvproject <project_dir>
```
#### 3. Clone the repository:
```
git clone https://github.com/ChronoFrank/pokemon_api.git 
```
#### 4. Install dependencies:
```
workon pokemon_api
pip install -r requirements.txt
```
#### 5. Migrate the database (PostgreSQL):

Switch to the `postgres` user.

```
sudo su postgres
```

Create database user `pokemon` with password `123456`.

```
createuser -U postgres -s -P pokemon
```

Create a database named `pokemons`.

```
createdb -U pokemon pokemons
```
Also you will need to create a 'settings_local.py' file in the path 
'mo_project/settings_local.py' to add the following configuration.

```
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2', # '.postgresql_psycopg2', '.mysql', or '.oracle'
        'NAME': 'pokemons',
        'USER': 'pokemon',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}
```


Then you can sync the database with your own user.

```
workon pokemon_api
python manage.py migrate
```

#### 6. Run tests to validate everything
```
workon pokemon_api
python manage.py test

# if we want to get the coverage report:
coverage run --source='.' manage.py test pokemon_api; coverage report
```
#### 7. Run the server:
```
$ python manage.py runserver
```

#### 8. Usage
The first thing to do is run a command to download and save information
about the pokemons base on the evolution chain.

the command will take an id argument that must be a number between 1 and 
467 according to the https://pokeapi.co/api/v2/evolution-chain/ count parameter

```
(pokemon_api)$ python manage.py  extract_evolution_chain 88
extracting evolution chain and pokemon information for id 88
Evolution chain -> https://pokeapi.co/api/v2/evolution-chain/88
retreving info for natu
https://pokeapi.co/api/v2/pokemon/natu/
{'pokemon_id': 177, 'name': 'natu', 'height': 2, 'weight': 20, 'hp': 40, 'attack': 50, 'defense': 45, 'special_attack': 70, 'special_defense': 45, 'speed': 70}
retreving info for xatu
https://pokeapi.co/api/v2/pokemon/xatu
{'pokemon_id': 178, 'name': 'xatu', 'height': 15, 'weight': 150, 'hp': 65, 'attack': 75, 'defense': 70, 'special_attack': 95, 'special_defense': 70, 'speed': 95}
All Done
```

to check the pokemon information you can check the following end-ponit

### REQUEST ###
curl --location --request GET 'http://localhost:8000/api/v1/pokemon/natu/'

### Response ###

```
{
    "pokemon_id": 177,
    "name": "natu",
    "height": 2,
    "weight": 20,
    "hp": 40,
    "attack": 50,
    "defense": 45,
    "special_attack": 70,
    "special_defense": 45,
    "speed": 70,
    "evolutions": [
        {
            "info": {
                "pokemon_id": 178,
                "name": "xatu",
                "evolution_type": "evolution"
            }
        }
    ]
}
```
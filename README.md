# poetry

pyproject.toml aanvullen met de nodige packages
    --> poetry install
Na de installatie is het bestand poetry.lock aangemaakt. Dit bestand bevat alle package afhankelijkheden.

De virtual environment staat in de folder "C:\Users\BartDewancker\AppData\Local\pypoetry\Cache\virtualenvs"
starten van de shell
    --> poetry shell
De virtual environment is nu zicht in de python environment manager.
Verlaten van de shell: exit
De shell kan ook vanuit de python environment manager herstart worden.

Updaten van dependencies
    --> poetry lock

Lokaal starten van de applicatie
    --> poetry run python main.py
of vanuit een poetry shell
    --> python main.py

toevoegen package, bv typings
resultaat te zien in de map C:\Users\BartDewancker\AppData\Local\pypoetry\Cache\virtualenvs\study-81wSHQNk-py3.10\Lib\site-packages en in het pyproject.toml bestand

    --> poetry add typings

verwijderen van een package, bv typings
    --> poetry run pip uninstall typings

# docker compose
Starten services:
    --> docker-compose up -d --build
    --> docker-compose -f docker-compose.admin.yml up -d --build

Stoppen services
    --> docker compose down

Een service rebuilden, bv video_api. Eerst de api container stoppen. Dan builden en herstarten met
    --> docker compose up -d --no-deps --build video_api



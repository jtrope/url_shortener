# url-shortner

## Installfest
### BE Dependencies
This project uses [pipenv](https://pipenv.readthedocs.io/en/latest/#install-pipenv-today) for dependency management. If using MacOS, you can install it with Homebrew
```bash
> brew install pipenv
``` 

Pipenv requires pip. You can check if you have it by running:
```bash
> pip --version
``` 

If you are missing pip you can install it by following
these [instructions](https://pip.pypa.io/en/stable/installing/)

To install the dependencies to run the BE run the following in the project root dir:
```bash
> pipenv install --dev
```

Finally, to ensure the database (using SQLite) is set up, run the migration like so:
```bash
> pipenv run python url_shortener/manage.py migrate
```


### FE Dependencies
To install the FE dependencies run:
```bash
> npm install
```

To create the JS bundle run:
```bash
> npm run build
```

## Starting the application
From the project root dir run:

```bash
pipenv run python url_shortener/manage.py runserver 3000
```

## Running tests
From the project root dir run:

```bash
pipenv run python url_shortener/manage.py test url_shortener/
```

## Project Structure
Django is organized around a project with multiple apps. The apps in this project are:
* [shortener](url_shortener/shortener/): API responsible for creating shortened
  urls and the handler for redirects to the expanded url
* [www](url_shortener/www/): Serves up the FE. JS lives [here](url_shortener/www/static/www/js/)


## TODO
* FE unittests
* Dockerize for easier installfest :)

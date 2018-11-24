# sse

Semantic Search Engine

## Idea

A biomedical semantic search engine using omop vocabularies.
The goal is to allow to search for specific entities in text.

![alt text](https://travis-ci.org/escodebar/sse.svg?branch_master)

## Setup Development

### API

To setup the API, create a Python virtual environment and install the backend.

```shell
$ git clone git@github.com/escodebar/sse.git && cd sse
$ python3 -m venv . && source bin/activate
$ (sse) python3 -m pip install -e . -r requirements.txt -c constraints.txt
$ (sse) python3 manage.py migrate
```

Then run the server with:
```shell
$ (sse) python3 manage.py runserver
```

# frontend

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run all tests
npm test
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

### Endpoints

Call the autocompletion endpoint with the following `CURL` command:
```shell
$ curl -H 'Content-Type: application/json;' --request POST --data '{"query": "As"}' "http://127.0.0.1:8000/api/autocompletion/"
```

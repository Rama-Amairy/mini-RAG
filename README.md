# mini-rag-application

Mini-application for RAG model for questions-answering

## Requirement

- python 3.8 or later


#### Install python using Miniconda

1) Download and install from [here]:

2) Create a new environment usind this command: 
```bash 
$ conda create -n mini-rag-app python=3.8 
```

3) Activit the environment: 
```bash
$ conda activate mini-rag-app
```


## Installtions

```bash
$ pip install -r requirement.txt
```

setup the environment variables:

```bash
$ cp .env.example .env 
```

set your environment variables in the `.env` file like your `OPEN_API_KEY` value.


## run the FAST API server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

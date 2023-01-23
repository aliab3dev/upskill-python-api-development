# Python API Development

### Project Description

Code accompanying the [Python API Development](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=66133s) YouTube course.

### Environment Setup

```
# create conda environment
> conda env create --name api python=3.10

# activate environment
> conda activate api

# install requirements
> pip install -r requirements.txt
```

### Server Setup 

```
uvicorn app.main:app --reload
```

### Database Migration Setup

```
# initialize alembic in a directory named alembic
alembic init alembic

# create manual revisions to db schemas
alembic revision -m "Create post table"

# upgrade/downgrade revision
alembic upgrade <revision, head, +1>
alembic downgrade <revision, -1,>

# navigate alembic
alembic history
alembic current
alembic heads

# create automatic revisions to db schemas 
# checks diff between target and current state: target_metadata = Base.metadata
alembic revision --autogenerate -m "Create posts, users and votes tables"
```


### Set Secret for JWT Generation
 ```
# generate random string to use in .env file for SECRET_KEY
openssl rand -hex 32 
```
# iris-fastapi-template

![fastapi_logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

## Description

This is a template for a FastApi application that can be deployed in IRIS as an native Web Application.

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install the requirements
4. Run the docker-compose file

```bash
git clone
cd iris-fastapi-template
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
docker-compose up
```

## Usage

The base URL is `http://localhost:53795/fastapi/`.

### Endpoints

- `/iris` - Returns a JSON object with the top 10 classes present in the IRISAPP namespace.
- `/interop` - A ping endpoint to test the interoperability framework of IRIS.
- `/posts` - A simple CRUD endpoint for a Post object.
- `/comments` - A simple CRUD endpoint for a Comment object.

## How to develop from this template

See WSGI introduction article: [wsgi-introduction](https://community.intersystems.com/post/wsgi-support-introduction).

TL;DR : You can toggle the `DEBUG` flag in the Security portal to make changes to be reflected in the application as you develop.

## Code presentation

### `app.py`

This is the main file of the FastAPI application. It contains the FastAPI application and the routes.

```python
from fastapi import FastAPI, Request

import iris

from iop import Director

# import models
from models import Post, Comment, init_db
from sqlmodel import Session,select

app = FastAPI()

# create a database engine
url = "iris+emb://IRISAPP"
engine = init_db(url)
```

- `from fastapi import FastAPI, Request` - Import the FastAPI class and the Request class.
- `import iris` - Import the IRIS module.
- `from iop import Director`: Import the Director class to bind the flask app to the IRIS interoperability framework.
- `from models import Post, Comment, init_db` - Import the models and the init_db function.
- `from sqlmodel import Session,select` - Import the Session class and the select function from the sqlmodel module.
- `app = FastAPI()` - Create a FastAPI application.
- `url = "iris+emb://IRISAPP"` - Define the URL of the IRIS namespace.
- `engine = init_db(url)` - Create a database engine for the sqlmodel ORM.

### `models.py`

This file contains the models for the application.

```python
from sqlmodel import Field, SQLModel, Relationship, create_engine

class Comment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    content: str
    post: "Post" = Relationship(back_populates="comments")

class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    comments: list["Comment"] = Relationship(back_populates="post")
```

Not much to say here, just the definition of the models with foreign keys and relationships.

The `init_db` function is used to create the database engine.

```python
def init_db(url):

    engine = create_engine(url)

    # create the tables
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    # initialize database with fake data
    from sqlmodel import Session

    with Session(engine) as session:
        # Create fake data
        post1 = Post(title='Post The First', content='Content for the first post')
        ...
        session.add(post1)
        ...
        session.commit()

    return engine
```

- `engine = create_engine(url)` - Create a database engine.
- `SQLModel.metadata.drop_all(engine)` - Drop all the tables.
- `SQLModel.metadata.create_all(engine)` - Create all the tables.
- `with Session(engine) as session:` - Create a session to interact with the database.
- `post1 = Post(title='Post The First', content='Content for the first post')` - Create a Post object.
- `session.add(post1)` - Add the Post object to the session.
- `session.commit()` - Commit the changes to the database.
- `return engine` - Return the database engine.

### `/iris` endpoint

```python
######################
# IRIS Query example #
######################

@app.get("/iris")
def iris_query():
    query = "SELECT top 10 * FROM %Dictionary.ClassDefinition"
    rs = iris.sql.exec(query)
    # Convert the result to a list of dictionaries
    result = []
    for row in rs:
        result.append(row)
    return result
```

- `@app.get("/iris")` - Define a GET route for the `/iris` endpoint.
- `query = "SELECT top 10 * FROM %Dictionary.ClassDefinition"` - Define the query to get the top 10 classes in the IRIS namespace.
- `rs = iris.sql.exec(query)` - Execute the query.
- `result = []` - Create an empty list to store the results.
- `for row in rs:` - Iterate over the result set.
- `result.append(row)` - Append the row to the result list.
- `return result` - Return the result list.

### `/interop` endpoint

```python
########################
# IRIS interop example #
########################
bs = Director.create_python_business_service('BS')

@app.get("/interop")
@app.post("/interop")
@app.put("/interop")
@app.delete("/interop")
def interop(request: Request):
    
    rsp = bs.on_process_input(request)

    return rsp

```

- `bs = Director.create_python_business_service('BS')` - Create a Python business service.
  - Must be created outside the route definition to prevent multiple instances of the business service.
- `@app.get("/interop")` - Define a GET route for the `/interop` endpoint.
- `@app.post("/interop")` - Define a POST route for the `/interop` endpoint.
- ...
- `def interop(request: Request):` - Define the route handler.
- `rsp = bs.on_process_input(request)` - Call the `on_process_input` method of the business service.
- `return rsp` - Return the response.

### `/posts` endpoint

```python
############################
# CRUD operations posts    #
############################

@app.get("/posts")
def get_posts():
    with Session(engine) as session:
        posts = session.exec(select(Post)).all()
        return posts
    
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        return post
    
@app.post("/posts")
def create_post(post: Post):
    with Session(engine) as session:
        session.add(post)
        session.commit()
        return post
```

This endpoint is used to perform CRUD operations on the `Post` object.

Note much to say here, just the definition of the routes to get all posts, get a post by id, and create a post.

Everything is done using the sqlmodel ORM.

### `/comments` endpoint

```python
############################
# CRUD operations comments #
############################


@app.get("/comments")
def get_comments():
    with Session(engine) as session:
        comments = session.exec(select(Comment)).all()
        return comments
    
@app.get("/comments/{comment_id}")
def get_comment(comment_id: int):
    with Session(engine) as session:
        comment = session.get(Comment, comment_id)
        return comment
    
@app.post("/comments")
def create_comment(comment: Comment):
    with Session(engine) as session:
        session.add(comment)
        session.commit()
        return comment
```

This endpoint is used to perform CRUD operations on the `Comment` object.

Note much to say here, just the definition of the routes to get all comments, get a comment by id, and create a comment.

Everything is done using the sqlmodel ORM.

## Troubleshooting

### How to run the FastAPI application in a standalone mode

You can always run a standalone Flask application with the following command:

```bash
python3 /irisdev/app/community/app.py
```

NB : You must be inside of the container to run this command.

```bash
docker exec -it iris-fastapi-template-iris-1 bash
```

### Restart the application in IRIS

Be in `DEBUG` mode make multiple calls to the application, and the changes will be reflected in the application.

### How to access the IRIS Management Portal

You can access the IRIS Management Portal by going to `http://localhost:53795/csp/sys/UtilHome.csp`.

### Run this template locally

For this you need to have IRIS installed on your machine.

Next you need to create a namespace named `IRISAPP`.

Install the requirements.

Install IoP :

```bash
#init iop
iop --init

# load production
iop -m /irisdev/app/community/interop/settings.py

# start production
iop --start Python.Production
```

Configure the application in the Security portal.

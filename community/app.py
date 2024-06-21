from fastapi import FastAPI, Request

import iris

from grongier.pex import Director

# import models
from models import Post, Comment, init_db
from sqlmodel import Session,select

app = FastAPI()

# create a database engine
url = "iris+emb://IRISAPP"
engine = init_db(url)

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

######################
# SQLModel example   #
######################

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
    
@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        post.title = post.title
        post.content = post.content
        session.commit()
        return post
    
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        session.delete(post)
        session.commit()
        return {"message": "Post deleted successfully"}
    
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
    
@app.put("/comments/{comment_id}")
def update_comment(comment_id: int, comment: Comment):
    with Session(engine) as session:
        comment = session.get(Comment, comment_id)
        comment.content = comment.content
        session.commit()
        return comment
    
@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int):
    with Session(engine) as session:
        comment = session.get(Comment, comment_id)
        session.delete(comment)
        session.commit()
        return {"message": "Comment deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=2188)


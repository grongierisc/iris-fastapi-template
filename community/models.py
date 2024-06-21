# create sqlmodel for post and comment

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
        post2 = Post(title='Post The Second', content='Content for the Second post')
        post3 = Post(title='Post The Third', content='Content for the third post')

        comment1 = Comment(content='Comment for the first post', post=post1)
        comment2 = Comment(content='Comment for the second post', post=post2)
        comment3 = Comment(content='Another comment for the second post', post=post2)
        comment4 = Comment(content='Another comment for the first post', post=post1)

        # Add the data to the session
        session.add(post1)
        session.add(post2)
        session.add(post3)
        session.add(comment1)
        session.add(comment2)
        session.add(comment3)
        session.add(comment4)

        # Commit the session
        session.commit()

    return engine


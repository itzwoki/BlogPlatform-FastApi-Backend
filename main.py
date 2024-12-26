from fastapi import FastAPI

from db.db_setup import engine
from db.models import comment, post, user


user.Base.metadata.create_all(bind=engine)
post.Base.metadata.create_all(bind=engine)
comment.Base.metadata.create_all(bind=engine)


app=FastAPI(
    title="FAST API BLOG",
description="Blog Post Application.",
contact={
    "name": "M.Waqas",
    "email": "abdullahwaqas22@gmail.com"

},
license_info={
    "name": "Associate Software Engineer"
}
)


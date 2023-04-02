from fastapi import FastAPI
import uvicorn
#import routers
from api.user import user_router
from api.contacts import contact_router
#import engine
from db import engine, Base





app = FastAPI(
    title="Fast API LMS",
    description="for managing user and contacts.",
    version="0.0.1",
    contact={
        "name": "ismail",
        "email": "eyi201201@gmail.com",
    },
    license_info={
        "name": "",
    },
) 

# creating the database connections
Base.metadata.create_all(engine)

#register the routers
app.include_router(user_router)
app.include_router(contact_router)

# connect flask
# from fastapi.middleware.wsgi import WSGIMiddleware
# from web_app.app import flask_app
# app.mount("/flask_app", WSGIMiddleware(flask_app))

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional 
from random import randrange

app  = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

# Array contain a bunsh of Post objects represented as dict 

my_posts = [{"title": "title of post 1", 
             "content": "content of post 1",
             "id": 1},
            {"title": "title of post 2", 
             "content": "content of post 2",
             "id": 2},
            {"title": "title of post 3", 
             "content": "content of post 3",
             "id": 3}]

def find_posts(id: int)-> dict:
    for p in my_posts: 
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id: 
            return i 
@app.get("/")
def root():
    return {"message":"Hello, World!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts} # serialize post containter to Json

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict} 

@app.get("/posts/latest") # order matters , before id to not cause type issues
def get_latest_post(): 
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

@app.get("/posts/{id}") # {id}: id is a path parameter, returned as str
def get_post(id: int, response: Response):
    post = find_posts(id) # cast to int or use a hint
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} doesn't exist!")
        # HARD CODE / status value response.status_code = 404 , or : 
        #response.status_code = status.HTTP_404_NOT_FOUND
        # HARD CODE / return {"message": f"post with id: {id} doesn't exist!"}
    return {"post_detail":post}


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    #find index in the array that has required ID
    #my_posts.pop(index)
    index = find_index_post(id)
    if index == None : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist!")
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist!")
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}    
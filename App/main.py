import time 
from typing import Optional
from fastapi import FastAPI,HTTPException,status,Response,Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2 as db
from psycopg2.extras import RealDictCursor
from fastapi.middleware.cors import CORSMiddleware
from functions import Func as fc
from . import model
from .database import engine,SessionLocal
from sqlalchemy.orm import Session

# All functions
#----------------------------------------end-------------------------------------------

model.Base.metadata.create_all(bind=engine)

#App
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = ["*"]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


while True:
    try :
        connection = db.connect(host='localhost',database="LogBook",user="postgres",
        password="goodmorning003".upper(),cursor_factory=RealDictCursor,port=1234)
        cursor=connection.cursor()
        print ("Connection Was Success")
        print(fc.get_One(cursor,'12'))
        break
    except Exception as err:
        print("Error in connection")
        print("Eror is",err)
        time.sleep(5)

allPosts=[{"title":"Before Update","content":"Before Update","id":2}]


class Schema(BaseModel):
    title:str
    content:str
    published:Optional[bool]=True

#All Routes

@app.get("/")
def read_root():
    
    return {"Hello": "World"}

@app.get('sql')
def sql( db: Session = Depends(get_db)):
    return {"sts":"done"}
    
@app.get("/posts")
def send():
    cursor.execute("SELECT * FROM posts")
    re=cursor.fetchall()
    if len(re)==0:
        return {"msg":"No data updated yet"}
    return {"data":re}

@app.post('/uploadposts')
def posts(data:Schema=Body(...) ):  
    result=fc.pushData(cursor,data.dict())
    connection.commit()
    return {"response":result,"uplodedata":data.dict()}

@app.get("/posts/{id}")
def get_data(id:int):
    cursor.execute("SELECT * FROM posts where id = %s ",(str(id),))
    result=cursor.fetchone()
    print('re=',result)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the data with the given id {id} was not found")
    return {'result':result}
    # return {"data":reqData}

@app.get('/latestposts')
def get():
    return fc.get_latest(cursor)

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int):
    cursor.execute("delete from posts where id=%s returning *;",(str(id),))
    re=cursor.fetchone()
    connection.commit()
    print(re,type(re))
    # if type(re)==None:
    if re!=None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,detail="Already Item Got deleted")
    
    
    
@app.put('/posts/{id}')    
def Update(id:int,content:Schema=Body(...)):
    try:
        data=content.dict()
        cursor.execute("UPDATE posts SET title =%s, content = %s,published=%s WHERE id=%s returning *;",(data['title'],data['content'],data['published'],str(id)))
        connection.commit()
        msg=cursor.fetchone()
        return {"message":msg}
    except Exception as err:
        return {"res":err}
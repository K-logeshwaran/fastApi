def update(Sdata:dict,id:int,allData:list):
    for  d in allData:
        print(f" id of d ={d['id']}")
        print(f" given id  ={id}")
        print(id==d['id'])
        print(f" type of id ={type(id)}")
        print(f" type of d[id] ={type(d['id'])}")
        if d['id']==id:
            print('yes')
            d["title"]=Sdata["title"]
            d["content"]=Sdata["content"]
            return {"Status":"Success"}
        
    else:
        return "Failed" 

def pushData(cursor,data:dict):
    try :
        print(data['title'])
        sqlCm= f"""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s); """
        print(sqlCm)
        cursor.execute(sqlCm,(data['title'],data['content'],data['published']))
        return "data Uploded Successfully"
    except Exception as err:
        return {f"Error is {err}"}

def get_One(cursor,id):
    try :
        cursor.execute("""SELECT title FROM posts where id =(%s);""",(id))
        result=cursor.fetchone()
        print('re=',result)
        return {'result':result}
    except Exception as err:
        return None

def get_latest(cursor):
    try :
        sqlCommand="""SELECT * FROM posts ORDER BY id desc"""
        cursor.execute(sqlCommand)
        re=cursor.fetchone()
        if not re :
            return {'msg':"No data updated yet"}
        return {'data':re}
    except Exception as err:
        return {
            "msg":err
        }    

from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel

app=FastAPI()

@app.get("/health")

def health():
    return {"status":"ok"}

tasks=[]
next_id=1
class Task(BaseModel):
    title:str
@app.post("/tasks",status_code=status.HTTP_201_CREATED)

def create_task(data:Task):

    global next_id

    title=data.title.strip()

    if not title:
        raise HTTPException(status_code=422,detail="Title cannot be empty")
    for task in tasks:
        if title == task["title"]:
            raise HTTPException(status_code=409,detail="Title already exists")
    
    new_task={
        "id":next_id,
        "title":title
    }

    next_id+=1

    

    tasks.append(new_task)

    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id:int,data:Task):

    title=data.title.strip()

    if not title:
        raise HTTPException(status_code=422,detail="empty title")
    
    for task in tasks:
        if task["id"] != task_id and task["title"] == title:
            raise HTTPException(status_code=409, detail="Title Already exists")
  
    for task in tasks:
        if  task["id"]==task_id:
            task["title"]=title
            return task
        
        
    raise HTTPException(status_code=404,detail="Task not found")


@app.delete("/tasks/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def del_task(task_id:int):

    for i,task in enumerate(tasks):
        if task["id"]==task_id:
            del tasks[i]
            return

    raise HTTPException(status_code=404,detail="Task not found")
    


@app.get("/tasks")

def list_tasks():
    return tasks

@app.get("/tasks/{task_id}")

def get_task(task_id:int):
    for task in tasks:
        if task["id"]==task_id:
            return task
    
    raise HTTPException(status_code=404,detail="Task not found")



     


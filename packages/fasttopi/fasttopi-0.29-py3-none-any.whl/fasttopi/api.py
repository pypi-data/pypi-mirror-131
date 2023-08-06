from fastapi import FastAPI, Query
from model import *
from  config import *
app = FastAPI()




def create_model():
    path_model=get_path_model("model")
    model=load_model(path_model)
    return model

model =  create_model()

@app.get("/categories/")
def read_item(title: str = Query("no-title",min_length=7,max_length=100)):
    category = predict_title(model,title)
    return {"category":category}
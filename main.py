from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Optional, Annotated

app = FastAPI()

notebook = []

class Note(BaseModel):
    name:str
    company:Optional[str] = None
    phone:str
    email:str
    birthdate:Optional[str] = None
    photo:Optional[str] = None

@app.get('/api/v1/notebook/')
def get_notebook(page: int = Query(1, ge=1), per_page: int = Query(10, ge=1)) -> List[Note]:
    start = (page - 1) * per_page
    end = start + per_page
    return notebook[start:end]

@app.post('/api/v1/notebook/')
def add_note(note: Note) -> Note:
    new_note = note.dict()
    new_note['id']=notebook[-1]['id']+1 if notebook else 1
    notebook.append(new_note)
    return new_note

@app.get('/api/v1/notebook/{id}/')
def get_note(id: int):
    for note in notebook:
        if note['id']==id:
            return note
    raise HTTPException(status_code=404, detail="Note doesn't exist")

@app.post('/api/v1/notebook/{id}/')
def refresh_note(id: int, renewed_note: Note) -> Note:
    for note in notebook:
        if note['id']==id:
            note.update(renewed_note)
            return note
    raise HTTPException(status_code=404, detail="Note doesn't exist")

@app.delete('/api/v1/notebook/{id}/')
def delete_note(id: int):
    for note in notebook:
        if note['id']==id:
            notebook.remove(note)
    raise HTTPException(status_code=404, detail="Note doesn't exist")
import chunk
import io
import os
import shutil
from typing import Annotated
from db import get_db, Files, FileChunk
from sqlalchemy.orm import Session
from file_parser import FileParser
from background_tasks import TextProcessor, client
from sqlalchemy import select
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, BackgroundTasks

app = FastAPI()


class QuestionModel(BaseModel):
    question: str


@app.get("/")
def root():
    return "Hello RAG"


@app.post("/uploadfile")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile, db: Session = Depends(get_db)):
    allowed_extensions = ["txt", "pdf"]
    file_extension = file.filename.split('.')[-1]
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed")

    folder = "sources"
    try:
        os.makedirs(folder, exist_ok=True)

        file_location = os.path.join(folder, file.filename)
        file_content = await file.read()
        with open(file_location, "wb+") as file_object:
            file_like_object = io.BytesIO(file_content)
            # for secure file writing
            shutil.copyfileobj(file_like_object, file_object)

        content_parser = FileParser(file_location)
        file_text_content = content_parser.parse()
        new_file = Files(file_name=file.filename, file_content=file_text_content)
        db.add(new_file)
        db.commit()
        db.refresh(new_file)

        # background job for file content
        background_tasks.add_task(TextProcessor(db, new_file.file_id).chunk_and_embed, file_text_content)

        return {"info": "File saved", "filename": file.filename}

    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Error saving file")


@app.post("/find-similar-chunks/{file_id}")
async def find_similar_chunks(file_id: int, question_date: QuestionModel, db: Session = Depends(get_db)):
    try:
        question = question_date.question
        response = client.embeddings.create(input=question, model="text-embedding-ada-002")
        question_embedding = response.data[0].embedding

        # find
        similar_chunks_query = select(FileChunk).where(FileChunk.file_id == file_id)\
            .order_by(FileChunk.embedding_vector.l2_distance(question_embedding)).limit(10)
        similar_chunks = db.scalars(similar_chunks_query).all()

        formatted_response = [
            {"chunk_id": chunk.chunk_id, "chunk_text": chunk.chunk_text}
            for chunk in similar_chunks
        ]

        return formatted_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

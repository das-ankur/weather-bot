from fastapi import FastAPI
from pydantic import BaseModel
from chat import chat


# Create an instance of FastAPI
app = FastAPI()

# Define a Pydantic model for the input
class Message(BaseModel):
    text: str

# Define a POST endpoint to accept the string input
@app.post("/weather_bot/")
async def process_string(message: Message):
    response = chat(message.text)
    return {"response": response}

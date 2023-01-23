
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import openai
import pandas as pd
app = FastAPI()
import os
#with open('openaiapikey.txt', 'r') as infile:
#       openai.api_key = infile.read()
openai.api_key = os.environ['openai_key']
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("")
async def generate_text(prompt: str):
    with open('prompt_script.txt', 'r') as infile:
        prompt = infile.read().replace('<<ED>>', prompt)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt
    )
    completion = response["choices"][0]["text"]
    lines = completion.split("\n")
    lines = [line for line in lines if line]
    data = {}
    for line in lines:
        parts = line.split(":")

        key = parts[0].strip()
        value = parts[1].strip()

        data[key] = value
    json_data = json.dumps(data)
    return json_data

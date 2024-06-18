#server code for classification LLM
from fastapi import FastAPI
from pydantic import BaseModel

from lib.mistralai import load_model
from lib.messages import format_model_input, infer_response, process_response

model_path = './mistral_7B/mistral_model_v0.2'
tokenizer_path = './mistral_7B/mistral_tokenizer_v0.2'

model, tokenizer = load_model(
    model_path=model_path,
    tokenizer_path=tokenizer_path
)

app = FastAPI()

class Data(BaseModel):
    data: str

def call_model(data: str):
    #translation section
    translatation_encoded = format_model_input(
        input=data,
        tokenizer=tokenizer,
        mode='translation'
    )

    translation_decoded = infer_response(
        model=model,
        tokenizer=tokenizer,
        encoded=translatation_encoded
    )

    translation = process_response(translation_decoded)

    #classification section
    classification_encoded = format_model_input(
        input=translation,
        tokenizer=tokenizer,
        mode='classification'
    )

    classification_decoded = infer_response(
        model = model,
        tokenizer=tokenizer,
        encoded=classification_encoded
    )

    classification = process_response(classification_decoded)

    return classification

@app.post("/classify")
async def classify(data: Data):
    category = call_model(data.data)
    return {
        'category' : category
    }
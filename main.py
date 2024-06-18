from lib.mistralai import load_model
from lib.messages import format_model_input, infer_response, process_response

model_path = './mistral_7B/mistral_model_v0.2'
tokenizer_path = './mistral_7B/mistral_tokenizer_v0.2'

model, tokenizer = load_model(
    model_path=model_path,
    tokenizer_path=tokenizer_path
)


from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

def load_model(model_path, tokenizer_path):
    """
    to initialize the model that is save locally

    Params : {
        model_path (str) : mistral model's path,
        tokenizer_path (str) : mistral tokenizer's path
    }

    Returns : {
        model (transformers.AutoModelForCausalLM) : mistralai model,
        tokenizer (transformers.AutoTokenizer) : mistralai tokenizer
    }
    """
    # define model configuration with the purpose of qunatization and loading the model in 4-bit
    quantization_config = BitsAndBytesConfig(load_in_4bit=True,
                                            llm_int8_threshold=200.0,
                                            bnb_4bit_use_double_quant=True,
                                            bnb_4bit_quant_type="nf4",
                                            bnb_4bit_compute_dtype=torch.bfloat16
                                            )
    
    #load locally saved model
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype = torch.float16,
        quantization_config = quantization_config,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

    #return the model along with tokenizer
    return model, tokenizer

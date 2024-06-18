from lib.preprocess import preprocess_response, remove_outside_curly_braces, remove_symbols, extract_text
import json

def format_model_input(input, tokenizer, mode):
    """
    Format the input data for the model, to create a message that is to be passed to the model for inference.
    The model would need to translate the input data first and then infer the class, thus at the function creates two separate
    message template.
    mode = 'translation' | 'classification'

    Params : {
            input (str) : input data, whether translated text or untranslated text,
            tokenizer (transformers.AutoTokenizer) : tokenizer for the model,
            mode (str) : 'translation' | 'classification'
        }
    
    Returns : encoded (str) : input properly formatted for mistralai's input
    """
    # check the mode, should be either 'translation' or 'classification'
    if mode == 'translation' or mode == 'classification':
        if mode == 'classification':
            # system prompt and user input for classification task
                message = f"""
                            text: '{input}' , this is the text containing a problem, categorize this problem.
                            preprocessing : the text is translated beforehand, so it could contain explanation about translation, ignore it and just understand the context of problem
                        """

                sys_prompt = """You are a helpful, intelligent classifier. You will be doing task as a ticket classifier in a bank located in Nepal. you will only be giving response to client, without any explanation,
                                with one of the following classes :
                                ['Block/Unblock', 'Others', 'Password/PIN Reset', 'Registration', 'Renewal', 'Transaction Pending', 'Transaction Failure', 'VKYC']
                                some information :
                                    Renewal means problem related to account renewal.
                                    Registration means problem related to new registration.
                                    Transaction Pending means problem mentioning transaction not completing and 'transaction is pending' is shown to the user, "pending" should be mentioned to be categorized as this.
                                    Transaction Failure means the problem is related to failed transaction, it means purely unable to complete or process a transaction.
                                    Block/Unblock means problem related to blocked account, request to unblock account, account blocked due to many wrong password/PIN try.
                                    Password/PIN Reset means problem related pin/password reset requests.
                                    Others means any problem outside this categories.
                                    VKYC, if the client is requesting "any kind of service", which would also include categories mentioned before this, from outside the country Nepal.
                                output_format: JSON
                                    {
                                        "prediction" : "your final prediction",
                                        "explanation" : "your explanation here"
                                    }
                                advice to you:
                                    you are not expected to provide any justification and explanation and you should not as well.
                                    don't write anything outside the output_format at any cost, everything should be within { and }.
                                    if you explain, explain in designated place "explanation" as mentioned in output_format.
                                    don't include double quotation within the explanation value.
                            """
        else:
            #system prompt and user prompt for translation
            sys_prompt="""You are a helpful, intelligent translator. The text may contain nepali roman english or english text.Please translate it to understandable pure english text
                            output_format:
                                {
                                    "prediction" : "your final english translated text, strictly just translation only",
                                    "note" : "your opinion here"
                                }
                            advice to you:
                                please don't include double quotation within the explanation and prediction value.
                                you are not expected to provide any justification and explanation and you should not as well.
                                Strictly enforce the policy to not write anything outside the output_format { and }.
                                provide pure translation, no explanation or any sort within the translated text as well.
                        """
            message =f"""
                        text : {input}
                      """
        prefix = "<|im_start|>"
        suffix = "<|im_end|>\n"
        sys_format = prefix + "system\n" + sys_prompt + suffix
        user_format = prefix + "user\n" + message + suffix
        input_text = sys_format + user_format
        messages = [
            {
                'role':'user',
                'content': input_text
            }
        ]
        encoded = tokenizer.apply_chat_template(
            messages,
            return_tensors='pt'
        )
        return encoded
    else:
        print('Pass proper mode, either "translation" or "classification"')
        return None
    
def infer_response(model, tokenizer, encoded):
    """
    This function takes the model, tokenizer and encoded input and returns the response.

    Params : {
        model (transformers.AutoModelForCausalLM) : mistralai model,
        tokenizer (transformers.AutoTokenizer) : tokenizer for the model,
        encoded (str) : input encoded to match model's input
    }

    Returns : decoded (str) : full response from the model
    """

    # infer using model using the encoded user promt
    generated_id = model.generate(
        encoded,
        max_new_tokens = 1000,
        do_sample=True
    )
    decoded = tokenizer.batch_decode(generated_id)[0]
    # print(f'from lib : {decoded}')
    decoded = preprocess_response(decoded)
    return decoded

def process_response(decoded):
    """
    Processing the model's output

    Params : decoded (str) : mistralai model's full response

    Returns : response (str) : extracted response with some preprocessing
    """
    temp = extract_text(decoded)
    temp = remove_outside_curly_braces(temp)
    temp = remove_symbols(temp)
    try:
        temp = json.loads(temp)
        return temp['prediction']
    except Exception as e:
        print('JSON load failed.')
        print(e)
        return None

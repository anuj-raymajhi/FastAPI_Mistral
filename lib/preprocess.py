import string
import json
import re


def preprocess_text(text):
    """
    Preprocesses text by converting to lowercase and removing punctuation efficiently,
    while keeping spaces intact.

    Args:
        text: The text to preprocess.

    Returns:
        The preprocessed text as a single string.
    """
    # Define punctuation characters to remove (excluding spaces)
    remove_chars = string.punctuation

    # Create translation table: maps each punctuation character to None (i.e., it will be removed)
    table = str.maketrans('', '', remove_chars)

    # Apply translation table, convert to lowercase in one go
    preprocessed_text = text.translate(table).lower()
    preprocessed_text = preprocessed_text.replace('\n', ' ')
    return preprocessed_text

def remove_mail_links(text):
    """
    Removes email addresses and URLs from the text.

    Params : text (str)

    Returns : text (str)
    """
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    return text

def remove_numbers(text):
    """
    To remove numbers from the text.

    Params : text (str)

    Returns : text (str)
    """
    temp = ''.join([i for i in text if not i.isdigit()])
    return temp

def preprocess_response(text):
    """
    Simple function to remove extra spaces in the text

    Params : text (str)

    Return : cleaned_string (str)
    """
    # Splitting the string into words
    words = text.split()

    # Joining the words back together without extra spaces
    cleaned_string = " ".join(words)
    return cleaned_string


def extract_text(input_string):
    """
    Specifically to extract the response part from the mistralai model's output, which is wrapped in ... [/INST] ... </s>

    Params : input_string (str)

    Returns : text (str) -> which is a response
    """
    # print('from preprocess :\n\t',type(input_string))
    pattern = r'\[\/INST\](.*?)<\/s>'
    match = re.search(pattern, input_string)
    if match:
        return match.group(1).strip()
    else:
        print("The response couldn't be extracted.")
        return None
    

def remove_outside_curly_braces(input_string):
    """
    To extract the JSON only part from the response

    Params : input_string (str)

    Returns : text (str) -> wrapped in {}
    """
    inside_curly_braces = False
    result = ''
    lastCharIndex = len(input_string) - 1
    for index,char in enumerate(input_string):
        if char == '{':
            inside_curly_braces = True
        elif char == '}':
            inside_curly_braces = False
            result += char
            break
        if inside_curly_braces:
            result += char
        if index == lastCharIndex:
            if char != '}':
                result += '}'

    return result

def remove_symbols(json_string):
    """
    To remove symbols from the response that poses problem during json conversion

    Params : json_string (str)

    Returns : cleaned_string (str) -> most likely to be translated to JSON
    """
    # List of problematic symbols
     # List of problematic symbols
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '.', '_', '/', '\n','\\',]
    
    # Escape problematic symbols for use in regex
    symbols_regex = '[' + re.escape(''.join(symbols)) + ']'
    
    # Replace problematic symbols with an empty string
    cleaned_string = re.sub(symbols_regex, '', json_string)
    
    return cleaned_string


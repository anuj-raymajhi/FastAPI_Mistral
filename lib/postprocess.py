import string
import json
import re

# Dictionary to map specific replacements
replacements = {
    'TransactionFailure': 'Transaction Failure',
    'PasswordPINReset': 'Password PIN Reset',
    'BlockUnblock': 'Block/Unblock',
    'TransactionRenewal': 'Renewal',
}

# List of final output category
cat = ['BlockUnblock', 'Others', 'PasswordPINReset', 'Registration', 'Renewal', 'TransactionPending', 'TransactionFailure', 'VKYC']

def post_process(category):
    """
    Post-processes the given category to ensure it matches a predefined list of categories.
    
    Strips all whitespace from the input category.
    If the resulting category is not in the predefined list,
    it is replaced with 'Others'.
    
    Args:
        category (str): The input category to be processed.
    
    Returns:
        str: The processed category, either as a valid category from the list
    """
    print(category)
    # Strip all symbols from the category

    category = re.sub(r'\W+', '', category)

    print(category)


    # Check if the category is in the list
    if category not in cat:
        category = 'Others'

    return category

# # Example usage
# input_category = "Transa ctionFa ile ure"
# processed_category = post_process(input_category)
# print(processed_category)

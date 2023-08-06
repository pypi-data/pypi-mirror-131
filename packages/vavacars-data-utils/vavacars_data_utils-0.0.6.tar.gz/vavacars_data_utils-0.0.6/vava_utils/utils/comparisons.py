from difflib import SequenceMatcher

def get_best_match(value, list_values):
    '''
    Returns the best match for a string  between a list of strings based on similarity

    Parameters:
        value (str): Main string to find similar
        list_values (list(str)): List of strings to look for similarity

    Returns:
        best_match (str): String with higher similarity to value
        best_score (float): Score of similarity (1=> identical)
    '''

    score = 0
    best_match = ''

    for v in list_values:
        # C Serisi <-> C (or similar)
        if v.lower() in value.lower():
            return (v, 0.99)

        temp_score = SequenceMatcher(None, str(value).lower(), str(v).lower()).ratio()

        if temp_score > score:
            best_match = v
            score = temp_score

    return (best_match, score)

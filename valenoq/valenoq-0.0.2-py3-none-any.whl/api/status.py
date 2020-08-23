from pdb import set_trace as stop

def get(api_key):
    """
    Get the informations about:
        - Available message quota for the current API key. The quota is 100 messages per week
        - Remaining messages. The allocation of message quota is reset on a weekly basis
        - Initial quota (100 messages)
    
    Parameters
    ------------
    api_key: str
        The API key (available after registration at https://valenoq.com)
    
    Returns JSON
    """
    pass

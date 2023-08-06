
def primitive_datatype_checker(value: str) -> object:
    """A simple function to infer the datatype of an element that is stored with string type.

    Args:
        value (str): It is a string element whose type will be inferred 

    Returns:
        object: It returns the inferred type of the value
    """
    
    try:
        int(value)
        return int
    except:
        pass
    try:
        float(value)
        return float
    except:
        pass

    return str
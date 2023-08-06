from .utils import primitive_datatype_checker
from .model.Matrix import Matrix
from pathlib import Path

def read_csv(file_path : Path, delimiter :str) -> Matrix:
    """It is a function that reads data from a csv file and generates a generic structure that will be used to create other file types.

    Args:
        file_path (Path): It is the path where the file that will be read is.
        delimiter (str):  The character that is used to separete the data
        encoding (str):  The encoding type that is used in the file

    Returns:
        Matrix: A instance of Matrix class
    """

    matrix = Matrix()

    with open(file_path, "r") as stream:
        
        rtn = stream.readline().replace('\n', "")
        matrix.columns = rtn.split(delimiter)

        

        rtn = stream.readline().replace('\n', "")
        while(rtn != ''):
            matrix.rows.append(rtn.split(delimiter))

            rtn = stream.readline().replace('\n', "")
    
    return matrix


def read_json(file_path : Path) -> Matrix: 
    """It is a function that reads data from a json file and generates a generic structure (Matrix) that will be used to create other file types.

    Args:
        file_path (Path): The path where the file that will be read is.
        encoding (str):  The encoding type that will be used to read this file.
    return:
        Matrix: A instance of Matrix class
    """
    
    def read_json_item(str_item: str) -> dict:
        """A function to isolate the process of parsing a simple json item string into a  python dict. 
        When we say simple json item we mean a json object that doesn't contain another object, but only simple types.

        Args:
            str_item (str): The simple json object string. 

        Returns:
            dict: A dict that represents the simple json item string that was received.
        """
        item = dict()
        cleaned_item = str_item.replace("{", "")
        cleaned_item = cleaned_item.split(",")
        
        for attribute in cleaned_item:
            
            attribute = attribute[attribute.find("\""):]
            attribute = attribute.split(":")
            
            if(len(attribute) != 2):
                continue

            
            column_name = attribute[0].replace("\"", "")
            
            value = attribute[1]
            
            if("\"" in value):
                value = value.split("\"")[1]
            else:
                value = primitive_datatype_checker(value)(value)
            
            item[column_name] = value

        return item



    matrix = Matrix()

    with open(file_path, "r") as stream:
        whole_data = stream.read()

        whole_data = whole_data.replace("[", "").replace("]", "")
   
        raw_items = whole_data.split("}")
        items = []

        raw_item = raw_items[0]
        item = read_json_item(raw_item)
        matrix.columns = list(item.keys())

        matrix.rows.append([item[column] for column in matrix.columns])
        
        for raw_item in raw_items[1:]:
            item = read_json_item(raw_item)

            if(item):
                matrix.rows.append([item[column] for column in matrix.columns])
    return matrix


    

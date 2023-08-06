
from pathlib import Path
from .utils import primitive_datatype_checker
from .model.Matrix import Matrix

def write_csv(matrix: Matrix ,path: Path, name: str, delimiter: str, encoding: str) -> None:
    """It is a simple function that uses our generic structure (Matrix) to write the data to a csv file.

    Args:
        matrix (Matrix): It is an instance of our generic data structure that contains the data and will be used on file creation. This structure is defined in `model/Matrix`
        path (Path): It is the path where our csv file will be saved.
        name (str): The name file that will be used.
        delimiter (str): The delimiter that will be used to separete the row elements in the csv format.
        encoding (str): The encoding type that will be used.
    """

    if(not (".csv" in name)):
        _path = path / (name + ".csv")
    else:
        _path = path / name
    
    with open(_path, "w") as stream:

        for i, column in enumerate(matrix.columns):
            stream.write(str(column).encode(encoding))
            
            if(not(i == len(matrix.columns)-1)):
                stream.write(delimiter.encode(encoding))
        stream.write("\n")


        for j, row in enumerate(matrix.rows):
            
            for i, column in enumerate(row):
                
                if(column == None):
                    stream.write("".encode(encoding))
                else:
                    stream.write(str(column).encode(encoding))
                
                if(not(i == len(matrix.columns)-1)):
                   stream.write(delimiter.encode(encoding))

            stream.write("\n".encode(encoding))

def write_json(matrix: Matrix, path: Path, name: str, encoding: str) -> None:
    """It is a simple function that uses our generic structure (Matrix) to write the data to a csv file.

    Args:
        matrix (Matrix): It is an instance of our generic data structure that contains the data and will be used on file creation. This structure is defined in `model/Matrix`
        path (Path): It is the path where our csv file will be saved.
        name (str): The name file that will be used.
        encoding (str): The encoding type that will be used.
    """
    if(not (".json" in name)):
        _path = path / (name + ".json")
    else:
        _path = path / name

    with open(_path, "w") as stream:

        stream.write("[\n")
        
        for j, row in enumerate(matrix.rows):
            
            stream.write("  {\n")
            
            for i, column in enumerate(row):
               
                column_type = primitive_datatype_checker(column)

                stream.write(f"    \"{matrix.columns[i]}\":")

                if(column == None or column == ""):
                    stream.write("null")
                elif(column_type == str):
                    stream.write(f"\"{column}\"")
                else:
                    stream.write(f"{str(column)}")

                if(not(i == len(row) - 1)):
                    stream.write(f",")
                stream.write("\n")
            
            if(not(j == (len(matrix.rows) - 1))):
                stream.write("  },\n")
            else:
                stream.write("  }\n")
        
        stream.write("]")
                


        


class Matrix():
    def __init__(self) -> None:
        self.columns = []
        self.types = {}
        
        self.rows    = []

    def __str__(self):
       
        rtn = "|"
        for column in self.columns:
            rtn += f" {column} |"
        
        

        for row in self.rows:
            rtn += '\n|'
            for item in row:
                rtn += f" {item} |"
            
        
        return rtn
        
class EmptyStringError(Exception):
    def __init__(self):
        self.message = "Empty Strings Error"
        super().__init__(self.message)
    
    def __str__(self):
        return f"Error - {self.message}"
class BusinessException(RuntimeError):
    
    def __init__(self, message:str):
        self.message = message
        super().__init__(message)
    
    def get_message(self) -> str:
        return self.message
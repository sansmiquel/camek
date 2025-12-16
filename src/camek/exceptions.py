class CamekException(Exception):
    """Base exception"""
    pass   

class CamekError(CamekException):
    """Exception for errors"""
    pass

class CamekFileIOError(CamekError):
    """Exception for file I/O errors"""
    pass
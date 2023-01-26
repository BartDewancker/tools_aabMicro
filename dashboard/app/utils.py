from uuid import uuid4

def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())
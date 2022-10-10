import uuid


def create_hash():
    """
    :rtype: str
    """
    return uuid.uuid4().__str__().replace('-', '')[:30]
import uuid
def make_id(prefix="t"):
    return f"{prefix}{uuid.uuid4().hex[:8]}"

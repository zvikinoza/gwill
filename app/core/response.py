from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class Response(Generic[T]):
    def __init__(self, success: bool, obtained: T, msg: Optional[str]):
        self.success = success
        self.obtained = obtained
        self.msg = msg

    def succeeded(self):
        return self.success

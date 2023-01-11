class ArchMonolithicFlaskError(Exception):
    
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(status_code, message)
        self.status_code = status_code
        self.message = message


class ModelObjectNotFoundError(ArchMonolithicFlaskError):
    pass


class OversellError(ArchMonolithicFlaskError):
    pass


class WithoutCheckingRequiredProductsError(ArchMonolithicFlaskError):
    pass
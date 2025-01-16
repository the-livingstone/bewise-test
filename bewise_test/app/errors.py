class RepresentativeError(Exception):
    status_code: int = 422
    title: str | None = None

    def __init__(
        self,
        status_code: int = None,
        title: str = None,
    ) -> None:
        self.status_code = status_code or self.status_code
        self.title = title or self.title

    def dict(self):
        return {"status_code": self.status_code, "title": self.title}

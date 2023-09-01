class StartNaviException(Exception):

    def __init__(self, msg: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.msg = msg

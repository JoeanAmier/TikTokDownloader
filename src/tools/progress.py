class FakeProgress:
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        pass

    async def __aenter__(self):
        return self

    def __enter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_task(
        self,
        *args,
        **kwargs,
    ):
        pass

    def update(
        self,
        *args,
        **kwargs,
    ):
        pass

    def remove_task(
        self,
        *args,
        **kwargs,
    ):
        pass

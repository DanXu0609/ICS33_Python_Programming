from grin import GrinLocation

class GrinRuntimeException(Exception):
    def __init__(self, message: str, location: GrinLocation):
        formatted = f'Error during execution: {str(location)}: {message}'
        super().__init__(formatted)
        self._message = message
        self._location = location


    def location(self) -> GrinLocation:
        return self._location
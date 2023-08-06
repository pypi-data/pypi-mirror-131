
class LayoutReader:
    def __init__(self, path: str):
        self._reader = open(path, encoding="utf-8", mode="r")
        self._cachedLine = ""

    
    def __iter__(self):
        return self

    def __next__(self) -> str:
        self._cachedLine = self._reader.__next__()
        return self._cachedLine


    def nextLine(self) -> str:
        return self.__next__()

    def currentLine(self) -> str:
        return self._cachedLine

    def close(self):
        self._reader.close();    

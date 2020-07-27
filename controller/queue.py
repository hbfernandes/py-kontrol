

class Queue:
    items: list = []

    def __init__(self) -> None:
        pass

    def add(self, item):
        return self.items.append(item)

    def get(self):
        return self.items.pop(0)

    def is_empty(self) -> bool:
        return len(self.items) == 0        


if __name__ == "__main__":
    x = Queue()
    x.add(1)
    x.add(2)
    print(x.get())
    print(x.is_empty())
    print(x.get())
    print(x.is_empty())

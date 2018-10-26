class minecraft:
    def blank(self, *args, **kwargs):
        print(args, kwargs)

    def __getattr__(self, attr):
        print(attr, end=" ")
        return self.blank
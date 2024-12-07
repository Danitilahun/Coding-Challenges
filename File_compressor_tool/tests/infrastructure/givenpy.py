class Context:
    def __getattribute__(self, name: str):
        return object.__getattribute__(self, name)


class GivenScope:
    def __init__(self, steps):
        self.context = Context()
        self.steps = steps or []
        self.started_steps = []

    def __enter__(self):
        for step in self.steps:
            result = step(self.context)
            self.started_steps.append(result)

            if hasattr(result, '__enter__'):
                result.__enter__()

        return self.context

    def __exit__(self, type, value, traceback):
        for step in reversed(self.started_steps):
            if hasattr(step, '__exit__'):
                step.__exit__(type, value, traceback)


class MockWith:
    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

    def __getattribute__(self, item):
        return MockWith()


def given(steps=None):
    return GivenScope(steps)


def then(message=None):
    return MockWith()


def when(description=None):
    return MockWith()


def resulting(param=None):
    return MockWith()

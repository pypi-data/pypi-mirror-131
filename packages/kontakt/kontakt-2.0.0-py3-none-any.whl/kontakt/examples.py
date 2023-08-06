"""Examples of how to use the kontakt extension system.

These serve both as a concrete example of how to use kontakt
as well as for use in the tests.
"""

import kontakt


@kontakt.extension('example-extension')
class ExampleExtension:
    def __init__(self, flavor, size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flavor = flavor
        self.size = size


class ExampleExtensionError(kontakt.ExtensionError):
    pass


class Blue(ExampleExtension):
    pass


class Red(ExampleExtension):
    "Red extension"
    pass


class Green(ExampleExtension):
    @classmethod
    def describe(cls):
        return "description of the Green extension"

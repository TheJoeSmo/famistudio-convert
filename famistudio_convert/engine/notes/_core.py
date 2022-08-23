def literal_property(literal) -> property:
    @property
    def return_literal(*args, **kwargs):
        return literal

    return return_literal

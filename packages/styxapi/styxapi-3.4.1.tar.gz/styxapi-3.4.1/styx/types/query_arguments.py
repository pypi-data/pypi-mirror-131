
def parse_query_argument(type_, value, values, referencetypes={}):
    return type_.visit(Visitor(referencetypes), value, values)


class QueryValidationError(Exception):
    pass


class Visitor:

    def __init__(self, types):
        self.types = types

    def visit_string(self, node, value, values):
        return value

    def visit_integer(self, node, value, values):
        try:
            return int(value)
        except ValueError:
            raise QueryValidationError(f"Invalid value for integer: { value }")

    def visit_float(self, node, value, values):
        try:
            return float(value)
        except ValueError:
            raise QueryValidationError(f"Invalid value for float: { value }")

    def visit_list(self, node, value, values):
        return [node.type.visit(self, item, [item]) for item in values]

    def visit_default(self, typename, node, argument_name, request):
        raise Exception(f"Invalid Type for argument parsing ({ typename })")

    def visit_reference(self, node, value, values):
        reftype = self.types.get(node.name)
        if reftype is None:
            raise Exception(f"Unknown type { node.name }")
        return reftype.visit(self, value, values)

    def visit_const(self, node, value, values):
        if isinstance(node.value, int):
            try:
                value = int(value)
            except ValueError:
                raise QueryValidationError(f"Invalid const { repr(value) }, "
                                            f"expected { repr(node.value )}")
        if node.value != value:
            raise QueryValidationError(f"Invalid const { repr(value) }, "
                                        f"expected { repr(node.value )}")
        return value

    def visit_oneof(self, node, value, values):
        for subtype in node.types:
            try:
                return subtype.visit(self, value, values)
            except QueryValidationError:
                continue
        raise QueryValidationError(f"Invalid value { repr(value) }")

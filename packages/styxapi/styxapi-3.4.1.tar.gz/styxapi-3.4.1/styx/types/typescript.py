import json


def to_ts(type_):
    """ Generates a typescript type from the given type

    >>> to_ts(Array(String()))
    <<< "string[]"
    """
    return type_.visit(Visitor())


class Visitor:

    def visit_unset(self, node):
        return 'undefined'

    def visit_any(self, node):
        return 'any'

    def visit_null(self, node):
        return 'null'

    def visit_string(self, node):
        return 'string'

    def visit_integer(self, node):
        return 'number'

    def visit_float(self, node):
        return 'number'

    def visit_boolean(self, node):
        return 'boolean'

    def visit_object(self, node):
        fields = [
            f'"{ name }"{ "?" if name in node.optional_keys else "" }: '
            f'({ field.visit(self) })'
            for name, field in node.fields.items()]

        return '{' + ', '.join(fields) + '}'

    def visit_list(self, node):
        return f'({ node.type.visit(self) })[]'

    def visit_const(self, node):
        return json.dumps(node.value)

    def visit_reference(self, node):
        return node.name

    def visit_oneof(self, node):
        if node.types:
            return ' | '.join(f'({ t.visit(self) })' for t in node.types)
        else:
            return 'never'

    def visit_default(self, name, node):
        raise Exception(f"cannot handle type { name }")

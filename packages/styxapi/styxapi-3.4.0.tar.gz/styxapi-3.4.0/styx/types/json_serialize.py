
def json_schema(type_):
    """ generates a json schema from the given type

    >>> json_schema(String())
    <<< {'type': 'null'}
    """
    return type_.visit(Visitor())


class Visitor:

    def visit_any(self, node):
        return {
            'type': 'any'
        }

    def visit_null(self, node):
        return {
            "type": "null"
        }

    def visit_string(self, node):
        return {
            "type": "string"
        }

    def visit_integer(self, node):
        return {
            "type": "integer"
        }

    def visit_float(self, node):
        return {
            "type": "number"
        }

    def visit_boolean(self, node):
        return {
            "type": "boolean"
        }

    def visit_object(self, node):
        return {
            "type": "object",
            "properties": {
                name: {
                    "item_type": field.visit(self),
                    "required": name not in node.optional_keys,
                }
                for name, field in node.fields.items()
            }
        }

    def visit_list(self, node):
        return {
            "type": "array",
            "item_type": node.type.visit(self)
        }

    def visit_const(self, node):
        return {
            "type": "const",
            "value": node.value
        }

    def visit_unset(self, node):
        return {"not": {}}

    def visit_reference(self, node):
        return {"$ref": f"#/components/schemas/{ node.name }"}

    def visit_default(self, name, node):
        raise Exception(f"cannot handle type { name }")

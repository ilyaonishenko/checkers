import ast


class Transformer(ast.NodeTransformer):
    ALLOWED_NAMES = {'Decimal', 'None', 'False', 'True', 'null'}
    ALLOWED_NODE_TYPES = {'Expression', 'Tuple', 'Call', 'Name', 'Load', 'Str', 'Num', 'List', 'Dict'}

    def visit_Name(self, node):
        if not node.id in self.ALLOWED_NAMES:
            raise RuntimeError("Name access to %s is not allowed" % node.id)

        # traverse to child nodes
        return self.generic_visit(node)

    def generic_visit(self, node):
        nodetype = type(node).__name__
        if nodetype not in self.ALLOWED_NODE_TYPES:
            raise RuntimeError("Invalid expression: %s not allowed" % nodetype)

        return ast.NodeTransformer.generic_visit(self, node)

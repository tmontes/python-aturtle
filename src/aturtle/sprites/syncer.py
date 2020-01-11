# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import ast
import inspect
import textwrap
import time
import types



class _AsyncDefTransformer(ast.NodeTransformer):

    def __init__(self, name_transformer):
        self._name_transformer = name_transformer

    def visit_AsyncFunctionDef(self, node):
        self.generic_visit(node)
        return ast.FunctionDef(
            name=self._name_transformer(node.name),
            args=node.args,
            body=node.body,
            decorator_list=node.decorator_list,
            returns=node.returns,
            type_comment=node.type_comment,
        )

    def visit_Await(self, node):
        await_expr = node.value
        return _ExprTransformer(self._name_transformer).visit(await_expr)



class _ExprTransformer(ast.NodeTransformer):

    def __init__(self, name_transformer):
        self._name_transformer = name_transformer

    def visit_Attribute(self, node):
        if node.value.id == 'asyncio' and node.attr == 'sleep':
            return ast.Attribute(
                value=ast.Name(id='time', ctx=node.value.ctx),
                attr='sleep',
                ctx=node.ctx,
            )
        elif node.value.id == 'self':
            return ast.Attribute(
                value=ast.Name(id=node.value.id, ctx=node.value.ctx),
                attr=self._name_transformer(node.attr),
                ctx=node.ctx,
            )



def create_sync_method(async_method, name_transformer):

    if not inspect.iscoroutinefunction(async_method):
        raise TypeError(f'{async_method} must be a coroutine function')

    async_src = textwrap.dedent(inspect.getsource(async_method))
    async_mod_ast = ast.parse(async_src)

    sync_mod_ast = _AsyncDefTransformer(name_transformer).visit(async_mod_ast)
    ast.fix_missing_locations(sync_mod_ast)

    sync_mod_code = compile(sync_mod_ast, '<generated>', 'exec')
    is_code_object = lambda o: isinstance(o, types.CodeType)
    sync_code = next(filter(is_code_object, sync_mod_code.co_consts))
    sync_method_globals = dict(async_method.__globals__)
    sync_method_globals['time'] = time
    sync_name = name_transformer(async_method.__name__)

    sync_method = types.FunctionType(sync_code, sync_method_globals, sync_name)
    sync_method.__kwdefaults__ = async_method.__kwdefaults__

    return sync_method

# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

"""
Syncer module.

Exposes a single function that creates synchronous function objects from
coroutine functions.
"""

# READ THIS
# ---------
# This module was created specifically with the base.Sprite class' async_*
# methods in mind. It's purpose is to allow for their source code to support
# both coroutine based asynchronous animation, and function based synchronous
# animation: the former are the `async def` methods with names starting with
# `async_`, the latter will be created automatically by this module's code.
#
# Having tried a few design approaches, I settled with what seemed like the
# most explicit one: a single function is called with coroutine that leads to
# the creation of its "equivalent" function. Various combinations of this
# design would work: a base class with __init_subclass__, a meta class, a
# decorator, and probably more. The "just a function" approach seemed simpler,
# easier to diagnose, and, again, more explicit.
#
# IMPORTANT
# ---------
# Not being generic, this module may need updates if ever the coroutine function
# objects it needs to handle use other kinds of async code. In particular, it
# has been updated in order to support chained attribute access expressions used
# in the Turtle class' async methds.

import ast
import inspect
import textwrap
import time
import types



def create_sync_func(async_func, name_transformer):
    """
    Returns a function object created from the `async_func` coroutine function
    object. The `name_transformer` callable takes a string and returns another
    string. It is used to map asynchronous names to synchronous ones, as in:

    - Determining the resulting function's name from `async_func`'s name.
    - Replacing names in awaited "self.<name>" expressions.

    The resulting function will have the same signature and equivalent code:

    - All awaited expressions are converted to non-awaited ones.
    - All awaited references to `asyncio.sleep` are replaced with `time.sleep`.
    - All awaited expressions with "self." attribute access have their names
      transformed.

    EXAMPLE
    -------
    Take this class:

    >   import asyncio
    >
    >   class Sleeper:
    >
    >       async def do(self, duration):
    >           await asyncio.sleep(duration)
    >
    >       async def repeat(self, duration, times):
    >           for _ in times:
    >               await self.do(duration)

    Setting the following class attributes, using a name transformer that adds
    a `_sync` suffix:

    >       do_sync = create_sync_func(do, lambda n: n+'_sync')
    >       repeat_sync = create_sync_func(repeat, lambda n: n+'_sync')

    Is equivalent to adding these methods to the class:

    >       def do_sync(self, duration):
    >           time.sleep(duration)
    >
    >       def repeat_sync(self, duration, times):
    >           for _ in times:
    >               self.do_sync(duration)

    NOTE: The do_sync and repeat_sync assignments **must** be consistent with
          the `name_transformer` in use, otherwise cross method references fail
          at runtime.

    IMPORTANT
    ---------
    Created explicitly to handle base.Sprite's and Turtle's use cases.
    """

    if not inspect.iscoroutinefunction(async_func):
        raise TypeError(f'{async_func} must be a coroutine function')

    # Get the coroutine function's AST.
    async_src = textwrap.dedent(inspect.getsource(async_func))
    async_mod_ast = ast.parse(async_src)

    # Create a new, transformed, synchronous "equivalent" AST.
    sync_mod_ast = _AsyncDefTransformer(name_transformer).visit(async_mod_ast)
    ast.fix_missing_locations(sync_mod_ast)

    # The sync code object is the only code constant in the compiled module.
    sync_mod_code = compile(sync_mod_ast, '<generated>', 'exec')
    is_code_object = lambda o: isinstance(o, types.CodeType)
    sync_code = next(filter(is_code_object, sync_mod_code.co_consts))

    # The sync code has references to the `time` module: ensure it's reachable.
    sync_func_globals = async_func.__globals__
    sync_func_globals['time'] = time

    # Create the sync function's name from the async one.
    sync_name = name_transformer(async_func.__name__)

    # Finally, create the sync function from sync code and globals.
    sync_func = types.FunctionType(sync_code, sync_func_globals, sync_name)
    # Is there a better way of "copying" default kwarg values?
    if async_func.__kwdefaults__:
        sync_func.__kwdefaults__ = dict(async_func.__kwdefaults__)

    return sync_func



class _AsyncDefTransformer(ast.NodeTransformer):

    def __init__(self, name_transformer):
        self._name_transformer = name_transformer

    def visit_AsyncFunctionDef(self, node):
        """
        Replaces "async def async_name" constructs with "def sync_name" ones.
        Uses `name_transformer` to produce "sync_name" from "async_name".
        """
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
        """
        Replaces "await expr" constructs with "sync_expr", transformed from
        "expr" via delegation to another AST transformer.
        """
        await_expr = node.value
        return _ExprTransformer(self._name_transformer).visit(await_expr)



class _ExprTransformer(ast.NodeTransformer):

    def __init__(self, name_transformer):
        self._name_transformer = name_transformer

    def visit_Attribute(self, node):
        """
        Replaces "asyncio.sleep" constructs with "time.sleep" ones,
        "self.async_name" constructs with "self.sync_name" ones, and
        "self.<ASAC>.async_name" constructs with "self.<ASAC>.sync_name"
        ones, where "<ASAC>" is a chain of "attribute.sub_attribute",
        using `name_transformer` to produce "sync_name" from "async_name".
        """
        if isinstance(node.value, ast.Name):
            if node.value.id == 'asyncio' and node.attr == 'sleep':
                # Transform "asyncio.sleep" into "time.sleep"
                return ast.Attribute(
                    value=ast.Name(id='time', ctx=node.value.ctx),
                    attr='sleep',
                    ctx=node.ctx,
                )
            if node.value.id == 'self':
                # Transform "self.async_name" into "self.sync_name".
                return ast.Attribute(
                    value=node.value,
                    attr=self._name_transformer(node.attr),
                    ctx=node.ctx,
                )
        if isinstance(node.value, ast.Attribute) and self._starts_at_self(node.value):
            # Recurse into sub-attributes if first name is "self".
            return ast.Attribute(
                value=self.visit_Attribute(node.value),
                attr=self._name_transformer(node.attr),
                ctx=node.ctx,
            )
        # Leave unchanged.
        return node

    def _starts_at_self(self, node):
        # True if the attribute/sub-attribute chain in node starts with "self".
        if isinstance(node.value, ast.Name):
            return node.value.id == 'self'
        if isinstance(node.value, ast.Attribute):
            return self._starts_at_self(node.value)
        return False

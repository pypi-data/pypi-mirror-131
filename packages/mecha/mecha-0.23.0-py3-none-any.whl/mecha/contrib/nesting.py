"""Plugin for handling nested commands."""


__all__ = [
    "NestedCommandsTransformer",
    "parse_nested_root",
]


from dataclasses import dataclass, replace
from typing import List, cast

from beet import Context, Function
from beet.core.utils import required_field
from tokenstream import TokenStream, set_location

from mecha import (
    AstChildren,
    AstCommand,
    AstNode,
    AstResourceLocation,
    AstRoot,
    CompilationDatabase,
    Diagnostic,
    Mecha,
    MutatingReducer,
    consume_line_continuation,
    delegate,
    rule,
)

COMMAND_TREE = {
    "type": "root",
    "children": {
        "execute": {
            "type": "literal",
            "children": {
                "expand": {
                    "type": "literal",
                    "children": {
                        "commands": {
                            "type": "argument",
                            "parser": "mecha:nested_root",
                            "executable": True,
                        }
                    },
                },
                "commands": {
                    "type": "argument",
                    "parser": "mecha:nested_root",
                    "executable": True,
                },
            },
        },
        "schedule": {
            "type": "literal",
            "children": {
                "function": {
                    "type": "literal",
                    "children": {
                        "function": {
                            "type": "argument",
                            "parser": "minecraft:function",
                            "children": {
                                "time": {
                                    "type": "argument",
                                    "parser": "minecraft:time",
                                    "children": {
                                        "append": {
                                            "type": "literal",
                                            "children": {
                                                "commands": {
                                                    "type": "argument",
                                                    "parser": "mecha:nested_root",
                                                    "executable": True,
                                                },
                                            },
                                        },
                                        "replace": {
                                            "type": "literal",
                                            "children": {
                                                "commands": {
                                                    "type": "argument",
                                                    "parser": "mecha:nested_root",
                                                    "executable": True,
                                                },
                                            },
                                        },
                                        "commands": {
                                            "type": "argument",
                                            "parser": "mecha:nested_root",
                                            "executable": True,
                                        },
                                    },
                                }
                            },
                        }
                    },
                },
            },
        },
        "function": {
            "type": "literal",
            "children": {
                "name": {
                    "type": "argument",
                    "parser": "minecraft:function",
                    "executable": True,
                    "children": {
                        "commands": {
                            "type": "argument",
                            "parser": "mecha:nested_root",
                            "executable": True,
                        }
                    },
                }
            },
        },
    },
}


def beet_default(ctx: Context):
    mc = ctx.inject(Mecha)

    mc.spec.multiline = True
    mc.spec.add_commands(COMMAND_TREE)

    mc.spec.parsers["nested_root"] = parse_nested_root
    mc.spec.parsers["command:argument:mecha:nested_root"] = delegate("nested_root")

    mc.transform.extend(NestedCommandsTransformer(ctx=ctx, database=mc.database))


def parse_nested_root(stream: TokenStream) -> AstRoot:
    """Parse nested root."""
    with stream.syntax(colon=r":"), stream.intercept("newline", "indent"):
        stream.expect("colon")
        stream.expect("newline")
        stream.expect("indent")

    level, command_level = stream.indentation[-2:]

    commands: List[AstCommand] = []

    with stream.intercept("newline"), stream.provide(
        scope=(),
        line_indentation=command_level,
    ):
        while True:
            commands.append(delegate("command", stream))

            # The command parser consumes the trailing newline so we need to rewind
            # to be able to use "consume_line_continuation()".
            while (token := stream.peek()) and not token.match("newline", "eof"):
                stream.index -= 1

            with stream.provide(multiline=True, line_indentation=level):
                if not consume_line_continuation(stream):
                    break

    node = AstRoot(commands=AstChildren(commands))
    return set_location(node, commands[0], commands[-1])


@dataclass
class NestedCommandsTransformer(MutatingReducer):
    """Transformer that handles nested commands."""

    ctx: Context = required_field()
    database: CompilationDatabase = required_field()

    def emit_function(self, path: str, root: AstRoot):
        """Helper method for emitting nested commands into a separate function."""
        function = Function()
        self.ctx.data[path] = function
        self.database[function] = replace(
            self.database[self.database.current],
            ast=root,
            resource_location=path,
        )
        self.database.enqueue(function, self.database.step + 1)

    @rule(AstCommand, identifier="execute:run:subcommand")
    def execute_function(self, node: AstCommand):
        if (
            isinstance(command := node.arguments[0], AstCommand)
            and command.identifier == "function:name:commands"
        ):
            name, root = command.arguments

            if isinstance(name, AstResourceLocation) and isinstance(root, AstRoot):
                path = name.get_canonical_value()

                if path in self.ctx.data.functions:
                    d = Diagnostic("error", f"Function {path!r} already exists.")
                    raise set_location(d, name)

                self.emit_function(path, root)

            command = replace(
                command,
                identifier="function:name",
                arguments=AstChildren([name]),
            )
            return replace(node, arguments=AstChildren([command]))

        return node

    @rule(AstCommand, identifier="execute:commands")
    def execute_commands(self, node: AstCommand):
        generate = self.ctx.generate["nested_execute"]
        root = cast(AstRoot, node.arguments[0])

        if len(root.commands) == 1:
            subcommand = root.commands[0]

            if subcommand.identifier == "execute:subcommand":
                return subcommand.arguments[0]

        else:
            if path := self.database[self.database.current].resource_location:
                path = generate.format(path + "/nested_execute_{incr}")
            else:
                path = generate.path()

            self.emit_function(path, root)

            resource_location = AstResourceLocation.from_value(path)

            subcommand = AstCommand(
                identifier="function:name",
                arguments=AstChildren([cast(AstNode, resource_location)]),
            )

        return AstCommand(
            identifier="execute:run:subcommand",
            arguments=AstChildren([cast(AstNode, subcommand)]),
        )

    @rule(AstCommand, identifier="schedule:function:function:time:commands")
    @rule(AstCommand, identifier="schedule:function:function:time:append:commands")
    @rule(AstCommand, identifier="schedule:function:function:time:replace:commands")
    def schedule_function(self, node: AstCommand):
        name = node.arguments[0]
        root = node.arguments[-1]

        if isinstance(name, AstResourceLocation) and isinstance(root, AstRoot):
            path = name.get_canonical_value()

            if path in self.ctx.data.functions:
                d = Diagnostic("error", f"Function {path!r} already exists.")
                raise set_location(d, name)

            self.emit_function(path, root)

            return replace(
                node,
                identifier=node.identifier[:-9],
                arguments=AstChildren(node.arguments[:-1]),
            )

        return node

    @rule(AstRoot)
    def root(self, node: AstRoot):
        changed = False
        commands: List[AstCommand] = []

        for command in node.commands:
            if command.identifier == "function:name:commands":
                name, root = command.arguments

                if isinstance(name, AstResourceLocation) and isinstance(root, AstRoot):
                    path = name.get_canonical_value()

                    if path in self.ctx.data.functions:
                        d = Diagnostic("error", f"Function {path!r} already exists.")
                        raise set_location(d, name)

                    self.emit_function(path, root)
                    changed = True
                    continue

            args = command.arguments
            stack: List[AstCommand] = [command]

            expand = None

            while args and isinstance(subcommand := args[-1], AstCommand):
                if subcommand.identifier == "execute:expand:commands":
                    expand = subcommand
                    break
                stack.append(subcommand)
                args = subcommand.arguments

            if expand:
                changed = True
                for nested_command in cast(AstRoot, expand.arguments[0]).commands:
                    if nested_command.identifier == "execute:subcommand":
                        expansion = cast(AstCommand, nested_command.arguments[0])
                    else:
                        expansion = AstCommand(
                            identifier="execute:run:subcommand",
                            arguments=AstChildren([cast(AstNode, nested_command)]),
                        )
                        expansion = set_location(expansion, nested_command)

                    for prefix in reversed(stack):
                        args = AstChildren([*prefix.arguments[:-1], expansion])
                        expansion = replace(prefix, arguments=args)

                    commands.append(expansion)

            else:
                commands.append(command)

        if changed:
            return replace(node, commands=AstChildren(commands))

        return node

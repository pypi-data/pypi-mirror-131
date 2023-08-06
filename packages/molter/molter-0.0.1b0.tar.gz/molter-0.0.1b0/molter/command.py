import functools
import inspect
import typing
from types import NoneType

import attr
import dis_snek

from . import converters
from . import errors


@attr.s(slots=True)
class CommandParameter:
    name: str = attr.ib(default=None)
    default: typing.Optional[typing.Any] = attr.ib(default=None)
    converters: list[
        typing.Callable[[dis_snek.MessageContext, str], typing.Any]
    ] = attr.ib(factory=list)
    variable: bool = attr.ib(default=False)
    consume_rest: bool = attr.ib(default=False)


def _convert_to_bool(argument: str) -> bool:
    lowered = argument.lower()
    if lowered in ("yes", "y", "true", "t", "1", "enable", "on"):
        return True
    elif lowered in ("no", "n", "false", "f", "0", "disable", "off"):
        return False
    else:
        raise errors.BadArgument(f"{argument} is not a recognised boolean option.")


def _get_converter(
    anno: type,
) -> typing.Callable[[dis_snek.MessageContext, str], typing.Any]:  # type: ignore
    if converter := converters.SNEK_OBJECT_TO_CONVERTER.get(anno, None):
        return converter().convert  # type: ignore
    elif inspect.isclass(anno) and issubclass(anno, converters.Converter):
        return anno().convert  # type: ignore
    elif inspect.isfunction(anno):
        num_params = len(inspect.signature(anno).parameters.values())
        match num_params:
            case 2:
                return lambda ctx, arg: anno(ctx, arg)
            case 1:
                return lambda ctx, arg: anno(arg)
            case _:
                errors.BadArgument(anno)
    elif anno == bool:
        return lambda ctx, arg: _convert_to_bool(arg)
    elif anno == inspect._empty:
        return lambda ctx, arg: str(arg)
    else:
        return lambda ctx, arg: anno(arg)


def _get_params(func: typing.Callable):
    cmd_params: list[CommandParameter] = []

    callback = functools.partial(func, dis_snek.MessageContext())

    params = inspect.signature(callback).parameters
    for name, param in params.items():
        cmd_param = CommandParameter()
        cmd_param.name = name
        cmd_param.default = (
            param.default
            if param.default is not param.empty
            else dis_snek.const.MISSING
        )

        anno = param.annotation

        if typing.get_origin(anno) == typing.Union:
            for arg in typing.get_args(anno):
                if arg != NoneType:
                    converter = _get_converter(arg)
                    cmd_param.converters.append(converter)
                elif cmd_param.default == dis_snek.const.MISSING:  # d.py-like behavior
                    cmd_param.default = None
        else:
            converter = _get_converter(anno)
            cmd_param.converters.append(converter)

        match param.kind:
            case param.KEYWORD_ONLY:
                cmd_param.consume_rest = True
            case param.VAR_POSITIONAL:
                cmd_param.variable = True

        cmd_params.append(cmd_param)

    return cmd_params


async def maybe_coroutine(func: typing.Callable, *args, **kwargs):
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        return func(*args, **kwargs)


@attr.s(
    slots=True, kw_only=True, on_setattr=[attr.setters.convert, attr.setters.validate]
)
class MolterCommand(dis_snek.MessageCommand):
    params: list[CommandParameter] = attr.ib(
        metadata=dis_snek.utils.docs("The paramters of the command."), default=None
    )

    async def call_callback(
        self, callback: typing.Callable, ctx: dis_snek.MessageContext
    ):
        if not self.params:
            # if we did this earlier, we would have to deal with self
            # and im too lazy to deal with self
            self.params = _get_params(self.callback)

        # sourcery skip: remove-empty-nested-block, remove-redundant-if, remove-unnecessary-else
        if len(self.params) == 0:
            return await callback(ctx)
        else:
            new_args: list[typing.Any] = []
            args: list[str] = ctx.args
            param_index = 0

            break_for_loop = False

            for index, arg in enumerate(args):
                while param_index < len(self.params):
                    param = self.params[param_index]

                    if param.consume_rest:
                        arg = " ".join(args[index:])
                        break_for_loop = True
                    if param.variable:
                        # temp behavior until i decide what to do with this
                        new_args.append(args[index:])
                        break_for_loop = True
                        break

                    converted = dis_snek.const.MISSING
                    for converter in param.converters:
                        try:
                            converted = await maybe_coroutine(converter, ctx, arg)
                            break
                        except Exception as e:
                            if param.default == dis_snek.const.MISSING:
                                raise errors.BadArgument(str(e))

                    if converted == dis_snek.const.MISSING:
                        if param.default != dis_snek.const.MISSING:
                            converted = param.default
                            new_args.append(converted)
                            param_index += 1
                        else:
                            # vague, ik
                            raise errors.BadArgument(
                                f"Could not convert {arg} into a type specified for"
                                f" {param.name}."
                            )
                    else:
                        new_args.append(converted)
                        param_index += 1
                        break

                if break_for_loop:
                    break

            if len(new_args) < len(self.params):
                raise errors.BadArgument(
                    f"Missing argument for {self.params[len(new_args)].name}"
                )

            return await callback(ctx, *new_args)


def message_command(
    name: str = None,
):
    """
    A decorator to declare a coroutine as a message command.
    parameters:
        name: The name of the command, defaults to the name of the coroutine
    returns:
        Message Command Object
    """

    def wrapper(func):
        if not inspect.iscoroutinefunction(func):
            raise ValueError("Commands must be coroutines.")
        return MolterCommand(name=name or func.__name__, callback=func)

    return wrapper


msg_command = message_command

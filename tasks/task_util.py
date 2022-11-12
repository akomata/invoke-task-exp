import functools

from rich import print


def pre_task(f):
    @functools.wraps(f)
    def wrapper(c, *args, **kwargs):
        if not hasattr(c, "indent"):
            c.indent = 0
        f(c, *args, **kwargs)

    return wrapper


def multi_print(
    *args, indent=0, ind="  ", invoke=False, header=False, bold=False, magenta=False, white=False, **kwargs
):
    """
    Multi purpose print with indent, and some cosmetics
      Args:
        indent: indent multiplier
        ind: indent string
        invoke: print with [Invoke] prefix
        header: print as heading line
        bold: print in bold style
        magenta: print in color magenta
        white: print in color white
    """
    header_prefix = "[b magenta]"
    header_suffix = "[/b magenta]"
    invoke_prefix = "[magenta][Invoke][/magenta] "
    bold_prefix = "[b]"
    bold_suffix = "[/b]"
    white_prefix = "[white]"
    white_suffix = "[/white]"

    if indent != 0 or invoke or header or bold or magenta or white:
        lst = list(args)
        if indent:
            # Add indent to the 1st arg
            lst[0] = ind * indent + str(lst[0])
        if invoke:
            lst[0] = invoke_prefix + str(lst[0])
        if header:
            for index, obj in enumerate(lst):
                # Surround each single object with prefix and suffix because rich print needs it
                lst[index] = f"{header_prefix}{str(obj)}{header_suffix}"
        if bold:
            for index, obj in enumerate(lst):
                # Surround each single object with prefix and suffix because rich print needs it
                lst[index] = f"{bold_prefix}{str(obj)}{bold_suffix}"
        if white:
            for index, obj in enumerate(lst):
                # Surround each single object with prefix and suffix because rich print needs it
                lst[index] = f"{white_prefix}{str(obj)}{white_suffix}"
        args = tuple(lst)
    print(*args, **kwargs)


multi_print.invoke = functools.partial(multi_print, invoke=True)
multi_print.header = functools.partial(multi_print, header=True)
multi_print.bold = functools.partial(multi_print, bold=True)
multi_print.magenta = functools.partial(multi_print, magenta=True)
multi_print.white = functools.partial(multi_print, white=True)

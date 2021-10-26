# iWut

Friendlier tracebacks, collapsing frames with library code, inline variable values, and adding context.

![wut-vars-ctx-prettier](https://user-images.githubusercontent.com/2068077/138010088-d17eef95-0965-49b0-9570-b21c832cbe99.gif)


## Installation

```
pip install iwut
```

## Notebook

```
%load_ext iwut
```

**Global Usage:** You can turn on wut globally to catch and re-render all tracebacks.

```
%wut on
```

You can likewise turn off wut with `%wut off`.

**Case-by-case Usage:** Once you hit an error, you can use wut to retroactively re-parse the exception. For example, you may have the following

```
> 1/0
---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)
/tmp/ipykernel_165/2354412189.py in <module>
----> 1 1/0

ZeroDivisionError: division by zero
```

In the next cell, simply use the line magic

```
%wut
```

This will pretty print a friendlier traceback. You can alternatively, prepend the cell magic on a faulty cell, like this:

```
%%wut
1 / 0
```

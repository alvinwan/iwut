# Wut

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

Once you hit an error. For example, you may have the following

```
1/0
```

In the next cell, simply use the line magic

```
%wut
```

This will pretty print a friendlier traceback. You can alternatively, use the cell magic on a faulty cell, like this:

```
%%wut
1 / 0
```

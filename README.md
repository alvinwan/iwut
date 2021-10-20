# Wut

Friendlier tracebacks, collapsing frames with library code, inline variable values, and adding context.

## Installation

```
pip install wut
```

## Notebook

```
%load_ext wut
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

Here is a GIF demo of wut's various features:

![https://i.imgur.com/GFUXqxk.gif](https://i.imgur.com/GFUXqxk.gif)
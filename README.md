# iWut

Friendlier tracebacks, with (1) collapsible traceback frames for library code and (2) inlined variable values.

1. **Collapsed traceback frames for library code**, to hide traceback information for library internals.

   The following is an example traceback from a faulty PyTorch dataloader.

   <img width="600" alt="Screen Shot 2021-10-26 at 4 13 20 PM" src="https://user-images.githubusercontent.com/2068077/138974041-b574c444-5952-461b-9b59-4672e85c3a05.png">
  
   Compare the above output to the below, collapsible traceback from wut:

   <img width="600" alt="collapsible-traceback" src="https://user-images.githubusercontent.com/2068077/138974069-fbb52695-f1aa-4690-8bf7-b6cac230507d.gif">

2. **Inline Variable Values** to make debugging faster.

   <img width="600" alt="inline-variable-values" src="https://user-images.githubusercontent.com/2068077/138973444-0d9efce3-48de-4ed2-b187-cc7a4b410bd6.gif">

## Usage

To install,

```
pip install iwut
```

Or, from within a notebook cell, run `%pip install iwut`. Then, load the `iwut` extension.

```
%load_ext iwut
```

**Global Usage:** You can turn on wut globally to catch and re-render all tracebacks.

```
%wut on
```

**Post-Error Usage** (Line Magic): If you don't turn wut on globally, you can use wut to retroactively re-parse the exception. For example, say you've got a `ZeroDivisionError`.

<img width="1008" alt="Screen Shot 2021-10-26 at 4 01 38 PM" src="https://user-images.githubusercontent.com/2068077/138973079-b0676104-f556-4c2a-8574-678ddc2ee3b6.png">

In the next cell, use the `%wut` line magic to print a friendlier traceback.

```
%wut
```

<img width="995" alt="Screen Shot 2021-10-26 at 3 59 06 PM" src="https://user-images.githubusercontent.com/2068077/138973875-c720105a-6115-408e-bc00-d23fabbfe796.png">

**Pre-Error Usage** (Cell Magic): If you don't turn on wut globally, you can also rerun a cell with the cell magic `%%wut` prepended to get friendlier tracebacks.

```
%%wut
1/0
```

## Demo

See `demo.ipynb` in the root directory of this repository for a demo, or see the GIF below:

![wut-vars-ctx-prettier](https://user-images.githubusercontent.com/2068077/138010088-d17eef95-0965-49b0-9570-b21c832cbe99.gif)

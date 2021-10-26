from IPython.core.magic import (
    Magics, magics_class, line_magic, cell_magic,
    line_cell_magic
)
from IPython.core.display import HTML, display
from IPython import get_ipython
from traceback import FrameSummary, linecache
from html import escape
import sys


CSS = """
<style>
.output_subarea { /* HACK to make tooltips at edge show */
    overflow-x: visible
}
.ellipsis {
    background-color:#eee;
    color:#666;
    border-radius:2px;
    cursor:pointer;
    padding: 0 5px;
}
.ellipsis:hover {
    background-color:#e3e3e3;
    color:#000;
}
.output_area pre.code {
    padding:0 10px;
    overflow:visible;
    color:#999;
    background-color:#f6f6f6;
}
pre.meta + pre.code {
    margin-top:5px;
}
pre.code + pre.meta, pre.code + details {
    margin-top:5px;
}
.variable {
    position:relative;
    cursor:pointer;
    border-bottom:1px solid #666;
}
.variable:before {
  content: attr(data-tooltip); /* here's the magic */
  position:absolute;
  
  /* horizontally center */
  left:50%;
  transform: translateX(-50%);
  
  /* move to top */
  bottom: 100%;
  margin-bottom: 5px; /* and add a small bottom margin */
  
  /* basic styles */
  padding: 7px 10px;
  border-radius:2px;
  background:#000;
  color: #fff;
  text-align:center;
  
  width: max-content; 
  max-width: 200px;

  display:none; /* hide by default */
}
.variable:hover:before {
  display:block;
}
.variable:after {
  content: "";
  position:absolute;
  
  /* position tooltip correctly */
  transform: translateX(-50%);
  left:50%;
 
  /* move to bottom */
  bottom:100%;
  margin-bottom:-10px;
 
  /* the arrow */
  border:10px solid #000;
  border-color: black transparent transparent transparent;
  
  display:none;
}
.variable:hover {
    color:#208FFB;
    border-bottom:1px solid #208FFB;
}
.variable:hover:before, .variable:hover:after {
  display:block;
}
.output_area .code.highlight {
    color:#000;
}
.output_area pre.meta {
    padding:5px;
    border-radius:2px;
    margin:5px 0;
}
.lineno {
    border-right:1px solid #999;
    padding-right:5px;
    color:#999;
}
.highlight .lineno {
    color:#000;
    border-right:1px solid #000;
}
.error-container {
    padding-left:1em;
    border-left:3px solid #eee;
}
</style>
"""


class ExtendedFrameSummary(FrameSummary):
    
    def __init__(self, *args, code=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code.splitlines() if code else []
    
    @property
    def lines(self):
        results = []
        for lineno in range(self.lineno - 2, self.lineno + 3):
            cached = linecache.getline(self.filename, lineno)
            if self.code and lineno > 0 and lineno <= len(self.code):
                results.append((lineno, self.code[lineno - 1]))
            elif cached:
                results.append((lineno, cached))
        return results


def to_summary(tb, name_to_meta=None):
    frame = tb.tb_frame
    code = frame.f_code
    
    name_to_meta = name_to_meta or {}
    meta = name_to_meta.get(code.co_filename, {})
    return ExtendedFrameSummary(
        filename=meta.get('name', code.co_filename),
        lineno=frame.f_lineno,
        name=code.co_name,
        lookup_line=True,
        locals=frame.f_locals,
        code=meta.get('code'),
    )


def extract_tb(tb, name_to_meta=None):
    frames = [to_summary(tb, name_to_meta)]
    while tb.tb_next:
        tb = tb.tb_next
        frames.append(to_summary(tb, name_to_meta))
    return frames


def annotate_variables(line, variables):
    if variables is None:
        return line
    cur = [(True, line)]
    for name, value in variables.items():
        tokens = []
        for raw, token in cur:
            if not raw:
                tokens.append((raw, token))
                continue
            parts = token.split(name)
            for i, part in enumerate(parts):
                tokens.append((True, part))
                if i != len(parts) - 1:
                    tokens.append((False, f"""<span class="variable" data-tooltip="{escape(value)}">{name}</span>"""))
        cur = tokens
    return "".join([token[1] for token in tokens])


def filename_to_cell(filename):
    if "/tmp/ipykernel" in filename:
        return f"Cell #{filename.split('/')[-1].split('.')[0]}"
    return filename


def get_wut_traceback(etype, value, tb, tb_offset=0, name_to_meta=None):
    lines = ["<div class='error-container'>"]
    toggle = False
    frames = extract_tb(tb, name_to_meta)[tb_offset:]
    for frame_idx, frame in enumerate(frames):
        should_hide_frame = 'site-packages' in frame.filename and not (frame_idx == len(frames) - 1)
        if should_hide_frame and not toggle:
            lines.append('<details><summary><span class="ellipsis">&middot;&middot;&middot;</span></summary>')
            toggle = True
        elif not should_hide_frame and toggle:
            lines.append('</details>')
            toggle = False
        filename = filename_to_cell(frame.filename)
        lines.append(
            f"<pre class='meta'><span style='color:#00A250'>{escape(filename)}</span></pre>" if frame.name == '<module>' else
            f"<pre class='meta'><b><span style='color:#60C6C8'>{escape(frame.name)}</span></b> in <span style='color:#00A250'>{escape(filename)}</span></pre>"
        )
        for lineno, code in frame.lines:
            cls, space = "code", "  "
            if lineno == frame.lineno:
                cls, space = "code highlight", "&rightarrow; "
            lines.append(f"<pre class='{cls}'>{space}<span class='lineno'>{lineno}</span>  {annotate_variables(code, frame.locals)}</pre>")
    lines.append(f"<br/><pre><span style='color:#E75C58'>{etype.__name__}</span>: {value}</pre>")
    lines.append("</div>")
    return HTML(CSS + '\n'.join(lines))


def handle_wut_traceback(self, etype, value, tb, tb_offset):
    return display(get_wut_traceback(etype, value, tb, tb_offset))


def handle_wut_command(command):
    if command == 'on':
        get_ipython().set_custom_exc((Exception,), handle_wut_traceback)
        return True
    elif command == 'off':
        get_ipython().set_custom_exc((), None)
        return True
    
    
def load_ipython_extension(ipython):
    ipython.register_magics(iWutMagics)


@magics_class
class iWutMagics(Magics):

    @line_magic('wut')
    def line_magic(self, line):
        if handle_wut_command(line):
            return 
        if not hasattr(sys, 'last_type'):
            print('No last error to analyze!')
            return
        display(get_wut_traceback(sys.last_type, sys.last_value, sys.last_traceback, tb_offset=1))

    @cell_magic('wut')
    def cell_magic(self, line, cell):
        try:
            self.shell.ex(cell)
        except Exception as e:
            display(get_wut_traceback(type(e), e, e.__traceback__, name_to_meta={
                '<string>': {'code': cell, 'name': '(current cell)'}
            }, tb_offset=1))
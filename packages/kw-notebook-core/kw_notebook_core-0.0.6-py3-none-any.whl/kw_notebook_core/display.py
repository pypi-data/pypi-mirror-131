from IPython.core.display import display, HTML, Markdown

def md(*paragraphs):
  for p in paragraphs:
    display(Markdown(p + '\n\n'))

def notebook_caution():
  md('''## 超重要：落とし穴に注意'

  ほかのひとから共有されたノートブックの所有権は共有してくれた人にあります。そういうノートブックも一時的に修正できそうに見えるので、あたかも所有権が自分にあるかのように錯覚します。でも、所有権がほかの人にあるノートブックは保存することができません。

  せっかく編集して、自分好みの内容になっても保存できなければ困ります。そこで、ノートブックを共有されたら、なにはともかくそれを**自分のノートブックとして保存**しましょう。

  いったん自分のノートブックとして保存してしまえば、それを自分の好きに編集し、保存できるようになります。
  ''')

notebook_caution()

from bokeh.plotting import output_notebook, show, figure
from bokeh.models import *
from bokeh.layouts import *

output_notebook()

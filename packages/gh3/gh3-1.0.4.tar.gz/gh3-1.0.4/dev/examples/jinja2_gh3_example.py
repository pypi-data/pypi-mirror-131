
"""Jinja2 integration example for gh3"""


import gh3
import jinja2


class Jinja2Plugin(gh3.Plugin):

  decorate_context_as = 'templating'

  def __init__(self, env: jinja2.Environment):
    self.env: jinja2.Environment = env

  def get(self, name):
    if not self.env:
      raise ValueError('environment has not been set')
    return self.env.get_template(name)

  def render(self, name, **kw):
    t = self.get(name)
    return t.render(**kw) 


hello_template = """
<h1>Headers</h1>

<p>Your request headers are:</p>

<pre>
{{ headers|e }}
</pre>
"""

templates = {'index': hello_template}


def index(ctx):
  html = ctx.templating.render('index', headers=ctx.req.headers)
  ctx.reply_html(html)


def make_app():
  app = gh3.App()
  loader = jinja2.DictLoader(templates)
  env = jinja2.Environment(loader=loader)
  app.add_plugin(Jinja2Plugin(env))
  app.add_route('/', index)
  return app


if __name__ == '__main__':
  app = make_app()
  app.debug()


# vim: ft=python sw=2 ts=2 sts=2 tw=80

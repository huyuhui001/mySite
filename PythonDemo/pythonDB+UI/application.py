import asyncio
import json
import logging
import os
from aiohttp import web
from jinja2 import Environment, FileSystemLoader
from webhandler import add_routes, add_static
logging.basicConfig(level=logging.INFO)


def init_jinja2(app, **kw):
    options = dict(
        autoescape=kw.get('autoescape', True),
        block_start_string=kw.get('block_start_string', '{%'),
        block_end_string=kw.get('block_end_string', '%}'),
        variable_start_string=kw.get('variable_start_string', '{{'),
        variable_end_string=kw.get('variable_end_string', '}}'),
        auto_reload=kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    logging.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env


async def data_factory(app, handler):
    pass


async def response_factory(app, handler):
    async def response(request):
        r = await handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(
                    body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response


async def init():
    app = web.Application(middlewares=[
        response_factory
    ])
    init_jinja2(app)
    add_routes(app, 'controller')
    add_static(app)

    appRunner = web.AppRunner(app)
    await appRunner.setup()
    tcpSite = web.TCPSite(appRunner, '127.0.0.1', 9000)
    await tcpSite.start()

event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(init())
event_loop.run_forever()

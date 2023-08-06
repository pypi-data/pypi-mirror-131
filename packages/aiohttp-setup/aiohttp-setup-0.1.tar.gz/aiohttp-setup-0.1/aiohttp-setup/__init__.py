import os
from aiohttp import web
from aiohttp.web import Application


def setup(host='localhost', port=8080, services=[], routes=None, 
        static_dir='public', index_file='index.html', root_path='/', 
        show_index=True):
    """ Setup aiohttp web server. """
    app = Application()
    if routes:
        app.add_routes(routes)
    if static_dir and index_file and root_path:
        static_path = static_dir if static_dir.startswith('./') \
            else f'./{static_dir}'
        index_path = f'{static_path}/{index_file}'
        if os.path.isdir(static_path) and os.path.isfile(index_path):
            async def index_handler(_):
                return web.FileResponse(index_path)
            app.router.add_get('/', index_handler)
            app.router.add_static(root_path, static_path, 
                    show_index=show_index)
    for service in services:
        start_service, stop_service = service
        app.on_startup.append(start_service)
        app.on_cleanup.append(stop_service)
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    setup()


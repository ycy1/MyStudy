def my_middleware(app):
    @app.middleware("http")
    async def middleware(request, call_next):
        print("请求前:")
        response = await call_next(request)
        print("请求后:")
        return response
    return app

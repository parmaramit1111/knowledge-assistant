from functools import wraps

def transactional(func):

    @wraps(func)
    async def wrapper(self, *args, **kwargs):

        async with self.context.session.begin():
            return await func(self, *args, **kwargs)

    return wrapper
import aiohttp

from aiohttp.client_exceptions import ContentTypeError

from qiwi_handler.exceptions import NotUrlWasSet, InvalidToken


class Request:
    main_url = "https://edge.qiwi.com/"
    api_url = "https://api.qiwi.com/"

    def __init__(self, token: str):
        self.token = token

    async def do_get(self, *, url: str = None, params: dict = None, headers: dict = None):
        f""":raise exceptions.NotUrlWasSet:
        """

        if url is None:
            raise NotUrlWasSet("Please, check req")

        link = Request.main_url + url

        for i in params:
            par = params[i]
            if isinstance(par, bool):
                params[i] = str(par)


        exit_params = {
            i: params[i]
            for i in params
            if params[i]

        }
        async with aiohttp.ClientSession() as session:
            if headers is None:
                session.headers['Accept'] = 'application/json'
                session.headers['authorization'] = 'Bearer ' + self.token
            else:
                for header in headers:
                    try:
                        session.headers['Accept'] = 'application/json'
                        session.headers.add(header, headers[header])
                    except ContentTypeError:
                        raise InvalidToken("Check your token")
            params = exit_params
            r = await session.get(url=link, params=params)
            return await r.json()

    async def do_put(self, *, url: str = None, data: dict = None, headers: dict = None):
        f""":raise exceptions.NotUrlWasSet:
        """

        if url is None:
            raise NotUrlWasSet("Please, check req")

        link = Request.api_url + url

        for i in data:
            dat = data[i]
            if isinstance(dat, bool):
               data[i] = str(dat)

        exit_data = {
            i: data[i]
            for i in data
            if data[i]
        }

        async with aiohttp.ClientSession() as session:
            if headers is None:
                session.headers['Accept'] = 'application/json'
                session.headers['Content-Type'] = 'application/json'
                session.headers['Authorization'] = 'Bearer ' + self.token
            else:
                for header in headers:
                    try:
                        session.headers['Accept'] = 'application/json'
                        session.headers.add(header, headers[header])
                    except ContentTypeError:
                        raise InvalidToken("Check your token")
            data = exit_data
            r = await session.put(url=link, data=data)

            return await r.json()

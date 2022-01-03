from django.shortcuts import render, redirect
from django.views.generic import CreateView
import aiohttp
import asyncio
import time


class Index(CreateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        url = request.POST.get('api_holder')
        return redirect('index')


start_time = time.time()


class ApiCall:

    async def get_pokemon(self, session, url, number):
        try:
            async with session.get(url) as resp:
                pokemon = resp.status, resp.request_info
                if resp.status == 200:
                    # await session.close()
                    print("200 done")
                elif resp.status == 401:
                    print('authentication required')
                return pokemon, number
        except (aiohttp.ClientConnectorError, aiohttp.ClientError):
            pass

    async def main(self, url, number_of_request):
        async with aiohttp.ClientSession() as session:
            tasks = (asyncio.create_task(self.get_pokemon(session, url, number)) for number in
                     range(1, number_of_request + 1))
            await asyncio.gather(*tasks)


obj = ApiCall()
requests_num = 10
# asyncio.run(main(f'http://www.7timer.info/bin/api.pl?lon=113.17&lat=23.09&product=astro&output=json', requests_num))
asyncio.run(obj.main(f'https://pokeapi.co/api/v2/pokemon/{5}', requests_num))


print("--- %s ms ---" % ((time.time() - start_time) * 1000))


# def authentication_in_url(username=None, password=None):
#     headers = {"Authorization": "Basic bG9naW46cGFzcw=="}
#     if username and password:
#         auth = aiohttp.BasicAuth(login=username, password=password, encoding='utf-8')
#         print(auth)

# authentication_in_url(username='viral', password=123)

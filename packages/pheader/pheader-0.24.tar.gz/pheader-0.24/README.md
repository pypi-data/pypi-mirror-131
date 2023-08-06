pheader
=============

simple parse string to dict headers data

```python:
>> import pheader
>> string_headers = """accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
    accept-encoding: gzip, deflate
    accept-language: en-US,en;q=0.9,id;q=0.8,ru;q=0.7
    sec-fetch-dest: document
    sec-fetch-mode: navigate
    sec-fetch-site: same-origin
    sec-fetch-user: ?1
    upgrade-insecure-requests: 1
    user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"""
>> headers = pheader.set_header(string_headers, origin = 'www.google.com')
>> print(headers)
>> {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	 'accept-encoding': 'gzip, deflate',
	 'accept-language': 'en-US,en;q=0.9,id;q=0.8,ru;q=0.7',
	 'sec-fetch-dest': 'document',
	 'sec-fetch-mode': 'navigate',
	 'sec-fetch-site': 'same-origin',
	 'sec-fetch-user': '?1',
	 'upgrade-insecure-requests': '1',
	 'origin': 'www.google.com',
	 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}
>>
>> string_headers = """accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/
   signed-exchange;v=b3;q=0.9\n\taccept-encoding: gzip, deflate\n\taccept-language: en-US,en;q=0.9,id;q=0.8,ru;q=0.7\n\tsec-fetch-dest: 
   document\n\tsec-fetch-mode: navigate\n\tsec-fetch-site: same-origin\n\tsec-fetch-user: ?1\n\tupgrade-insecure-requests: 1\n\tuser-agent: Mozilla/5.0 (X11; Linux x86_64) 
   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36""" 
>> headers = pheader.set_header(string_headers, referer = 'http://www.google.com')
>> print(headers)
>> {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	 'accept-encoding': 'gzip, deflate',
	 'accept-language': 'en-US,en;q=0.9,id;q=0.8,ru;q=0.7',
	 'sec-fetch-dest': 'document',
	 'sec-fetch-mode': 'navigate',
	 'sec-fetch-site': 'same-origin',
	 'sec-fetch-user': '?1',
	 'upgrade-insecure-requests': '1',
	 'referer': 'http://www.google.com',
	 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}
```
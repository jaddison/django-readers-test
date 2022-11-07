## Testing `django-readers` out
Having been introduced to the [`django-readers` package](https://github.com/dabapps/django-readers/) by one of the 
DabApps folks and gotten a good slide deck intro on it, I thought I would dig in and compare it to the plain old 
'standard' DRF approach. This repository is a series of comparative test view implementations, along with some crude 
benchmarks. 

### Setup
To replicate the setup for this test repo:

- clone the repo
- create a virtual environment
  - I used Python 3.10.3 via `pyenv`
  - `python -m venv venv`
- install the requirements into the virtual environment
  - `python venv/bin/pip install -r requirements.txt`
- create the database
  - `python manage.py migrate`
- populate the DB with `Faker`-based fake data
  - `python manage.py populate_db`
- run benchmarks of your choosing against the endpoints
  - I simply ran single concurrency `ab` against Django's `runserver` command

I enabled the [`django-debug-toolbar` package](https://github.com/jazzband/django-debug-toolbar) to let me easily see 
the number of queries being processed.

### 'Benchmarks'

[DRF-based 'basic'](./implementations/drf/views/basic.py) results (your bog standard non-optimized approach)

102 queries.

```commandline
➜  django-raid-test ab -n100 -c1 http://127.0.0.1:8000/drf/authors/basic/
This is ApacheBench, Version 2.3 <$Revision: 1901567 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient).....done


Server Software:        WSGIServer/0.2
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /drf/authors/basic/
Document Length:        486192 bytes

Concurrency Level:      1
Time taken for tests:   128.911 seconds
Complete requests:      100
Failed requests:        0
Total transferred:      48690929 bytes
HTML transferred:       48619200 bytes
Requests per second:    0.78 [#/sec] (mean)
Time per request:       1289.112 [ms] (mean)
Time per request:       1289.112 [ms] (mean, across all concurrent requests)
Transfer rate:          368.86 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       0
Processing:  1138 1289 128.8   1243    1678
Waiting:     1136 1286 128.5   1239    1675
Total:       1139 1289 128.8   1243    1679

Percentage of the requests served within a certain time (ms)
  50%   1243
  66%   1325
  75%   1360
  80%   1392
  90%   1499
  95%   1569
  98%   1659
  99%   1679
 100%   1679 (longest request)
```

[DRF-based 'with prefetch'](./implementations/drf/views/basic.py) results (with `.prefetch_related()` added to the 
'basic' approach)

3 queries.

```commandline
➜  django-raid-test ab -n100 -c1 http://127.0.0.1:8000/drf/authors/with-prefetch/
This is ApacheBench, Version 2.3 <$Revision: 1901567 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient).....done


Server Software:        WSGIServer/0.2
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /drf/authors/with-prefetch/
Document Length:        486200 bytes

Concurrency Level:      1
Time taken for tests:   37.152 seconds
Complete requests:      100
Failed requests:        0
Total transferred:      48691455 bytes
HTML transferred:       48620000 bytes
Requests per second:    2.69 [#/sec] (mean)
Time per request:       371.522 [ms] (mean)
Time per request:       371.522 [ms] (mean, across all concurrent requests)
Transfer rate:          1279.88 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:   309  371  67.5    338     620
Waiting:      307  369  67.4    336     618
Total:        309  371  67.5    338     621

Percentage of the requests served within a certain time (ms)
  50%    338
  66%    356
  75%    445
  80%    461
  90%    473
  95%    488
  98%    541
  99%    621
 100%    621 (longest request)
```

[DRF-based 'with prefetch and selected fields'](./implementations/drf/views/basic.py) results (with `.prefetch_related()` 
and `.only()` added to the 'basic' approach)

3 queries.

```commandline
➜  django-raid-test ab -n100 -c1 http://127.0.0.1:8000/drf/authors/with-prefetch-and-selected-fields/
This is ApacheBench, Version 2.3 <$Revision: 1901567 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient).....done


Server Software:        WSGIServer/0.2
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /drf/authors/with-prefetch-and-selected-fields/
Document Length:        486220 bytes

Concurrency Level:      1
Time taken for tests:   35.520 seconds
Complete requests:      100
Failed requests:        0
Total transferred:      48693446 bytes
HTML transferred:       48622000 bytes
Requests per second:    2.82 [#/sec] (mean)
Time per request:       355.197 [ms] (mean)
Time per request:       355.197 [ms] (mean, across all concurrent requests)
Transfer rate:          1338.76 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:   300  355  62.0    335     730
Waiting:      298  353  61.8    333     727
Total:        300  355  62.0    335     730

Percentage of the requests served within a certain time (ms)
  50%    335
  66%    350
  75%    407
  80%    414
  90%    422
  95%    457
  98%    523
  99%    730
 100%    730 (longest request)
```

[`django-readers`-based](./implementations/readers/views.py) results:

3 queries.

```commandline
➜  django-raid-test ab -n100 -c1 http://127.0.0.1:8000/readers/authors/
This is ApacheBench, Version 2.3 <$Revision: 1901567 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient).....done


Server Software:        WSGIServer/0.2
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /readers/authors/
Document Length:        486190 bytes

Concurrency Level:      1
Time taken for tests:   27.096 seconds
Complete requests:      100
Failed requests:        0
Total transferred:      48690498 bytes
HTML transferred:       48619000 bytes
Requests per second:    3.69 [#/sec] (mean)
Time per request:       270.962 [ms] (mean)
Time per request:       270.962 [ms] (mean, across all concurrent requests)
Transfer rate:          1754.83 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:   228  271  43.5    247     379
Waiting:      226  268  43.6    245     376
Total:        228  271  43.5    247     379

Percentage of the requests served within a certain time (ms)
  50%    247
  66%    275
  75%    316
  80%    321
  90%    347
  95%    361
  98%    369
  99%    379
 100%    379 (longest request)
```

As you can see, based on the data I had generated in the DB at the time of running these tests, `django-readers` still 
outperforms an 'optimized' DRF approach - and perhaps appears to be more consistent in response timing. [_Do let me 
know if I have missed optimizations that could help to match numbers/outcomes._]

This indicates that there is some interesting internal differences between how `django-readers` serializes the payload 
compared to DRF.
There is likely other machinery in DRF views/serializers that isn't getting called in `django-readers` (validation, etc?).

### Other observations

I think it is a very neat way of dealing with reader-like implementations; to simplify the code for such views. However, 
it is important to recognize the added cognitive load in a system with both read/write needs.

In such a system, `django-readers` would be able to easily handle read-related output needs - but one would need to fall 
back on DRF-based serialization anyhow for PUT and POST actions. If a PUT/POST request also returned the created/updated
record, then there might be duplicate serialization approaches necessary.

Of course, there's more goodies under the hood of the package, dealing with counts/annotations and more - 
[read the `django-readers` docs](https://www.django-readers.org/)! 
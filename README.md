Write a Python program which will query the first 500 repositories on GitHub 
using their public API.

https://developer.github.com/v3/search/#search-repositories

It must be callable from the command line as shown below.

    $ python github.com.py --q=.. --sort=... --order=...

Examples:
    $ python github.com.py --q=ninja+language:python --sort=stars --order=asc
    $ python github.com.py --q=ninja+language:javascript --sort=forks --order=asc
    
Output:

    A pretty printed list of results (using pprint()).

Constraints:

    - The API in question provides a maximum of 100 results per page. Since we 
      want 500 results, you must query the first 5 pages in parallel.
    
    - Use a local filesystem-based cache. i.e.: Repeated calls to the API with 
      the same input must be avoided (to satisfy rate limit constraints).
      Usehttp://beaker.readthedocs.io/en/latest/caching.html or 
      https://bitbucket.org/zzzeek/dogpile.cache

Plan:

    read q, sort and order from the command line
    create 5 threads or processes (or use Celery)
        queryhttps://api.github.com/search/repositories?q=...&sort=...&order=...&per_page=100&page=1
            only if not already queried (check cache)
        queryhttps://api.github.com/search/repositories?q=...&sort=...&order=...&per_page=100&page=2
            only if not already queried (check cache)
        queryhttps://api.github.com/search/repositories?q=...&sort=...&order=...&per_page=100&page=3
            only if not already queried (check cache)
        queryhttps://api.github.com/search/repositories?q=...&sort=...&order=...&per_page=100&page=4
            only if not already queried (check cache)
        queryhttps://api.github.com/search/repositories?q=...&sort=...&order=...&per_page=100&page=5
            only if not already queried (check cache)
    aggregate results from all threads
    combine aggregated results
    pprint(...)
    
    
 

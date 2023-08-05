# ulozto-search
Search uloz.to for files using Python. It only supports one-page query for now. 

## Usage

``` python
import ulozto_search

query = "your_query"
file_type = "documents|videos|images|archives|audios"  # optional
kwargs = {
    "insecure": False   # disables SSL check, optional, default False
}

# search and return dictionary
ulozto_search.search(query, file_type, **kwargs)

# search and return HTML string
ulozto_search.searchHTML(query, file_type, **kwargs)
```

It can be also used from terminal:

```
$ ulozto-search -h
usage: ulozto-search [-h] [-t {documents,videos,images,archives,audios}] [--insecure] query

positional arguments:
  query                 String to query uloz.to

optional arguments:
  -h, --help            show this help message and exit
  -t {documents,videos,images,archives,audios}, --type {documents,videos,images,archives,audios}
                        Filter by file type
  --insecure            Don't verify SSL certificates, not recommended

```

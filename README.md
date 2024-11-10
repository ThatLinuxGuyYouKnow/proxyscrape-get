# ProxyScrape - Get

A simple python script to test for currently viable proxies from [proxyscrapes proxy list]('https://proxyscrape.com/free-proxy-list').

## Features

* Automatically removes empty and duplicate proxies
* checks proxies vs [Sofascore]('https://sofascore.com') one of the **strictest** anti bot platforms(if it works there, it'll *probably* work on most other platforms)
* returns viable proxies[TODO]
* verbose logging

## Like this? Clone this repository !

But first, make sure you have:

> Python 3.+ 

and

> The requests library

And now you can:

```
git clone github.com/ThatLinuxGuyYouKnow/proxyscrape-get
```

### Run this

```
cd proxyscrape-get && python3 app.py
```

## TODO's
- [ ] test proxies concurrently
- [ ] return viable proxies as a list
- [ ] add optioning to reduce noisy logging



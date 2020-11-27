About
=====

This module provides the **SitemapRange** class and a tool to allow command-line usage **sitemap_fetch.py**.

The class **SitemapRange** is meant primarily as a generic building block for creating news aggregating applications where the datasources
are [spec-compliant](https://www.sitemaps.org/protocol.html) news websites.

There are some fault-tolerance features included to deal with some inconsistencies in sitemaps.

Install
=======

To install from pypi:

    pip3 install --user sitemap-range-fetch

Usage
=====

Fetching all news articles on [cnn.com](http://cnn.com) in the past 6 days, and format the result as [JSON](https://en.wikipedia.org/wiki/JSON):

    sitemap_fetch.py --site "https://cnn.com" --format json --daysago 6

Here is an example of using the **SitemapRange** class in your code:

    from sitemap_range.sitemap_range import SitemapRange
    from datetime import datetime, timedelta
    sr = SitemapRange("https://cnn.com")
    in_range = sr.get_articles_in_range(start=datetime.now()-timedelta(days=3), end=datetime.now(), opts={})
    print(in_range)

The `get_articles_in_range` method returns a list of dictionaries, where each dictionary has two
keys: `"url"` and `"dt"` which is an [ISO 8601 formatted datetime string](https://en.wikipedia.org/wiki/ISO_8601) (as returned by the 
[isoformat method](https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat)).


More details about the CLI switches:

```
    usage: sitemap_fetch.py [-h] --site SITE [--format FORMAT] [--daysago DAYSAGO]
                            [--notz] [--advanced]

    Tool for extracting articles from news websites

    optional arguments:
      -h, --help         show this help message and exit
      --site SITE        the url for the website
      --format FORMAT    the url for the website
      --daysago DAYSAGO  defines the oldest date of an article that will be
                         selected (default: 2 days ago)
      --notz             strip the timezone from the dates before selection
                         (processing is more fault-tolerant)
      --advanced         use a more fault-tolerant parser
```

Details
=======

This module is provided as is under [MIT License](https://opensource.org/licenses/MIT).

For extensions, customizations or business inquiries you can [get in touch here](mailto:business@garage-coding.com).

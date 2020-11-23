About
=====

This module provides the **SitemapRange** class and a tool to allow command-line usage **sitemap_fetch.py**.

The class **SitemapRange** is meant primarily as a generic building block for creating news aggregating applications where the datasources are [spec-compliant](https://www.sitemaps.org/protocol.html) news websites.

There are some fault-tolerance features included to deal with some inconsistencies in sitemaps.

Install
=======

To install from pypi:

    pip install --user sitemap-range-fetch

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

Details
=======

This module is provided as is under [MIT License](https://opensource.org/licenses/MIT).

For extensions, customizations or business inquiries you can [get in touch here](mailto:business@garage-coding.com).

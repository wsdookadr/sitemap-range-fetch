import sys
import re
import requests
from io import StringIO
from datetime import datetime, timedelta
from lxml import etree
"""

This class extracts articles from sitemaps using time constraints.

The algorithm is composed of the following steps:
1) fetch all "Sitemap:" entries found in robots.txt
2) the entry can be of type sitemapindex or urlset
3.1) if it's an urlset, go over all articles in it, and select
     those within the time range.
3.2) if it's of type sitemapindex, select those in the timerange
4) for the sitemaps that were found in 3.2, fetch them and get the
   articles that are within the given timerange

So steps 3.2 and 4 are handling a simple-nested hierarchy.

Sitemap hierarchy example:

. robots.txt
.. sitemapindex
... urlset
... urlset
.. sitemapindex
... urlset
.. sitemapindex
... urlset
... urlset
... urlset
.. urlset
.. urlset

Refer to [1] for more details on the sitemap protocol.

[1] https://www.sitemaps.org/protocol.html#sitemapIndex_sitemap

"""
class SitemapRange:

    def __init__(self, domain):
        self.domain = domain

    def get_page(self, url, raw=True):
        r = requests.get(url)
        if raw:
            return r.content
        else:
            return r.text

    def get_sitemap_urls(self):
        robots_txt = self.get_page(self.domain + "/robots.txt", raw=False)
        for line in robots_txt.split("\n"):
            g = re.match(r"^Sitemap: (.*)$", line)
            if g and len(g.groups()) > 0:
                sitemap_url = (g.groups())[0]
                yield sitemap_url

    def handle_sitemapindex(self, parse_tree, start, end):
        if parse_tree is not None:
            for x in parse_tree.getroottree().xpath('.//*[name() = "sitemap"]'):
                y = x.xpath('.//*[name() = "loc"]/text()')
                z = x.xpath('.//*[name() = "lastmod"]/text()')
                if len(z) > 0:
                    z = z[0]
                    if z[-1] == 'Z':
                        z = z[:-1]
                    dt = datetime.fromisoformat(z)

                    if dt >= start and dt <= end:
                        yield({"url": y[0], "dt": dt})

    def handle_urlset(self, parse_tree, start, end):
        if parse_tree is not None:
            for x in parse_tree.getroottree().xpath('.//*[name() = "url"]'):
                y = x.xpath('.//*[name() = "loc"]/text()')
                z1 = x.xpath('.//*[name() = "news:news"]/*[name() = "news:publication_date"]/text()')
                z2 = x.xpath('.//*[name() = "lastmod"]/text()')

                z = None
                if z1 is not None and len(z1) > 0:
                    z = z1
                elif z2 is not None and len(z2) > 0:
                    z = z2

                if z is not None and len(z) > 0:
                    z = z[0]
                    if z[-1] == 'Z':
                        z = z[:-1]
                    dt = datetime.fromisoformat(z)

                    if dt >= start and dt <= end:
                        ret = {"url": y[0], "dt": dt}
                        yield(ret)

    def get_articles_in_range(self, start=datetime.now(), end=datetime.now()):
        # 1st pass
        articles = []
        sitemaps = []
        for u in self.get_sitemap_urls():
            print("Processing sitemap:"+u)
            parse_tree = None
            try:
                xml = self.get_page(u)
                parse_tree = etree.XML(xml)
            except etree.XMLSyntaxError as e:
                pass
            except Exception as e:
                print("ERROR 1: " + str(e))
                pass

            if parse_tree is not None:
                root_tag = parse_tree.tag
                root_tag = re.sub(r"^[^}]+}","",root_tag)
                if root_tag == "sitemapindex":
                    for o in self.handle_sitemapindex(parse_tree, start, end):
                        sitemaps.append(o)
                elif root_tag == "urlset":
                    for o in self.handle_urlset(parse_tree, start, end):
                        articles.append(o)
        # 2nd pass
        for sm in sitemaps:
            print("Processing sitemap:"+sm["url"])
            parse_tree = None
            try:
                xml = self.get_page(sm["url"])
                parse_tree = etree.XML(xml)
            except etree.XMLSyntaxError as e:
                pass
            except Exception as e:
                print("ERROR 2: " + str(e))
                pass
            if parse_tree is not None:
                for o in self.handle_urlset(parse_tree, start, end):
                    articles.append(o)
        
        return articles




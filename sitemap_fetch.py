from datetime import datetime, timedelta
from sitemap_range import SitemapRange
if __name__ == "__main__":
    o = SitemapRange("http://cnn.com")
    #o = SitemapRange("http://cbsnews.com")
    #o = SitemapRange("https://www.washingtonpost.com")
    #o = SitemapRange("http://www.nytimes.com")
    start_ = datetime.now() - timedelta(days=2)
    end_   = datetime.now() + timedelta(days=2)
    articles_in_range = o.get_articles_in_range(start=start_,end=end_)
    print(articles_in_range)


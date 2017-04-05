if __name__ == '__main__':
    from scrapy import cmdline
    # cmdline.execute("scrapy crawl jd -L INFO".split())
    cmdline.execute("scrapy crawl banggo -L WARNING -s LOG_FILE=banggo.log".split())

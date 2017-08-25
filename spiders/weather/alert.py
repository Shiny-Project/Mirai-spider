from core import spider
import json


class AlertSpider(spider.Spider):
    """全国预警定点监控"""

    def __init__(self):
        super(AlertSpider, self).__init__()
        self.name = 'AlertSpider'

    def main(self):
        result = self.fetch("http://www.12379.cn/data/alarm_list_all.html").decode("utf-8")
        data = json.loads(result)
        for item in data["alertData"]:
            if ("杭州" in item["description"] or "上海" in item["description"] or "郑州" in item["description"]) and ("县" not in item["description"] and "区" not in item["description"]):
                self.record(3, {
                    "title": "中国·预警速报",
                    "content": item["headline"],
                    "link": "http://www.12379.cn/data/alarmcontent.shtml?file={}.html".format(item["identifier"])
                })

    def check(self, timestamp):
        return self.check_expiration(timestamp, 180)
import json
from datetime import datetime
from typing import Iterator, Tuple, Dict
from random import Random
from time import sleep
from os import path

import requests


class GetHoliday:
    BASE_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://www.baidu.com/s?ie=UTF-8&wd=%E6%97%A5%E5%8E%86"
    }

    def __init__(self):
        now = datetime.now()
        self.__start_date = (now.day, now.month, now.year)
        self.__end_date = (now.day, now.month, now.year)
        self.__year = datetime.now().year
        self.__month = datetime.now().month
        self.__base_url = f"https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&type=json&resource_id=52109&query={self.__year}年{self.__month}月&apiType=yearMonthData&cb=jsonp_1733714370339_90870"
        self.__calendar = {}

    @property
    def start_date(self) -> Tuple[int, int, int]:
        return self.__start_date

    @start_date.setter
    def start_date(self, value: Tuple[int, int, int]):
        """
        设置开始日期
        :param value: Tuple[day, month, year]
        """
        day, month, year = value
        self.__start_date = day, month, year

    @property
    def end_date(self) -> Tuple[int, int, int]:
        return self.__end_date

    @end_date.setter
    def end_date(self, value: Tuple[int, int, int]):
        """
        设置结束日期
        :param value: Tuple[day, month, year]
        """
        day, month, year = value
        self.__end_date = day, month, year

    def _update_url(self) -> str:
        self.__base_url = f"https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&type=json&resource_id=52109&query={self.__year}年{self.__month}月&apiType=yearMonthData&cb=jsonp_1733714370339_90870"
        return self.__base_url

    @staticmethod
    def random_sec() -> float:
        result = Random().random() * 5
        return result if result > 1 else result + 1

    @staticmethod
    def jsonp_to_dict(jsonp: str) -> Dict:
        start_index = jsonp.index('(') + 1
        end_index = jsonp.rindex(')')
        return json.loads(jsonp[start_index:end_index])

    def _iterate_months(self) -> Iterator[datetime]:

        start_day, start_month, start_year = self.__start_date
        start_date = datetime(year=start_year, month=start_month, day=start_day)

        end_day, end_month, end_year = self.__end_date
        end_date = datetime(year=end_year, month=end_month, day=end_day)

        current_date = start_date

        while current_date <= end_date:
            yield current_date
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)

    def get_holiday(self):

        for current_date in self._iterate_months():
            self.__month, self.__year = current_date.month, current_date.year

            print(f'开始请求{self.__year}年 {self.__month}月节假日数据...')

            url = self._update_url()
            response = requests.get(url=url)
            response_json = GetHoliday.jsonp_to_dict(response.text)

            result: list = response_json.get('Result')[0].get('DisplayData') \
                .get('resultData').get('tplData').get('data') \
                .get('almanac')

            for item in result:
                if item.get('month') != str(self.__month) and item.get('year') != str(self.__year):
                    continue

                key = f"{item.get('year')}/{item.get('month')}/{item.get('day')}"

                # 接口返回结果中：
                # status 1: 法定节假日
                # status 2: 补班

                # 写入结果中：
                # status 0: 工作日
                # status 1: 周末
                # status 2: 法定假

                status = 2 if item.get('status') == '1' else 0
                status = 1 if status == 0 and item.get('week') in ('6', '7') else status

                value = "法定假" if status == 2 else "工作日" if status == 0 else "周末"
                value = "补班" if value == "工作日" and item.get('status') == '2' else value

                self.__calendar[key] = {
                    "date": key,
                    "status": status,
                    "value": value,
                    "detail": item
                }

            sleep(GetHoliday.random_sec())

            print("=" * 50)

    def write_to_file(self, overwrite_base: bool = False, separate: bool = False):
        """
        将结果写入文件
        separate开启时，会将基础的holiday.json替换为当前爬取的时间，然后将原始的holiday.json写入到holiday_custom.json文件中
        separate关闭时，会将当前爬取的时间与原始的holiday.json合并，然后将结果写入到holiday.json文件中
        :param overwrite_base: 是否覆盖基础的holiday.json文件
        :param separate: 是否将结果写入到单独的holiday_custom.json文件，只有当overwrite_base为True时有效
        :return:
        """
        utils_path = path.abspath(path.dirname(__file__))
        root_path = path.abspath(path.join(utils_path, '..'))
        public_path = path.join(root_path, 'public')

        if not overwrite_base:
            start_day, start_month, start_year = self.__start_date
            end_day, end_month, end_year = self.__end_date
            with open(path.join(public_path, f"holiday_{start_year}{start_month}-{end_year}{end_month}.json"), 'w',
                      encoding='utf-8') as f:
                json.dump(self.__calendar, f, ensure_ascii=False, indent=4)
            return

        try:
            with open(path.join(public_path, 'holiday.json'), 'r', encoding='utf-8') as fr:
                base_calendar: Dict = json.load(fr)
        except (json.JSONDecodeError, FileNotFoundError):
            base_calendar = {}

        with open(path.join(public_path, 'holiday.json'), 'w', encoding='utf-8') as fw:
            if separate:
                json.dump(self.__calendar, fw, ensure_ascii=False, indent=4)

                keys = list(base_calendar.keys()) if base_calendar else []
                if keys:
                    start_date, end_date = keys[0], keys[-1]
                    start_year, start_month, start_day = start_date.split('/')
                    end_year, end_month, end_day = end_date.split('/')
                    with open(path.join(public_path, f"holiday_{start_year}{start_month}-{end_year}{end_month}.json"),
                              'w',
                              encoding='utf-8') as f:
                        json.dump(base_calendar, f, ensure_ascii=False, indent=4)
            else:
                base_calendar.update(self.__calendar)
                json.dump(base_calendar, fw, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    gh = GetHoliday()
    gh.start_date = (1, 1, 2020)
    gh.end_date = (1, 12, 2025)
    gh.get_holiday()
    gh.write_to_file(overwrite_base=True)

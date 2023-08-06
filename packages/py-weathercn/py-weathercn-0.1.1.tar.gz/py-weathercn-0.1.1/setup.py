# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weathercn']

package_data = \
{'': ['*'], 'weathercn': ['icons/*']}

install_requires = \
['arrow>=0.13.1,<0.14.0',
 'css-parser>=1.0,<2.0',
 'fclist-cffi>=1.1.2,<2.0.0',
 'pillow>=6,<9',
 'regex>=2019.4,<2020.0',
 'requests>=2.21,<3.0']

entry_points = \
{'console_scripts': ['weathercn = weathercn.main:main']}

setup_kwargs = {
    'name': 'py-weathercn',
    'version': '0.1.1',
    'description': '中国天气python插件',
    'long_description': '实时天气图片生成器\n================================\n\n### 介绍\n根据中国天气网生成天气信息，抓取最近四天内的天气以及实时数据，\n附带一些农历日历信息。\n\n### 效果预览\n![Alt text](https://github.com/ssfdust/weatherCN/raw/master/screenshots/weather.png)\n\n### 安装\n\n```\npip install py-weathercn --user\n```\n\n### 使用\n```\nweathercn -f <自定义字体> <城市ID或城市名>\n```\n* 城市ID：如http://www.weather.com.cn/weather1d/101190401.shtml 中的101190401\n* 将会在用户文件夹下生成.cache/weatherCN目录，为缓存weather.json, weather.png, icon.png文件\n* weather.json为json文件\n* weather.png为生成图片\n* icon.png为当前天气的icon图标（例如用于waybar等）\n* 自定义字体支持路径，fontconfig\n\n### json展示\n```json\n{\n    "current": {\n        "humidity": "79%",\n        "wind_direction": "东南风 ",\n        "wind_level": "3级",\n        "air_quality": "29",\n        "air_pressure": "1004",\n        "updateat": "09:55",\n        "cur_weather": "阴",\n        "temperature": "23 ℃",\n        "weather": "小雨转阴",\n        "dcode": "d07",\n        "ncode": "d02",\n        "high": "25 ℃",\n        "low": "21 ℃",\n        "code": "d02",\n        "unsuited": "修坟-安葬-入宅-安门-安床",\n        "suited": "嫁娶-移徙-赴任-除服-纳采",\n        "lunar": "四月十三",\n        "shizhai": ""\n    },\n    "forcast": [\n        {\n            "date": "五月18日",\n            "weekday": "星期六",\n            "high": "25",\n            "low": "18",\n            "dcode": "d01",\n            "ncode": "n01",\n            "weather": "多云"\n        },\n        {\n            "date": "五月19日",\n            "weekday": "星期日",\n            "high": "27",\n            "low": "20",\n            "dcode": "d02",\n            "ncode": "n01",\n            "weather": "阴转多云"\n        },\n        {\n            "date": "五月20日",\n            "weekday": "星期一",\n            "high": "23",\n            "low": "16",\n            "dcode": "d01",\n            "ncode": "n00",\n            "weather": "多云转晴"\n        }\n    ]\n}\n```\n\n### json释义\n1. humidity: 湿度\n2. wind_level: 风级\n3. wind_direction: 风向\n4. air_quality: 空气质量\n5. air_pressure: 气压\n6. updateat: 更新时间\n7. cur_weather: 当前天气\n8. temperature: 当前气温\n9. weather: 小雨转阴,\n10. dcode: 白天天气图标\n11. ncode: 夜间天气图标\n12. high: 最高温度\n13. low: 最低温度\n14. code: 当前天气图标\n15. unsuited: 不宜\n16. suited: 宜\n17. lunar: 农历\n18. shizhai: 是否是地藏十斋日\n19. date: 日期\n\n',
    'author': 'ssfdust',
    'author_email': 'ssfdust@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

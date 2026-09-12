from mcp.server.mcpserver import MCPServer
import requests
import xml.etree.ElementTree as ET


mcp = MCPServer("simple-server")


@mcp.tool()
def get_weather(city: str) -> str:
    city_query = normalize_city_query(city)

    try:
        geocoding_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city_query,
                "count": 1,
                "language": "zh",
                "format": "json",
            },
            timeout=10,
        )
        geocoding_response.raise_for_status()
    except requests.RequestException as error:
        return f"天气查询失败：{error}"

    geocoding_data = geocoding_response.json()

    results = geocoding_data.get("results", [])
    if not results:
        return f"未找到城市：{city}"

    location = results[0]
    try:
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": (
                    "temperature_2m,apparent_temperature,relative_humidity_2m,"
                    "precipitation,rain,weather_code,wind_speed_10m"
                ),
                "timezone": "auto",
            },
            timeout=10,
        )
        weather_response.raise_for_status()
    except requests.RequestException as error:
        return f"天气查询失败：{error}"

    weather_data = weather_response.json()

    current = weather_data["current"]
    current_units = weather_data.get("current_units", {})
    weather_text = get_weather_text(current.get("weather_code"))
    is_raining = current.get("rain", 0) > 0 or current.get("precipitation", 0) > 0

    place = format_place(location)
    return (
        f"{place} 当前天气：{weather_text}。"
        f"是否下雨：{'是' if is_raining else '否'}。"
        f"温度：{current['temperature_2m']}{current_units.get('temperature_2m', '')}，"
        f"体感温度：{current['apparent_temperature']}{current_units.get('apparent_temperature', '')}，"
        f"湿度：{current['relative_humidity_2m']}{current_units.get('relative_humidity_2m', '')}，"
        f"风速：{current['wind_speed_10m']}{current_units.get('wind_speed_10m', '')}，"
        f"降水量：{current['precipitation']}{current_units.get('precipitation', '')}，"
        f"更新时间：{current['time']}。"
    )


@mcp.tool()
def get_hot_news() -> str:
    try:
        response = requests.get(
            "https://news.google.com/rss?hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
            headers={
                "User-Agent": "uni-agent-learning-project/1.0"
            },
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        return f"热点新闻查询失败：{error}"

    root = ET.fromstring(response.content)
    items = root.findall("./channel/item")

    if not items:
        return "未找到热点新闻。"

    news_lines = ["当前热点新闻前三条："]
    for index, item in enumerate(items[:3], start=1):
        title = item.findtext("title", default="无标题")
        link = item.findtext("link", default="")
        published_at = item.findtext("pubDate", default="未知时间")

        news_lines.append(f"{index}. {title}")
        news_lines.append(f"   发布时间：{published_at}")
        if link:
            news_lines.append(f"   链接：{link}")

    return "\n".join(news_lines)


def format_place(location: dict) -> str:
    return "，".join(
        part
        for part in [
            location.get("name"),
            location.get("admin1"),
            location.get("country"),
        ]
        if part
    )


def get_weather_text(weather_code: int) -> str:
    weather_code_text = {
        0: "晴朗",
        1: "大致晴朗",
        2: "局部多云",
        3: "阴天",
        45: "有雾",
        48: "结霜雾",
        51: "小毛毛雨",
        53: "中等毛毛雨",
        55: "大毛毛雨",
        56: "轻微冻毛毛雨",
        57: "较强冻毛毛雨",
        61: "小雨",
        63: "中雨",
        65: "大雨",
        66: "轻微冻雨",
        67: "较强冻雨",
        71: "小雪",
        73: "中雪",
        75: "大雪",
        77: "雪粒",
        80: "小阵雨",
        81: "中等阵雨",
        82: "强阵雨",
        85: "小阵雪",
        86: "强阵雪",
        95: "雷暴",
        96: "雷暴伴小冰雹",
        99: "雷暴伴大冰雹",
    }
    return weather_code_text.get(weather_code, f"未知天气代码 {weather_code}")


def normalize_city_query(city: str) -> str:
    city_aliases = {
        "上海": "Shanghai",
        "北京": "Beijing",
        "深圳": "Shenzhen",
        "广州": "Guangzhou",
        "湛江": "Zhanjiang",
        "赣江": "Ganjiang",
    }
    return city_aliases.get(city.strip(), city.strip())


if __name__ == "__main__":
    mcp.run()

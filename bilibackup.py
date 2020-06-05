import requests
import math
import subprocess
from concurrent.futures import ThreadPoolExecutor


def get_json(url):
    r = requests.get(url)
    return r.json()


def get_count(mid: int) -> int:
    video_info = get_json(
        f'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={mid}&pagesize=1&tid=0&page=1&keyword=&order=pubdate')
    count = video_info['data']['count']
    return count


def get_video_list(mid, count):
    result = []
    for i in range(math.ceil(count / 50)):
        rawJson = get_json(
            f'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={mid}&pagesize=50&tid=0&page={i}&keyword=&order=pubdate')
        for v in rawJson['data']['vlist']:
            result.append(v)
    return result


def downloadVideo(video):
    url = f"https://www.bilibili.com/video/av{video['aid']}"
    title = video['title'].replace("/", "")
    co: list = ['youtube-dl', '-o', title+".ts", url]
    subprocess.run(co)


def main(mid):
    count = get_count(mid)
    video_list = get_video_list(mid, count)
    pool = ThreadPoolExecutor(16)
    for v in video_list:
        pool.submit(downloadVideo, v)


if __name__ == '__main__':
    main(336731767)

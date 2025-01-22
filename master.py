from youtube_downloader import YouTubeDownloader


# 初始化下载器，使用 aria2c 并设置 16 个线程
downloader = YouTubeDownloader(use_aria2c=True, aria2c_threads=16)

url = input("请输入 YouTube 视频链接: ")

# # 下载视频并合并音频
# print("正在下载视频并合并音频...")
# downloader.download_video_with_audio(url)
# print("视频下载完成！")
# 仅下载音频流
print("正在仅下载音频流...")
downloader.download_audio_only(url)
print("音频流下载完成！")
from yt_dlp import YoutubeDL

class YouTubeDownloader:
    def __init__(self, use_aria2c=False, aria2c_threads=16, concurrent_fragments=4):
        """
        初始化下载器
        :param use_aria2c: 是否使用 aria2c 作为外部下载器
        :param aria2c_threads: aria2c 的线程数（仅当 use_aria2c=True 时生效）
        :param concurrent_fragments: 多片段下载的线程数（仅当 use_aria2c=False 时生效）
        """
        self.use_aria2c = use_aria2c
        self.aria2c_threads = aria2c_threads
        self.concurrent_fragments = concurrent_fragments

    def _get_ydl_opts(self, format_code, output_template, extract_audio=False):
        """
        获取 yt-dlp 的配置选项
        :param format_code: 下载格式（如 bestvideo+bestaudio/best）
        :param output_template: 输出文件名模板
        :param extract_audio: 是否提取音频
        :return: yt-dlp 配置字典
        """
        ydl_opts = {
            'format': format_code,
            'outtmpl': output_template,
            'merge_output_format': 'mp4',  # 合并后的输出格式
        }

        if extract_audio:
            ydl_opts['postprocessors'] = [{  # 后处理：将音频转换为 MP3
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]

        if self.use_aria2c:
            # 使用 aria2c 作为外部下载器
            ydl_opts['external_downloader'] = 'aria2c'
            ydl_opts['external_downloader_args'] = [
                '-x', str(self.aria2c_threads),  # 设置最大连接数
                '-s', str(self.aria2c_threads),  # 设置分片数
                '-k', '1M',  # 设置分片大小
            ]
        else:
            # 使用内置的多片段下载
            ydl_opts['concurrent_fragment_downloads'] = self.concurrent_fragments

        return ydl_opts

    def download_video_with_audio(self, url, output_template='%(title)s.%(ext)s'):
        """
        下载视频并自动合并音频流
        :param url: YouTube 视频链接
        :param output_template: 输出文件名模板
        """
        ydl_opts = self._get_ydl_opts('bestvideo+bestaudio/best', output_template)
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def download_video_only(self, url, output_template='%(title)s_video.%(ext)s'):
        """
        仅下载视频流（不包含音频）
        :param url: YouTube 视频链接
        :param output_template: 输出文件名模板
        """
        ydl_opts = self._get_ydl_opts('bestvideo', output_template)
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def download_audio_only(self, url, output_template='%(title)s_audio.%(ext)s'):
        """
        仅下载音频流（不包含视频）
        :param url: YouTube 视频链接
        :param output_template: 输出文件名模板
        """
        ydl_opts = self._get_ydl_opts('bestaudio', output_template, extract_audio=True)
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


# 示例用法
if __name__ == '__main__':
    # 初始化下载器，使用 aria2c 并设置 16 个线程
    downloader = YouTubeDownloader(use_aria2c=True, aria2c_threads=16)

    url = input("请输入 YouTube 视频链接: ")

    # 下载视频并合并音频
    print("正在下载视频并合并音频...")
    downloader.download_video_with_audio(url)
    print("视频下载完成！")

    # 仅下载视频流
    print("正在仅下载视频流...")
    downloader.download_video_only(url)
    print("视频流下载完成！")

    # 仅下载音频流
    print("正在仅下载音频流...")
    downloader.download_audio_only(url)
    print("音频流下载完成！")
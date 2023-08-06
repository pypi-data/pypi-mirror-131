import sys
import os
import sys
import re
import pyperclip
import emoji
from rich.prompt import Prompt

from youtube_video_downloader import single_video
from youtube_video_downloader import playlist_video
from youtube_video_downloader import console

ask = Prompt().ask


def get_desktop_path() -> str:
    """Desktop path finder

    Returns:
        str: The Desktop path
    """

    if sys.platform == 'win32':
        user_profile: str = os.getenv('USERPROFILE')
        desktop_path: str = os.path.join(user_profile, 'Desktop')

        return desktop_path if os.path.exists(desktop_path) else os.path.join(
            user_profile, 'OneDrive', 'Desktop')


def main():
    """The entry point to the application

    """
    url: str
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = pyperclip.paste()

    if not url:
        print(emoji.emojize(":warning: "), end='')
        console.print('[red]youtube url was not specified[/]')
    else:
        try:
            yt_url = re.search(
                r'https://www.youtube.com/watch\?v=.*|https://www.youtube.com/playlist\?list=.*',
                url)[0]
            console.print(f'[green]:thumbs_up:{yt_url}[/]')
        except TypeError as e:
            console.print(
                f'[red]:thumbs_down: This url, {url} is not a valid youtube url[/]')
        else:
            desired_path = ask('[cyan]Enter folder path[/]')
            folder_path = desired_path if os.path.exists(
                desired_path) else get_desktop_path()
            if 'watch' in url:
                single_video(url=yt_url, folder_path=folder_path)
            else:
                playlist_video(url=yt_url, folder_path=folder_path)


if __name__ == '__main__':
    main()

import os
import re
import requests
from tqdm import tqdm
from pytube import YouTube, Playlist

from youtube_video_downloader import console


def single_video(url: str, folder_path: str) -> None:
    """Single video downloader function

    Args:
        url (str): The url of the youtube video to download
        folder_path (str): The path to which the folder should be saved
    """
    yt = YouTube(url)
    stream = yt.streams.filter(
        file_extension='mp4',
        progressive=True).get_by_itag(22)
    url: str = stream.url
    title: str = re.sub(r'[|!@#$%^&*()+-\/,]', '', stream.title)
    chunk_size: int = 1024
    r = requests.get(url, stream=True)
    total_size: int = int(r.headers['content-length'])
    file_path: str = os.path.join(folder_path, f'{title}.mp4')

    with open(f'{file_path}', 'wb') as f:
        print(f'Downloading {title}')
        for data in tqdm(
                iterable=r.iter_content(chunk_size=chunk_size),
                leave=True,
                total=total_size / chunk_size,
                unit='KB',
                colour='green'):

            f.write(data)

    console.print(':white_check_mark:', end="")
    console.print(f'[green]{title} successfully downloaded[/]')


def playlist_video(url: str, folder_path: str) -> None:
    """ Playlist downloader function

    Args:
        url (str): The url of the playlist video to download
        folder_path (str): The path to which the folder should be saved
    """

    playlist = Playlist(url)

    playlist_folder = os.path.join(folder_path, playlist.title)

    try:
        os.mkdir(playlist_folder)
    except Exception as e:
        print(e)
    else:
        for yt_url in playlist.video_urls:
            single_video(yt_url, folder_path=playlist_folder)


if __name__ == '__main__':
    pass

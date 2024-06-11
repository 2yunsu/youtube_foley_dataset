import yt_dlp
import os
import re

def sanitize_filename(filename):
    # 컴퓨터가 읽지 못하는 문자를 제거하고, 띄어쓰기를 밑줄로 변경
    return re.sub(r'[^a-zA-Z0-9_.]', '_', filename)

def rename_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        sanitized_name = sanitize_filename(filename)
        # 기존 파일 이름과 새로운 파일 이름이 다를 경우에만 이름을 변경
        if filename != sanitized_name:
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, sanitized_name)
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {filename} -> {sanitized_name}')

# channel_url = 'https://www.youtube.com/@JoshHarmon/shorts'
# channel_url = 'https://www.youtube.com/@reelfoleysound/shorts'
channel_url = 'https://www.youtube.com/@The_Object'
output_path = 'D:\dataset\YT_Object\%(title)s.%(ext)s'
extractor = yt_dlp.YoutubeDL({'outtmpl': output_path})

info = extractor.extract_info(channel_url, download=True)

# 폴더 내 파일 이름 중 띄어쓰기 및 특수문자 _로 변경
folder_path = 'D:\dataset\JoshHarmon'
rename_files_in_folder(folder_path)
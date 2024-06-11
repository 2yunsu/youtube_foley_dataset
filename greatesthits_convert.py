import pandas as pd
import glob
import os
import re
import pdb
import numpy as np
import csv

# 각 행의 마지막 유효한 값을 반환하는 함수
def last_valid_value(row):
    # NaN 값을 제외한 마지막 값을 반환
    return row.dropna().iloc[-1] if not row.dropna().empty else np.nan

# 각 영상 파일에서 소리가 나는 시각을 추출하는 함수
def get_sound_frames(sound_times, fps=15, max_frames=90000):
    # 빈 문자열을 제거한 후 소리가 나는 시각 리스트를 생성
    sound_times = [time for time in sound_times if time]
    if not sound_times:
        return []

    # 소리가 나는 시각 리스트가 비어있지 않은 경우에만 프레임 리스트를 생성
    max_time = float(sound_times[-1])
    total_frames = int(max_time * fps) + 1

    # 너무 큰 값 제한 (예: 1시간 영상의 프레임 개수, 1시간 = 3600초, 3600초 * 15fps = 54000프레임)
    total_frames = min(total_frames, max_frames)
    sound_frames = [0] * total_frames

    for time in sound_times:
        frame = int(float(time) * fps)
        if frame < total_frames:
            sound_frames[frame] = 1
    return sound_frames

# 데이터프레임을 읽어와서 소리가 나는지 여부를 판단하는 함수
def process_dataframe(df, fps=15):
    output_data = []

    for index, row in df.iterrows():
        video_name = row[0]
        sound_times = row[1:].dropna().astype(str).tolist()  # NaN 값 제거 및 문자열로 변환
        sound_frames = get_sound_frames(sound_times, fps)
        output_data.append([video_name] + sound_frames)
    
    # 최대 길이에 맞추어 모든 행을 동일하게 맞춤
    max_length = max(len(row) for row in output_data)
    output_data = [row + [0] * (max_length - len(row)) for row in output_data]
    
    output_df = pd.DataFrame(output_data)
    return output_df

# 폴더 경로 설정 (사용자가 원하는 폴더 경로로 변경하세요)
folder_path = 'D:/dataset/Greatest_hits'  # 여기에 실제 폴더 경로를 입력하세요

# 모든 .txt 파일의 경로를 가져옵니다.
txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

# 첫 열의 데이터를 저장할 리스트를 초기화합니다.
first_column_data = []

# 각 .txt 파일을 순회하며 첫 열의 데이터를 읽어옵니다.
for file in txt_files:
    # 파일을 읽어서 첫 열의 데이터를 가져옵니다.
    with open(file, 'r', encoding='utf-8') as f:
        # 파일 이름을 포함할 리스트를 초기화합니다.
        file_first_column = [os.path.basename(file)]
        for line in f:
            # 각 줄을 쉼표로 분리하여 첫 번째 요소를 가져옵니다.
            first_col = line.split(',')[0].strip()
            # 숫자와 소수점만 남기고 다른 문자는 제거합니다.
            first_col_numeric = re.sub(r'[^0-9.]', '', first_col)
            # txt를 mp4로 변환.
            pdb.set_trace()
            file_first_column.append(first_col_numeric)
        # 데이터를 리스트에 추가합니다.
        first_column_data.append(file_first_column)

# 데이터프레임으로 변환합니다.
# df = pd.DataFrame(first_column_data)
df = pd.read_csv('output.csv')

# 파일 이름을 mp4로 변경
df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: x.replace('.txt', '.mp4'))

# 소리가 나는지 여부를 판단하여 새로운 데이터프레임 생성
output_df = process_dataframe(df)
output_file = "greatesthits_fps.csv"

# 새로운 데이터프레임을 CSV 파일로 저장
output_df.to_csv(output_file, index=False, header=False)

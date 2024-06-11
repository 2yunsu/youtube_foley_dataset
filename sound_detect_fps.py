from moviepy.editor import VideoFileClip
import numpy as np
from scipy.io import wavfile
import csv
import os

def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def detect_sound_intervals(audio_path, threshold, fps):
    sample_rate, data = wavfile.read(audio_path)
    if len(data.shape) > 1:  # 스테레오 오디오 처리
        data = data.mean(axis=1)
    total_duration = len(data) / sample_rate
    num_frames = int(total_duration * fps)
    frame_size = int(sample_rate / fps)
    
    sound_intervals = []
    for frame in range(num_frames):
        start_idx = frame * frame_size
        end_idx = start_idx + frame_size
        if np.max(np.abs(data[start_idx:end_idx])) > threshold:
            sound_intervals.append(1)
        else:
            sound_intervals.append(0)
    
    return sound_intervals

def get_video_files(directory):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']  # 필요한 비디오 파일 확장자 추가 가능
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in video_extensions]

def process_videos(directory, threshold, fps, output_csv):
    video_paths = get_video_files(directory)
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for video_path in video_paths:
            audio_path = os.path.splitext(video_path)[0] + '.wav'
            extract_audio(video_path, audio_path)
            
            sound_intervals = detect_sound_intervals(audio_path, threshold, fps)
            writer.writerow([os.path.basename(video_path)] + sound_intervals)
            
            # 임시 오디오 파일 삭제
            os.remove(audio_path)
            
            print(f'Processed {video_path}')

# 사용 예시
video_directory = 'D:\dataset\JoshHarmon'  # 비디오 파일들이 저장된 디렉토리
output_csv = 'sound_intervals_JoshHarmon.csv'
threshold = 10000
fps = 15  # 15fps 간격으로 소리 여부 확인

process_videos(video_directory, threshold, fps, output_csv)

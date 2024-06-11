from moviepy.editor import VideoFileClip
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import csv
import os

def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def plot_waveform(audio_path):
    sample_rate, data = wavfile.read(audio_path)
    if len(data.shape) > 1:  # 스테레오 오디오 처리
        data = data.mean(axis=1)
    times = np.arange(len(data)) / sample_rate

    plt.figure(figsize=(15, 5))
    plt.plot(times, data)
    plt.title('Audio waveform')
    plt.ylabel('Amplitude')
    plt.xlabel('Time [s]')
    plt.xlim(0, times[-1])
    plt.show()

def detect_sound_times(audio_path, threshold, interval):
    sample_rate, data = wavfile.read(audio_path)
    if len(data.shape) > 1:  # 스테레오 오디오 처리
        data = data.mean(axis=1)
    times = np.arange(len(data)) / sample_rate
    sound_times = times[np.abs(data) > threshold]

    # 기록 간격 조정
    filtered_times = []
    last_recorded_time = -interval  # 초기값을 음수로 설정하여 첫 값을 무조건 기록하도록 함
    for time in sound_times:
        if time - last_recorded_time >= interval:
            filtered_times.append(time)
            last_recorded_time = time

    return filtered_times

def get_video_files(directory):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']  # 필요한 비디오 파일 확장자 추가 가능
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in video_extensions]

def process_videos(directory, threshold, interval, output_csv):
    video_paths = get_video_files(directory)
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Filename', 'Sound Time'])
        
        for video_path in video_paths:
            audio_path = os.path.splitext(video_path)[0] + '.wav'
            extract_audio(video_path, audio_path)
            
            sound_times = detect_sound_times(audio_path, threshold, interval)
            for time in sound_times:
                writer.writerow([os.path.basename(video_path), time])
            
            # 임시 오디오 파일 삭제
            os.remove(audio_path)
            
            print(f'Processed {video_path}')

# 사용 예시
video_directory = './videos'  # 비디오 파일들이 저장된 디렉토리
output_csv = 'combined_sound_times.csv'
threshold = 20000
interval = 0.1  # 기록 간격을 0.1초로 설정

extract_audio('./videos/Recreating_Vintage_Cartoon_Sounds_(HARD).mp4', './videos/Recreating_Vintage_Cartoon_Sounds_(HARD).wav')
plot_waveform('./videos/Recreating_Vintage_Cartoon_Sounds_(HARD).wav')
process_videos(video_directory, threshold, interval, output_csv)

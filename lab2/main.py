import librosa
import numpy as np
import argparse

LOWER_BOUND = 0.1

BUTTON_FREQUENCIES = {
    (697, 1209): '1',
    (697, 1336): '2',
    (697, 1477): '3',
    (770, 1209): '4',
    (770, 1336): '5',
    (770, 1477): '6',
    (852, 1209): '7',
    (852, 1336): '8',
    (852, 1477): '9',
    (941, 1209): '*',
    (941, 1336): '0',
    (941, 1477): '#'
}

FREQ_TOLERANCE = 20

def find_closest_frequency(target_freq, freq_array, tolerance=FREQ_TOLERANCE):
    """
    在频谱中找到最接近目标频率的频率
    """
    closest_freq = None
    for freq in freq_array:
        if abs(freq - target_freq) <= tolerance:
            closest_freq = freq
            break
    return closest_freq

def key_tone_recognition(audio_array):
    audio_array = audio_array[0]

    result = []

    for i in range(0, len(audio_array), 750):
        audio_frame = audio_array[i:i + 750]

        # 计算当前帧的平均能量
        energy = np.sum(np.square(audio_frame)) / len(audio_frame)
        if energy < LOWER_BOUND:
            result.append("-1")
            continue

        # 进行 FFT 计算频谱
        fft_result = np.fft.rfft(audio_frame)
        fft_magnitude = np.abs(fft_result)
        fft_frequencies = np.fft.rfftfreq(len(audio_frame), d=1/48000)

        # 找到最突出的 2 个频率
        prominent_frequencies = fft_frequencies[np.argsort(fft_magnitude)[-2:]]

        for target_low, target_high in BUTTON_FREQUENCIES.keys():
            # 检查低频和高频是否在当前帧的频谱中
            if find_closest_frequency(target_low, prominent_frequencies) and \
               find_closest_frequency(target_high, prominent_frequencies):
                result.append(BUTTON_FREQUENCIES[(target_low, target_high)])
                break

    print(" ".join(result) + ' ')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_file', type=str, help='test file name', required=True)
    args = parser.parse_args()
    input_audio_array = librosa.load(args.audio_file, sr=48000, dtype=np.float32)  # audio file is numpy float array
    key_tone_recognition(input_audio_array)

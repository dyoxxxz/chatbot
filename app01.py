import torch
from TTS.api import TTS
import streamlit as st
from scipy.io.wavfile import write
import os

# TTS 모델 로드
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Streamlit 인터페이스 설정
st.title("TTS 음성 합성")
st.write("텍스트를 입력하고 음성으로 변환된 파일을 재생하고 다운로드할 수 있습니다.")

# 텍스트 입력
text = st.text_input("텍스트 입력:", "안녕하세요, 이 텍스트를 음성으로 변환합니다.")

# 음성 생성 버튼
if st.button("음성 생성"):
    # 음성 합성 및 임시 파일로 저장
    output_path = "output_audio.wav"
    tts.tts_to_file(
        text=text,
        speaker_wav="c://chat//new//input.wav",  # 화자의 음성 스타일을 위한 참조 음성 파일
        language="ko",
        file_path=output_path
    )

    # Streamlit에서 저장한 오디오 파일 재생
    st.audio(output_path, format="audio/wav")

    # 다운로드 버튼 추가
    with open(output_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        st.download_button(
            label="음성 다운로드",
            data=audio_bytes,
            file_name="output_audio.wav",
            mime="audio/wav"
        )

    # 다운로드 후 파일 삭제
    if os.path.exists(output_path):
        os.remove(output_path)

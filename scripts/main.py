import os
import sys
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip
from gtts import gTTS

def create_automated_video():
    print("🎬 영상 제작 엔진 가동 시작...")

    # 1. [보안] 환경변수에서 DB 데이터 가져오기 (외부 유출 방지 로직 적용)
    # 실제 DB 연결 대신 환경변수로 주입된 데이터를 사용하는 안전한 방식
    db_user = os.getenv('DB_USER', 'Unknown_User')
    target_text = "안녕하세요! GitHub Actions로 자동 생성된 비디오입니다."
    
    print(f"🔒 보안 모드: 사용자 {db_user} 권한으로 실행 중")

    # 2. [오디오] gTTS를 이용한 음성 합성 (Text-to-Speech)
    print("🔊 음성 합성 중 (TTS)...")
    tts = gTTS(text=target_text, lang='ko')
    audio_filename = "voice_overs.mp3"
    tts.save(audio_filename)
    
    # 생성된 오디오 길이 측정
    audio_clip = AudioFileClip(audio_filename)
    video_duration = audio_clip.duration + 2  # 오디오 길이 + 2초 여유

    # 3. [비디오] 배경 및 자막 생성 (ImageMagick 활용)
    print("🖼️ 화면 렌더링 중...")
    
    # 3-1. 배경 (파란색, HD 해상도)
    bg_clip = ColorClip(size=(1280, 720), color=(0, 50, 150), duration=video_duration)
    
    # 3-2. 자막 (한글 폰트 적용 필수: Ubuntu의 NanumGothic 사용)
    # 폰트가 없을 경우를 대비해 예외처리
    font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
    if not os.path.exists(font_path):
        font_path = 'DejaVuSans' # 리눅스 기본 폰트 (한글 깨질 수 있음)
        print("⚠️ 한글 폰트를 찾을 수 없어 기본 폰트를 사용합니다.")

    txt_clip = TextClip(target_text, fontsize=50, color='white', font=font_path, size=(1000, None), method='caption')
    txt_clip = txt_clip.set_position('center').set_duration(video_duration)

    # 4. [합성] 영상 + 자막 + 오디오 결합
    print("🔗 미디어 합성 중...")
    final_video = CompositeVideoClip([bg_clip, txt_clip])
    final_video = final_video.set_audio(audio_clip)

    # 5. [출력] 결과 파일 저장
    output_filename = "final_news_video.mp4"
    final_video.write_videofile(output_filename, fps=24, codec='libx264', audio_codec='aac')
    
    print(f"✅ 영상 제작 완료: {output_filename}")

if __name__ == "__main__":
    try:
        create_automated_video()
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)

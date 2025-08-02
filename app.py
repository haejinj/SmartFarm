import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from collections import Counter
import re

# 페이지 설정
st.set_page_config(layout='wide', page_title='생성형 AI를 활용한 융합 수업')

# 앱 타이틀
st.title('Ethic is good for us')

# 한글 폰트 설정
try:
    # NanumGothic 폰트 설정 (Streamlit Cloud에서 사용 가능한 폰트로 대체 가능)
    font_path = None  # Streamlit Cloud에서는 시스템 폰트를 사용
    font_manager.fontManager.addfont(font_path)  # 시스템 폰트 사용 시 필요 없음
    plt.rcParams['font.family'] = 'DejaVu Sans'  # 기본 폰트로 대체
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
except Exception as e:
    st.warning(f"폰트 설정 중 경고: {str(e)}. 기본 폰트를 사용합니다.")

# 사이드바 메뉴
st.sidebar.subheader('메뉴')
menu = st.sidebar.radio('기능을 선택하세요:', ['AI 윤리와 스마트팜', '식물 상태 분석', '텍스트 마이닝'])

# 화면 분할: (4,1) 비율로 컬럼 생성
col1, col2 = st.columns([4, 1])

# 모의 AI 모델 (교육용으로 단순화된 식물 건강 분석)
def analyze_plant_health(image):
    try:
        # 이미지를 배열로 변환
        img_array = np.array(image)
        
        # 색상 평균을 이용한 단순 분석
        avg_color = img_array.mean()
        if avg_color < 100:
            health = "건강하지 않음"
            suggestions = "식물이 충분한 햇빛을 받지 못하고 있을 수 있습니다. 빛을 더 쬐어주세요. 물 주기를 확인하세요."
        elif avg_color < 150:
            health = "보통"
            suggestions = "식물 상태가 보통입니다. 물과 영양분 공급을 꾸준히 유지하세요."
        else:
            health = "건강함"
            suggestions = "식물이 건강합니다! 현재 조건을 유지하세요."
        
        return health, suggestions
    except Exception as e:
        return "분석 오류", f"이미지 처리 중 오류가 발생했습니다: {str(e)}"

# 텍스트 마이닝 및 시각화 함수
def generate_word_frequency_chart(text):
    # 텍스트 전처리: 특수문자 제거
    words = re.findall(r'\b[\w가-힣]+\b', text)  # 한글 단어 포함
    
    # 단어 빈도 계산
    word_counts = Counter(words)
    
    # 상위 10개 단어 선택
    top_words = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    
    # 바 차트 생성
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(top_words.keys(), top_words.values(), color='#4CAF50')
    ax.set_xlabel('단어')
    ax.set_ylabel('빈도')
    ax.set_title('학생 생각에서 자주 등장한 단어')
    plt.xticks(rotation=45)
    return fig

# 메뉴에 따라 다른 콘텐츠 표시
if menu == 'AI 윤리와 스마트팜':
    # 왼쪽 콘텐츠 영역 - 유튜브 영상
    with col1:
        st.subheader("AI 윤리와 스마트팜 📺")
        youtube_url = st.text_input("유튜브 영상 URL을 입력하세요:", 
                                    "https://www.youtube.com/watch?v=JrWHG4mBdcQ")  # 예시 URL
        if youtube_url:
            try:
                st.video(youtube_url)
            except Exception as e:
                st.error(f"유튜브 영상 로드 중 오류: {str(e)}")
        st.caption("※ AI와 윤리, 스마트 기술이 어떻게 융합되는지 확인해 보세요.")
        
        # 학생 생각 기록 입력란
        st.subheader("너의 생각을 기록해 보세요 ✍️")
        student_thoughts = st.text_area("AI 윤리와 스마트팜에 대해 느낀 점이나 생각을 적어주세요:", height=100)
        if st.button("제출하기"):
            if student_thoughts.strip():
                try:
                    with open("data.txt", "a", encoding="utf-8") as f:
                        f.write(student_thoughts + "\n\n")
                    st.success("생각이 성공적으로 저장되었습니다!")
                except Exception as e:
                    st.error(f"저장 중 오류: {str(e)}")
            else:
                st.warning("내용을 입력해주세요.")

    # 오른쪽 팁 영역
    with col2:
        st.subheader("팁 💡")
        st.markdown("""
        - **AI 윤리란?**  
          인공지능이 인간과 사회에 해를 끼치지 않도록 사용하는 규칙과 태도입니다.

        - **스마트팜 예시**  
          온도 센서를 활용해 자동으로 물을 주는 시스템을 설계해보세요.

        - **생각해볼 점**  
          AI가 잘못 판단하면 어떤 일이 생길까요?  
          누가 책임을 져야 할까요?

        - [📝 나만의 AI 윤리 선언문 작성하기](https://gptonline.ai/ko/)
        """)

elif menu == '식물 상태 분석':
    with col1:
        st.subheader("식물 상태 분석 🌱")
        st.write("식물 이미지를 업로드하여 AI가 식물의 건강 상태를 분석합니다.")
        
        # 이미지 업로드
        uploaded_image = st.file_uploader("식물 이미지를 업로드하세요", type=['jpg', 'png', 'jpeg'])
        
        if uploaded_image is not None:
            try:
                # 업로드된 이미지 표시
                image = Image.open(uploaded_image)
                st.image(image, caption='업로드된 식물 이미지', width=300)
                
                # 식물 건강 분석
                health, suggestions = analyze_plant_health(image)
                
                # 결과 표시
                st.write(f"**식물 건강 상태**: {health}")
                st.write(f"**필요한 조건**: {suggestions}")
                
                # 학생들을 위한 토론 질문
                st.markdown("**생각해보기**: AI가 이 판단을 어떻게 내렸을까요? 색상, 크기, 모양 중 어떤 요소가 중요했을까요?")
            except Exception as e:
                st.error(f"이미지 처리 중 오류: {str(e)}")
            
    with col2:
        st.subheader("팁 💡")
        st.markdown("""
        - **식물 건강 분석이란?**  
          AI는 식물의 색상, 모양 등을 분석하여 건강 상태를 판단할 수 있습니다.

        - **스마트팜에서의 활용**  
          AI가 식물의 상태를 모니터링하여 물이나 영양분을 자동으로 공급하도록 설정할 수 있습니다.

        - **주의할 점**  
          AI의 판단이 항상 정확할까요? 잘못된 판단을 줄이려면 어떤 데이터를 더 수집해야 할까요?
        """)

elif menu == '텍스트 마이닝':
    with col1:
        st.subheader("학생들의 생각 분석 📊")
        st.write("학생들이 작성한 생각을 바탕으로 자주 등장하는 단어를 시각화합니다.")
        
        try:
            with open("data.txt", "r", encoding="utf-8") as f:
                text = f.read()
            if text.strip():
                # 바 차트 생성 및 표시
                fig = generate_word_frequency_chart(text)
                st.pyplot(fig)
                st.markdown("**분석 결과 해석**: 위 차트는 학생들의 생각에서 자주 등장하는 단어를 보여줍니다. 어떤 단어가 많이 나왔나요? 이는 어떤 생각을 반영할까요?")
            else:
                st.warning("data.txt 파일이 비어 있습니다. 먼저 생각을 제출해주세요.")
        except FileNotFoundError:
            st.error("data.txt 파일을 찾을 수 없습니다. 먼저 생각을 제출하여 파일을 생성하세요.")
        except Exception as e:
            st.error(f"텍스트 마이닝 중 오류: {str(e)}")

    with col2:
        st.subheader("팁 💡")
        st.markdown("""
        - **텍스트 마이닝이란?**  
          텍스트 데이터를 분석하여 중요한 단어나 패턴을 찾아내는 기술입니다.

        - **스마트팜과의 연관성**  
          텍스트 마이닝은 농업 데이터를 분석해 농부의 의견이나 문제를 파악하는 데 사용될 수 있습니다.

        - **생각해볼 점**  
          자주 등장하는 단어는 어떤 의미를 가질까요? AI가 이를 어떻게 활용할 수 있을까요?
        """)

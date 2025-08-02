import streamlit as st
from PIL import Image
import numpy as np

# 페이지 설정
st.set_page_config(layout='wide', page_title='생성형 AI를 활용한 융합 수업')

# 앱 타이틀
st.title('Ethic is good for us')

# 사이드바 메뉴
st.sidebar.subheader('메뉴')
menu = st.sidebar.radio('기능을 선택하세요:', ['AI 윤리와 스마트팜', '식물 상태 분석'])

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

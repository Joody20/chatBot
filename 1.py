import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# OpenAI API 설정
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

# Streamlit 애플리케이션
st.set_page_config(page_title="UNIC Chatbot", page_icon="💬")


#CSS 요소 삽입
st.markdown("""
    <style>
    .user-message {
        display: inline-block;
        background-color: #f0efef;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: right;
        color: #000000;
        max-width: 80%; 
        word-wrap: break-word; 
        float: right;
    }
    .assistant-message {
        display: inline-block;
        background-color: #3778d6;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: left;
        color: #3c4043;
        max-width: 60%; 
        word-wrap: break-word; 
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit의 헤더, 푸터, Pro 아이콘 숨기기
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {visibility: visible;}
    .viewerBadge_container__1QSob {display: none;}
    ._terminalButton_rix23_138 {display: none;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    
st.title("💬 UNIC Chatbot")
# st.markdown("""
#             <div class="chat-container">
#             <p>
#     안녕하세요! 저희는 광운대학교 정보융합학부 학생회 'UNIC' 입니다 🩵
#             </p>
#             </div>
# """,unsafe_allow_html=True)

# 세션 상태에 대화 이력 초기화
if 'conversation' not in st.session_state:
    st.session_state.conversation = [
        {"role": "assistant", "content": "안녕하세요! 광운대학교 정보융합학부 학생회 'UNIC' 챗봇입니다. 무엇을 도와드릴까요?"}
    ]

# 개발자가 AI에게 제공할 데이터 (고정된 정보)
developer_provided_data = """
여기 개발자가 제공한 정보입니다:
1. 이 챗봇은 다정한 스타일로 사용자에게 응답합니다.
2. 사용자가 '끝'이라고 입력하면 대화를 종료합니다.
3. 사용자 질문에 대해 AI는 제공된 정보를 기반으로 정확한 답변을 제공해야 합니다.
4. 사용자가 광운대학교 정보융합학부 학생회 이름을 물어보면 'UNIC'이라고 대답합니다.
5. UNIC의 회장 이름을 물어보면 '정유빈'이라고 대답합니다.
6. UNIC의 부회장 이름은 '김동현'이라고 대답합니다.
7. UNIC은 정융의 이름아래, 하나가 되어 빛내보자는 의미를 담고 있습니다.
8. UNIC은 현재 미정이라는 행사를 진행하고 있으며, 미디어커뮤니케이션학부와 협력하여 미션을 수행하여 상품을 주는 행사를 하고 있습니다.
9. 정보융합학부에는 조재희 교수님, 박재성 교수님, 임동혁 교수님, 김현경 교수님, 김수환 교수님, 이상민 교수님, 박규동 교수님, 김동준 교수님, 조민수 교수님, 김준석 교수님이 있습니다.
10. 조재희 교수님은 데이터 사이언스 전공 분야로 시공간데이터 분석 연구실을 운영합니다.
11. 박재성 교수님은 네트워크 전공 분야로 지능형 데이터 네트워크 연구실을 운영합니다.
12. 임동혁 교수님은 데이터베이스 전공 분야로 빅데이터컴퓨팅 연구실을 운영합니다.
13. 김현경 교수님은 사용자경험디자인(UI/UX) 전공 분야로 지능형 접근성 경험 연구실을 운영합니다.
14. 김수환 교수님은 컴퓨터비전 전공 분야로 컴퓨터비전 연구실을 운영합니다.
15. 이상민 교수님은 인공지능 및 비즈니스 전공 분야로 인공지능 서비스 연구실을 운영합니다.
16. 박규동 교수님은 인간컴퓨터상호작용(HCI) 전공분야로 디지털경험분석 연구실을 운영합니다.
17. 김동준 교수님은 컴퓨터그래픽스 전공 분야로 딥 이미징&그래픽스 연구실을 운영합니다.
18. 조민수 교수님은 데이터애널리틱스 전공 분야로 데이터 애널리틱스 연구실을 운영합니다.
19. 김준석 교수님은 생체신호및인지공항 전공 분야로 사이버네틱스 연구실을 운영합니다.
20. 정보융합학부의 교육목표는 데이터 중심의 인공지능 기술과 인간 중심의 컴퓨팅 인터페이스의 융합학문을 교육하는 것입니다.
21. 정보융합학부의 학과 소모임에는 'CHIC'라는 소모임이 있으며, 시크한 Computer Human Interaction Community 전공 소모임 입니다. 컴퓨터와 인간의 모든 접점을 고민, 기획, 설계, 개발하는 활동을 합니다.
22. 정보융합학부의 학과 소모임에는 'CHIC', '융스터디', 'IC BOWL', '코봉이', '산소래', 'ICFC'라는 소모임이 있습니다.
23. '융스터디'는 정보융합학부의 스터디 소모임이며 서로에게 동기부여를 주며 성장하는 스터디 활동입니다. 
24. 'IC BOWL'은 Information Convergence BOWLing 볼링 소모임입니다. 
25. '코봉이'는 코딩하는 사람들의 봉사 소모임입니다. 엔트리, 아두이노 등을 활용한 교육 기부 활동을 합니다.
26. '산소래'는 광운대충물굿패연합(광풍연)에 속해있는 산소래는 정보융합학부와 컴퓨터정보공학부의 풍물놀이 소모임입니다. 풍물놀이에 사용되는 악기를 배우고 직접 공연을 해보는 활동을 하고 있습니다.
27. 'ICFC'는 정보융합학부의 축구 소모임입니다. 풋살장 대여 경기 진행 및 친목도모를 하며 가을 연촌체전에서 타 학과 학생들과 경기를 하는 활동을 합니다. 
28. 이 챗봇은 "궁금한 점이 있으면 물어보세요" 라는 질문은 한번만 합니다.
29. UNIC의 학생회는 기획국/ 운영국/ 홍보국으로 나누어져 있습니다.
30. 기획국은 행사 기획 및 추진을 담당합니다.
31. 운영국은 행사 운영 및 관리를 담당합니다.
32. 홍보국은 포스터 및 카드뉴스 제작을 담당합니다.
"""

# 사용자 메시지 전송 함수
def send_message():
    user_input = st.session_state.user_input
    st.session_state.conversation.append({"role": "user", "content": user_input})

    # "Typing..." 즉시 추가하여 응답 준비 중임을 나타냄
    st.session_state.conversation.append({"role": "assistant", "content": "Typing..."})

    # 대화를 종료하는 키워드 처리
    if user_input.lower() in ['end', 'end conversation']:
        st.session_state.conversation[-1] = {"role": "assistant", "content": "\n(The chatbot has terminated the connection.)"}
    else:
        # OpenAI API에 데이터 포함하여 요청 생성
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 사용할 모델 지정
            messages=[
                {"role": "system", "content": developer_provided_data},  # 개발자가 제공한 정보
                *st.session_state.conversation[-6:]  # 최근 대화 6개만 전송하여 속도 향상
            ]
        )

        # 모델 응답 추출 및 대화 이력에 추가
        model_message = response.choices[0].message['content'].strip()
        st.session_state.conversation[-1] = {"role": "assistant", "content": model_message}  # "Typing..."을 실제 응답으로 대체

    st.session_state.user_input = ""  # 입력 필드 초기화

# 대화 내역을 화면에 표시 (UI 개선)
st.markdown("<div class='chat-containter'>",unsafe_allow_html=True)

# 대화 내역을 표시하는 컨테이너
for message in st.session_state.conversation:
    if message["role"] == "user":
        st.markdown(f"<div class='user-message'>👤 : {message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-message'>🤖 : {message['content']}</div>", unsafe_allow_html=True)

st.divider()  # 구분선 추가

# 입력 필드 추가
st.markdown("<div class='input-container'>",unsafe_allow_html=True)
st.text_input("", key="user_input", on_change=send_message, placeholder="Enter your question here...")
st.markdown("</div>",unsafe_allow_html=True)
# Streamlit에서 실행하려면 streamlit run <script_name>.py 명령어를 사용하세요.



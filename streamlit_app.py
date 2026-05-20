import streamlit as st
import random
import time

# 페이지 기본 설정
st.set_page_config(page_title="구구단 거꾸로 풀기", page_icon="🧮", layout="centered")

def init_state():
    """Streamlit 세션 상태 초기화"""
    defaults = {
        'game_state': 'select_time', # 'select_time' | 'playing'
        'time_limit': 5,
        'time_left': 5,
        'last_tick': time.time(),
        'target_product': 0,
        'correct_a': 0,
        'selected_num1': None,
        'selected_num2': None,
        'total_gold': 0, # 누적 골드
        'earned_gold': 0, # 이번 문제에서 획득한 골드
        'message': '',
        'message_type': '', # 'success' | 'error' | 'error_timeout' | 'hint' | ''
        'is_hint_mode': False,
        'start_time': 0.0,
        'time_taken': 0.0,
        'show_time_modal': False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def generate_question(limit=None):
    """새로운 문제를 출제하고 관련 상태를 초기화하는 함수"""
    if limit is not None:
        st.session_state.time_limit = limit
        
    while True:
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        new_prod = a * b
        if new_prod != st.session_state.target_product:
            break

    st.session_state.correct_a = a
    st.session_state.target_product = new_prod
    st.session_state.selected_num1 = None
    st.session_state.selected_num2 = None
    st.session_state.message = ''
    st.session_state.message_type = ''
    st.session_state.is_hint_mode = False
    st.session_state.show_time_modal = False
    st.session_state.start_time = time.time()
    st.session_state.time_left = st.session_state.time_limit
    st.session_state.last_tick = time.time()

def start_game(limit):
    """게임 시작 핸들러"""
    st.session_state.game_state = 'playing'
    st.session_state.total_gold = 0 # 게임 시작 시 골드도 초기화
    generate_question(limit)

def handle_number(num):
    """숫자 버튼 클릭 핸들러 (콜백 함수)"""
    if st.session_state.show_time_modal or st.session_state.message_type in ['error', 'error_timeout']:
        return

    if st.session_state.selected_num1 is None:
        st.session_state.selected_num1 = num
    elif st.session_state.selected_num2 is None:
        st.session_state.selected_num2 = num
        
        # 두 숫자가 모두 입력되면 정답 확인
        if st.session_state.selected_num1 * st.session_state.selected_num2 == st.session_state.target_product:
            st.session_state.time_taken = round(time.time() - st.session_state.start_time, 1)
            
            # 랜덤 골드 획득 (5 ~ 15)
            earned = random.randint(5, 15)
            st.session_state.earned_gold = earned
            st.session_state.total_gold += earned
            
            st.session_state.message = f'정답입니다! {earned} 골드 획득 🎉'
            st.session_state.message_type = 'success'
            st.session_state.show_time_modal = True
        else:
            st.session_state.message = '아쉽네요, 다시 생각해봐요! 🤔'
            st.session_state.message_type = 'error'

def handle_clear():
    """지우기 버튼 핸들러"""
    if st.session_state.selected_num1 is not None and st.session_state.selected_num2 is None and not st.session_state.is_hint_mode:
        st.session_state.selected_num1 = None

def go_home():
    """처음 화면으로 돌아가기"""
    st.session_state.game_state = 'select_time'

# ==========================================
# UI 렌더링 로직 시작
# ==========================================
init_state()

if st.session_state.game_state == 'select_time':
    st.title("구구단 거꾸로 풀기 🧮")
    st.subheader("제한 시간을 선택하고 게임을 시작하세요!")
    st.write("---")
    
    if st.button("⏱️ 5초 모드", use_container_width=True):
        start_game(5)
        st.rerun()
    st.write("")
    if st.button("⏱️ 10초 모드", use_container_width=True):
        start_game(10)
        st.rerun()

elif st.session_state.game_state == 'playing':
    # 상단 헤더 및 골드 영역
    col1, col2, col3 = st.columns([2, 1.5, 1])
    with col1:
        st.subheader("구구단 거꾸로 풀기")
    with col2:
        # 획득한 총 골드 표시
        st.write(f"### 🪙 {st.session_state.total_gold} G")
    with col3:
        st.button("🔄 처음으로", on_click=go_home, use_container_width=True)

    # ------------------------------------------
    # 1. 타이머 감소 로직
    # ------------------------------------------
    if not st.session_state.show_time_modal and not st.session_state.is_hint_mode and st.session_state.message_type not in ['error', 'error_timeout']:
        now = time.time()
        elapsed = now - st.session_state.last_tick
        
        if elapsed >= 1.0:
            st.session_state.time_left -= int(elapsed)
            st.session_state.last_tick = now

        # 시간 초과 시 상태 변경
        if st.session_state.time_left <= 0:
            st.session_state.time_left = 0
            st.session_state.message = '시간 초과! ⏰'
            st.session_state.message_type = 'error_timeout'
            st.rerun()

    # 타이머 프로그레스 바 표시
    progress_val = max(0.0, min(1.0, st.session_state.time_left / st.session_state.time_limit))
    st.progress(progress_val, text=f"남은 시간: {st.session_state.time_left}초")

    # ------------------------------------------
    # 2. 문제 표시 영역
    # ------------------------------------------
    st.write("---")
    st.header(f":blue[{st.session_state.target_product}] 은(는)?", anchor=False)
    st.write("몇 곱하기 몇일까요?")

    num1 = st.session_state.selected_num1
    num2 = st.session_state.selected_num2
    n1_str = str(num1) if num1 is not None else "?"
    n2_str = str(num2) if num2 is not None else "?"

    # 상태에 따른 색상 변경 로직
    if st.session_state.is_hint_mode:
        n1_disp = f":red[{n1_str}]"
        n2_disp = n2_str
    elif st.session_state.message_type in ['error', 'error_timeout']:
        n1_disp = f":red[{n1_str}]"
        n2_disp = f":red[{n2_str}]" if num2 is not None else "?"
    elif st.session_state.message_type == 'success':
        n1_disp = f":green[{n1_str}]"
        n2_disp = f":green[{n2_str}]"
    else:
        n1_disp = n1_str
        n2_disp = n2_str

    st.subheader(f"{n1_disp} × {n2_disp}", anchor=False)

    # ------------------------------------------
    # 3. 상태 메시지 출력
    # ------------------------------------------
    msg = st.session_state.message
    if msg:
        if st.session_state.message_type == 'success':
            st.success(msg)
        elif st.session_state.message_type in ['error', 'error_timeout']:
            st.error(msg)
        elif st.session_state.message_type == 'hint':
            st.warning(msg)
    else:
        st.write("") # 빈 공간 유지

    # ------------------------------------------
    # 4. 정답 모달 or 숫자 입력 패드
    # ------------------------------------------
    if st.session_state.show_time_modal:
        st.write("---")
        st.success("정답을 맞혔습니다! 🎉")
        st.info(f"⏱️ **{st.session_state.time_taken}**초 만에 풀었어요!\n\n🪙 **{st.session_state.earned_gold}** 골드를 획득했습니다!")
        st.button("다음 문제 넘어가기", on_click=generate_question, args=(st.session_state.time_limit,), use_container_width=True)
    else:
        st.write("---")
        # 1~9 숫자 패드 (3x3 그리드)
        for row in range(3):
            cols = st.columns(3)
            for col in range(3):
                num = row * 3 + col + 1
                cols[col].button(str(num), key=f"btn_{num}", on_click=handle_number, args=(num,), use_container_width=True)

        st.write("---")
        # 컨트롤 버튼
        c1, c2 = st.columns(2)
        c1.button("지우기", on_click=handle_clear, use_container_width=True, disabled=(st.session_state.selected_num1 is None or st.session_state.is_hint_mode))
        c2.button("건너뛰기", on_click=generate_question, args=(st.session_state.time_limit,), use_container_width=True)

    # ------------------------------------------
    # 5. 애니메이션 및 타이머 갱신을 위한 지연(Loop) 처리
    # ------------------------------------------
    if st.session_state.game_state == 'playing' and not st.session_state.show_time_modal:
        # 오답을 입력했을 때 1.2초 대기 후 힌트 모드로 전환
        if st.session_state.message_type == 'error':
            time.sleep(1.2)
            st.session_state.message = '첫 번째 숫자를 빨간색으로 알려줄게요!'
            st.session_state.message_type = 'hint'
            st.session_state.selected_num1 = st.session_state.correct_a
            st.session_state.selected_num2 = None
            st.session_state.is_hint_mode = True
            st.rerun()
            
        # 시간 초과일 때 1.5초 대기 후 힌트 모드로 전환
        elif st.session_state.message_type == 'error_timeout':
            time.sleep(1.5)
            st.session_state.message = '시간이 초과되어 첫 번째 숫자를 알려줄게요!'
            st.session_state.message_type = 'hint'
            st.session_state.selected_num1 = st.session_state.correct_a
            st.session_state.selected_num2 = None
            st.session_state.is_hint_mode = True
            st.rerun()
            
        # 평상시 타이머가 돌아가는 중이라면 1초마다 화면 갱신
        elif not st.session_state.is_hint_mode:
            time.sleep(1)
            st.rerun()

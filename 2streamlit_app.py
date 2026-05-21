import streamlit as st
import random
import time

# 페이지 기본 설정
st.set_page_config(page_title="구구단 거꾸로 풀기", page_icon="🧮", layout="centered")

def safe_rerun():
    """버전 호환성을 위한 rerun 함수"""
    if hasattr(st, 'rerun'):
        st.rerun()
    else:
        st.experimental_rerun()

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
        'gacha_count': 0, # 뽑기 횟수
        'inventory': [],  # 뽑은 동물 보관함
        'gacha_message': '', # 뽑기 상태 메시지
        'gacha_effect': None, # 알 뽑기 이펙트 (None, '일반', '희귀', '전설')
        'is_gacha_animating': False, # 애니메이션 재생 중 여부
        'pending_gacha_result': None, # 애니메이션 후 확정될 결과
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
    st.session_state.gacha_message = '' # 새로운 문제 출제 시 뽑기 메시지 초기화
    st.session_state.gacha_effect = None
    st.session_state.is_gacha_animating = False
    st.session_state.pending_gacha_result = None
    st.session_state.is_hint_mode = False
    st.session_state.show_time_modal = False
    st.session_state.start_time = time.time()
    st.session_state.time_left = st.session_state.time_limit
    st.session_state.last_tick = time.time()

def start_game(limit):
    """게임 시작 핸들러"""
    st.session_state.game_state = 'playing'
    st.session_state.total_gold = 0 # 게임 시작 시 골드 초기화
    st.session_state.gacha_count = 0 # 뽑기 횟수 초기화
    st.session_state.inventory = [] # 보관함 초기화
    st.session_state.gacha_message = ''
    st.session_state.gacha_effect = None
    st.session_state.is_gacha_animating = False
    generate_question(limit)

def handle_gacha():
    """신비의 알 뽑기 버튼 핸들러"""
    if st.session_state.get('is_gacha_animating', False):
        return

    # 골드 뽑기 상한 300G 적용
    cost = min((st.session_state.gacha_count + 1) * 100, 300)
    
    # 보관함 가득 참 예외 처리 (최대 5개)
    if len(st.session_state.inventory) >= 5:
        st.session_state.gacha_message = '보관함이 가득 찼습니다! (최대 5마리)'
        return
        
    # 골드 부족 예외 처리
    if st.session_state.total_gold < cost:
        st.session_state.gacha_message = f'골드가 부족합니다! (필요 골드: {cost}G)'
        return
        
    # 비용 차감 및 횟수 증가
    st.session_state.total_gold -= cost
    st.session_state.gacha_count += 1
    
    # 확률에 따른 등급 및 동물 결정 (일반 70%, 희귀 25%, 전설 5%)
    rarity = random.choices(['일반', '희귀', '전설'], weights=[70, 25, 5], k=1)[0]
    
    if rarity == '일반':
        animal = random.choice(['🐰', '🐶', '🐱', '🐹', '🐥'])
    elif rarity == '희귀':
        animal = random.choice(['🦊', '🐼', '🐯', '🦁', '🦉'])
    else: # 전설
        animal = random.choice(['🦄', '🐉', '🐲', '🦅', '🦈'])
        
    # 애니메이션 상태로 전환 (결과는 애니메이션 끝난 후 보관함에 추가)
    st.session_state.pending_gacha_result = {'rarity': rarity, 'animal': animal}
    st.session_state.is_gacha_animating = True
    st.session_state.gacha_message = ''
    st.session_state.gacha_effect = None

def handle_number(num):
    """숫자 버튼 클릭 핸들러 (콜백 함수)"""
    if st.session_state.get('is_gacha_animating', False):
        return
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
    if st.session_state.get('is_gacha_animating', False):
        return
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
        safe_rerun()
    st.write("")
    if st.button("⏱️ 10초 모드", use_container_width=True):
        start_game(10)
        safe_rerun()

elif st.session_state.game_state == 'playing':
    # 상단 헤더 및 뽑기 영역 배치 (2단 분리)
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.subheader("구구단 거꾸로 풀기")
        st.write(f"### 🪙 {st.session_state.total_gold} G")
        st.button("🔄 처음으로", on_click=go_home, use_container_width=True)
        
    with col2:
        if st.session_state.get('is_gacha_animating', False):
            # ------------------------------------------
            # 알 뽑기 애니메이션 연출 (강화 버전)
            # ------------------------------------------
            anim_ph = st.empty()
            
            # 1단계: 흔들
            anim_ph.markdown("""
            <style>
            @keyframes gentle-shake {
                0% { transform: rotate(0deg); }
                25% { transform: rotate(-10deg); }
                50% { transform: rotate(0deg); }
                75% { transform: rotate(10deg); }
                100% { transform: rotate(0deg); }
            }
            .egg-stage1 { display: inline-block; font-size: 60px; animation: gentle-shake 0.4s infinite; }
            </style>
            <div style='text-align: center;'><div class='egg-stage1'>🥚</div><br><span style='font-size:20px'>알이 흔들립니다...</span></div>
            """, unsafe_allow_html=True)
            time.sleep(0.7)
            
            # 2단계: 격렬한 흔들림
            anim_ph.markdown("""
            <style>
            @keyframes intense-shake {
                0% { transform: translate(1px, 1px) rotate(0deg); }
                10% { transform: translate(-1px, -2px) rotate(-15deg); }
                20% { transform: translate(-3px, 0px) rotate(15deg); }
                30% { transform: translate(3px, 2px) rotate(0deg); }
                40% { transform: translate(1px, -1px) rotate(15deg); }
                50% { transform: translate(-1px, 2px) rotate(-15deg); }
                60% { transform: translate(-3px, 1px) rotate(0deg); }
                70% { transform: translate(3px, 1px) rotate(-15deg); }
                80% { transform: translate(-1px, -1px) rotate(15deg); }
                90% { transform: translate(1px, 2px) rotate(0deg); }
                100% { transform: translate(1px, -2px) rotate(-15deg); }
            }
            .egg-stage2 { display: inline-block; font-size: 65px; animation: intense-shake 0.2s infinite; }
            </style>
            <div style='text-align: center;'><div class='egg-stage2'>🥚</div><br><span style='font-size:20px; font-weight:bold; color:orange'>격렬하게 흔들립니다!!</span></div>
            """, unsafe_allow_html=True)
            time.sleep(0.7)
            
            # 3단계: 쩌저적 금 가기
            anim_ph.markdown("""
            <style>
            @keyframes shudder {
                0% { transform: scale(1) rotate(0deg); filter: brightness(1); }
                50% { transform: scale(1.05) rotate(-5deg); filter: brightness(1.2); }
                100% { transform: scale(1) rotate(5deg); filter: brightness(1); }
            }
            .egg-stage3 { display: inline-block; font-size: 70px; animation: shudder 0.1s infinite; }
            </style>
            <div style='text-align: center;'><div class='egg-stage3'>🥚⚡</div><br><span style='font-size:24px; font-weight:bold; color:red'>쩌저적... 금 가기 시작했습니다!</span></div>
            """, unsafe_allow_html=True)
            time.sleep(0.8)
            
            # 4단계: 쾅! 펄스 효과
            anim_ph.markdown("""
            <style>
            @keyframes pulse-explode {
                0% { transform: scale(0.5); opacity: 0.8; filter: brightness(2); }
                50% { transform: scale(2.5); opacity: 1; filter: brightness(1.5); }
                100% { transform: scale(1.2); opacity: 0; filter: brightness(1); }
            }
            .egg-stage4 { display: inline-block; font-size: 100px; animation: pulse-explode 0.4s ease-out forwards; }
            </style>
            <div style='text-align: center;'><div class='egg-stage4'>💥</div><br><strong style='font-size:

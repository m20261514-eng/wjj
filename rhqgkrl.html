import React, { useState, useEffect, useCallback } from 'react';
import { Delete, ArrowRight, RotateCcw, Trophy } from 'lucide-react';

export default function App() {
  const [targetProduct, setTargetProduct] = useState(null);
  const [selectedNum1, setSelectedNum1] = useState(null);
  const [selectedNum2, setSelectedNum2] = useState(null);
  const [score, setScore] = useState(0);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'success' | 'error' | 'hint' | ''
  const [isChecking, setIsChecking] = useState(false);

  // 새 기능들을 위한 상태 추가
  const [correctA, setCorrectA] = useState(null);
  const [startTime, setStartTime] = useState(Date.now());
  const [timeTaken, setTimeTaken] = useState(null);
  const [showTimeModal, setShowTimeModal] = useState(false);
  const [isHintMode, setIsHintMode] = useState(false);

  // 시간 제한 기능을 위한 상태 추가
  const [gameState, setGameState] = useState('select_time'); // 'select_time' | 'playing'
  const [timeLimit, setTimeLimit] = useState(null);
  const [timeLeft, setTimeLeft] = useState(null);

  // 새로운 문제를 생성하는 함수 (이전 문제와 겹치지 않게 방지)
  const generateQuestion = useCallback((prevProduct = null, currentLimit = timeLimit) => {
    let a, b, newProduct;
    do {
      a = Math.floor(Math.random() * 8) + 2; // 2 ~ 9
      b = Math.floor(Math.random() * 8) + 2; // 2 ~ 9
      newProduct = a * b;
    } while (newProduct === prevProduct);

    setCorrectA(a); // 힌트용 첫 번째 정답 저장
    setTargetProduct(newProduct);
    setSelectedNum1(null);
    setSelectedNum2(null);
    setMessage('');
    setMessageType('');
    setIsChecking(false);
    setIsHintMode(false);
    setStartTime(Date.now()); // 문제 출제 시간 기록 시작
    setShowTimeModal(false);
    
    // 타이머 리셋
    if (currentLimit) {
      setTimeLeft(currentLimit);
    }
  }, [timeLimit]);

  // 게임 시작 핸들러
  const startGame = (limit) => {
    setTimeLimit(limit);
    setTimeLeft(limit);
    setGameState('playing');
    setScore(0);
    generateQuestion(null, limit);
  };

  // 타이머 카운트다운 및 시간 초과 처리
  useEffect(() => {
    if (gameState !== 'playing' || showTimeModal || isChecking || isHintMode) return;

    if (timeLeft > 0) {
      const timerId = setTimeout(() => setTimeLeft((prev) => prev - 1), 1000);
      return () => clearTimeout(timerId);
    } else if (timeLeft === 0 && !isHintMode) {
      // 시간 초과 시
      setIsChecking(true);
      setMessage('시간 초과! ⏰');
      setMessageType('error');
      
      setTimeout(() => {
        setSelectedNum1(correctA);
        setSelectedNum2(null);
        setMessage('시간이 초과되어 첫 번째 숫자를 알려줄게요!');
        setMessageType('hint');
        setIsHintMode(true);
        setIsChecking(false);
      }, 1500);
    }
  }, [gameState, timeLeft, showTimeModal, isChecking, isHintMode, correctA]);

  // 초기 문제 생성
  useEffect(() => {
    generateQuestion();
  }, [generateQuestion]);

  // 두 숫자가 모두 선택되었을 때 정답 확인
  useEffect(() => {
    if (selectedNum1 !== null && selectedNum2 !== null) {
      setIsChecking(true);
      
      if (selectedNum1 * selectedNum2 === targetProduct) {
        // 정답일 경우
        const end = Date.now();
        setTimeTaken(((end - startTime) / 1000).toFixed(1)); // 소요 시간 계산 (소수점 1자리)

        setMessage('정답입니다! 최고예요 🎉');
        setMessageType('success');
        setScore((s) => s + 10);
        setShowTimeModal(true); // 자동 넘김 대신 결과 창(모달) 띄우기
      } else {
        // 오답일 경우
        setMessage('아쉽네요, 다시 생각해봐요! 🤔');
        setMessageType('error');
        
        // 1.2초 후 빨간색 힌트 제공
        setTimeout(() => {
          setSelectedNum1(correctA); // 첫 번째 숫자를 정답으로 고정
          setSelectedNum2(null);     // 두 번째 칸만 비우기
          setMessage('첫 번째 숫자를 빨간색으로 알려줄게요!');
          setMessageType('hint');
          setIsHintMode(true);
          setIsChecking(false);
        }, 1200);
      }
    }
  }, [selectedNum1, selectedNum2, targetProduct, correctA, startTime]);

  // 숫자 패드 클릭 핸들러
  const handleNumberClick = (num) => {
    if (isChecking) return;
    
    if (selectedNum1 === null) {
      setSelectedNum1(num);
    } else if (selectedNum2 === null) {
      setSelectedNum2(num);
    }
  };

  // 하나 지우기
  const handleClear = () => {
    if (isChecking) return;
    // 힌트 모드일 때는 힌트로 주어진 첫 번째 숫자를 지울 수 없음
    if (selectedNum1 !== null && selectedNum2 === null && !isHintMode) {
      setSelectedNum1(null);
    }
  };

  // 빈칸 스타일 동적 생성 함수 (isFirstBox 파라미터 추가)
  const getBoxClass = (num, isFirstBox = false) => {
    const baseStyle = "w-16 h-16 sm:w-20 sm:h-20 flex items-center justify-center rounded-2xl border-4 text-4xl sm:text-5xl font-black transition-all duration-300";
    if (num === null) return `${baseStyle} border-dashed border-sky-200 text-sky-200 bg-white`;
    if (messageType === 'success') return `${baseStyle} border-green-400 bg-green-50 text-green-500 scale-110`;
    if (messageType === 'error') return `${baseStyle} border-red-400 bg-red-50 text-red-500 animate-pulse`;
    
    // 힌트 모드일 때 첫 번째 박스만 눈에 띄는 빨간색으로 표시
    if (isHintMode && isFirstBox) return `${baseStyle} border-red-400 bg-red-50 text-red-500 shadow-inner`;

    return `${baseStyle} border-sky-400 bg-sky-50 text-sky-500 shadow-inner`;
  };

  // 시작 화면 렌더링
  if (gameState === 'select_time') {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4 font-sans select-none">
        <div className="bg-white rounded-[2rem] shadow-xl p-8 w-full max-w-md border border-slate-100 text-center">
          <h1 className="text-3xl font-black text-slate-800 mb-4">구구단 거꾸로 풀기</h1>
          <p className="text-lg text-slate-500 mb-8">제한 시간을 선택하고 게임을 시작하세요!</p>
          
          <div className="flex flex-col gap-4">
            <button
              onClick={() => startGame(5)}
              className="w-full bg-rose-100 hover:bg-rose-200 text-rose-600 font-bold py-5 px-6 rounded-2xl text-xl transition-transform active:scale-95 shadow-sm border-2 border-rose-200 flex items-center justify-center gap-2"
            >
              <span className="text-2xl">⏱️</span> 5초 모드
            </button>
            <button
              onClick={() => startGame(10)}
              className="w-full bg-sky-100 hover:bg-sky-200 text-sky-600 font-bold py-5 px-6 rounded-2xl text-xl transition-transform active:scale-95 shadow-sm border-2 border-sky-200 flex items-center justify-center gap-2"
            >
              <span className="text-2xl">⏱️</span> 10초 모드
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4 font-sans select-none relative">
      <div className="bg-white rounded-[2rem] shadow-xl p-6 sm:p-8 w-full max-w-md border border-slate-100 relative overflow-hidden">
        
        {/* 정답 시 시간 표시 모달 (새창) */}
        {showTimeModal && (
          <div className="absolute inset-0 bg-white/95 backdrop-blur-sm flex flex-col items-center justify-center z-50 p-6 animate-in fade-in duration-300">
            <div className="text-6xl mb-4">⏱️</div>
            <h2 className="text-3xl font-black text-slate-800 mb-2">정답!</h2>
            <p className="text-xl text-slate-600 mb-8 text-center">
              <strong className="text-sky-600 text-3xl mx-2">{timeTaken}</strong>초 만에 풀었어요!
            </p>
            <button
              onClick={() => generateQuestion(targetProduct)}
              className="w-full max-w-[200px] bg-sky-500 hover:bg-sky-600 text-white font-bold py-4 px-6 rounded-2xl text-lg transition-transform active:scale-95 shadow-lg shadow-sky-200"
            >
              다음 문제
            </button>
          </div>
        )}

        {/* 상단 헤더 및 점수 */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-xl sm:text-2xl font-bold text-slate-800">구구단 거꾸로 풀기</h1>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 bg-amber-50 px-3 py-1.5 rounded-full text-amber-600 font-bold">
              <Trophy size={18} />
              <span>{score}점</span>
            </div>
            <button 
              onClick={() => setGameState('select_time')} 
              className="text-slate-400 hover:text-slate-600 transition-colors p-2 rounded-full hover:bg-slate-100"
              title="처음으로"
            >
              <RotateCcw size={20} />
            </button>
          </div>
        </div>

        {/* 타이머 바 */}
        <div className="w-full bg-slate-100 h-4 rounded-full mb-6 overflow-hidden relative border border-slate-200">
          <div 
            className={`h-full transition-all duration-1000 ease-linear ${timeLeft <= 3 ? 'bg-red-400' : 'bg-sky-400'}`}
            style={{ width: `${(timeLeft / timeLimit) * 100}%` }}
          />
          <div className="absolute inset-0 flex items-center justify-center text-xs font-black text-slate-700/70 mix-blend-color-burn">
            {timeLeft}초
          </div>
        </div>

        {/* 문제 표시 영역 */}
        <div className="bg-sky-50 rounded-3xl p-6 sm:p-8 mb-6 text-center border-2 border-sky-100">
          <div className="text-2xl font-bold text-slate-600 mb-1">
            <span className="text-5xl font-black text-sky-600 mr-1">{targetProduct}</span> 은(는)?
          </div>
          <div className="text-lg text-slate-500 mb-6">몇 곱하기 몇일까요?</div>
          
          {/* 수식 영역 (빈칸) */}
          <div className="flex items-center justify-center gap-2 sm:gap-4 mt-2">
            <div className="text-4xl sm:text-5xl font-black text-slate-300 mr-2 sm:mr-4"></div>
            <div className={getBoxClass(selectedNum1, true)}>
              {selectedNum1 !== null ? selectedNum1 : '?'}
            </div>
            <div className="text-3xl sm:text-4xl font-black text-slate-300">×</div>
            <div className={getBoxClass(selectedNum2, false)}>
              {selectedNum2 !== null ? selectedNum2 : '?'}
            </div>
          </div>
        </div>

        {/* 상태 메시지 */}
        <div className={`h-8 text-center font-bold text-lg mb-4 transition-all duration-300 ${
          messageType === 'success' ? 'text-green-500 animate-bounce' : 
          messageType === 'error' ? 'text-red-500' : 
          messageType === 'hint' ? 'text-orange-500 animate-bounce' : 'text-transparent'
        }`}>
          {message || 'placeholder'}
        </div>

        {/* 숫자 패드 (1~9) */}
        <div className="grid grid-cols-3 gap-3 mb-4">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
            <button
              key={num}
              onClick={() => handleNumberClick(num)}
              disabled={isChecking}
              className="bg-white border-2 border-slate-200 text-slate-700 text-2xl sm:text-3xl font-black py-4 sm:py-5 rounded-2xl shadow-sm hover:bg-sky-50 hover:border-sky-300 hover:text-sky-600 active:bg-sky-100 active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {num}
            </button>
          ))}
        </div>

        {/* 컨트롤 버튼 */}
        <div className="flex gap-3 mt-4">
          <button 
            onClick={handleClear} 
            disabled={isChecking || selectedNum1 === null} 
            className="flex-1 flex items-center justify-center gap-2 py-3 rounded-2xl bg-slate-100 text-slate-600 font-bold hover:bg-slate-200 active:bg-slate-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <Delete size={20} /> 지우기
          </button>
          <button 
            onClick={() => generateQuestion(targetProduct)} 
            disabled={isChecking} 
            className="flex-1 flex items-center justify-center gap-2 py-3 rounded-2xl bg-sky-100 text-sky-700 font-bold hover:bg-sky-200 active:bg-sky-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            건너뛰기 <ArrowRight size={20} />
          </button>
        </div>

      </div>
    </div>
  );
}

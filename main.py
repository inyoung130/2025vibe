import { useState, useEffect } from "react";

export default function ShihyangGame() {
  const [score, setScore] = useState(0);
  const [isHit, setIsHit] = useState(false);
  const [timer, setTimer] = useState(30);
  const [gameStarted, setGameStarted] = useState(false);

  useEffect(() => {
    let countdown;
    if (gameStarted && timer > 0) {
      countdown = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);
    } else if (timer === 0) {
      clearInterval(countdown);
    }
    return () => clearInterval(countdown);
  }, [gameStarted, timer]);

  const handleStart = () => {
    setScore(0);
    setTimer(30);
    setGameStarted(true);
  };

  const handleHit = () => {
    if (gameStarted && timer > 0) {
      setScore((prev) => prev + 1);
      setIsHit(true);
      setTimeout(() => setIsHit(false), 150);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-pink-100 text-center">
      <h1 className="text-4xl font-bold mb-4">💢 시향이 때리기 게임</h1>
      <p className="text-lg mb-2">30초 안에 얼마나 많이 때릴 수 있을까요?</p>

      {!gameStarted && (
        <button
          onClick={handleStart}
          className="px-6 py-2 bg-red-500 text-white rounded-lg text-lg hover:bg-red-600"
        >
          게임 시작
        </button>
      )}

      {gameStarted && (
        <>
          <div className="my-4 text-xl">⏱️ 남은 시간: {timer}s</div>
          <div className="my-4 text-xl">👊 점수: {score}</div>
          <img
            src={isHit ? "/shihyang_hit.png" : "/shihyang_normal.png"}
            alt="시향이"
            className={`w-60 h-60 cursor-pointer transition-transform duration-100 ${
              isHit ? "scale-95 rotate-2" : ""
            }`}
            onClick={handleHit}
          />
        </>
      )}

      {gameStarted && timer === 0 && (
        <div className="mt-6 text-2xl text-green-700 font-bold">
          🎉 게임 종료! 당신의 점수는 {score}점입니다.
        </div>
      )}
    </div>
  );
}

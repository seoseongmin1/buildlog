import { useEffect, useState } from "react";
import { getHealth } from "../api/health";

type ConnectionState = "checking" | "connected" | "disconnected";

export default function Home() {
  const [state, setState] = useState<ConnectionState>("checking");

  useEffect(() => {
    getHealth()
      .then(() => setState("connected"))
      .catch(() => setState("disconnected"));
  }, []);

  const label =
    state === "checking"
      ? "서버 연결 확인 중..."
      : state === "connected"
        ? "서버 연결됨"
        : "서버 연결 실패";

  return (
    <main>
      <h1>BuildLog</h1>
      <p>{label}</p>
    </main>
  );
}

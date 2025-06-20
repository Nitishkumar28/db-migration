import { useEffect, useRef, useState } from "react";

const WebsocketsTest = () => {
    const [logs, setLogs] = useState([]);
    const logContainerRef = useRef(null);

    // Connect to FastAPI WebSocket
    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8001/ws/logs");
        ws.onmessage = (event) => {
            setLogs((prev) => [...prev, event.data]);  // Append incoming log
        };
        ws.close = () => console.log("ws closed");
        ws.onerror = (error) => console.error("websockets", error)
        return () => ws.close();
    }, []);

    // Auto-scroll down when logs update
    useEffect(() => {
    if (logContainerRef.current) {
        logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
    }, [logs]);

    return (
        <div className="w-full h-full">
            <div
                ref={logContainerRef}
                className="bg-red-300 ">
                    {JSON.stringify(logs)}
                    {logs && logs.map((log, idx) => <p key={idx}>{log}</p>)}

            </div>
        </div>
    )
}

export default WebsocketsTest;
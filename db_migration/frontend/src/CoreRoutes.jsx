import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import ActionBlock from "./components/main/activeblock/ActionBlock";
import ExportBlock from "./components/main/activeblock/export/ExportBlock";
import ConnectionBlock from "./components/main/activeblock/connection/ConnectionBlock";
import SingleHistory from "./components/main/activeblock/history/SingleHistory";

const CoreRoutes = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Navigate to="/home/connections" />} />
                <Route path="/home" element={<Navigate to="/home/connections/" />} />
                <Route path="/home" element={<Home />}>
                    <Route index path="connections" element={<ConnectionBlock />}></Route>
                    <Route path="export" element={<ExportBlock />}></Route>
                    <Route path="history/:job_id" element={<SingleHistory />}></Route>
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

export default CoreRoutes;
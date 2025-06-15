import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import ActionBlock from "./components/main/activeblock/ActionBlock";
import ConnectionBlock from "./components/main/activeblock/ConnectionBlock";
import TransferBlock from "./components/main/activeblock/TransferBlock";
import RawDataBlock from "./components/main/activeblock/RawDataBlock";
import ValidationBlock from "./components/main/activeblock/ValidationBlock";

const CoreRoutes = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Navigate to="/home" />} />
                <Route path="/home" element={<Home />}>
                    <Route index path="" element={<ActionBlock />}></Route>
                    <Route index path="connections" element={<ConnectionBlock />}></Route>
                    <Route index path="transfer" element={<TransferBlock />}></Route>
                    <Route index path="validation" element={<ValidationBlock />}></Route> 
                    <Route index path="raw-data" element={<RawDataBlock />}></Route> 
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

export default CoreRoutes;
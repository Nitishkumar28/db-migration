import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import ExportBlock from "./components/main/activeblock/export/ExportBlock";
import ConnectionBlock from "./components/main/activeblock/connection/ConnectionBlock";
import SingleHistory from "./components/main/activeblock/history/SingleHistory";
import RegisterForm from "./pages/auth/register";
import LoginForm from "./pages/auth/Login";
import { PrivateRoute, PublicRoute } from "./AuthRoute";

const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="mb-4 text-3xl font-bold">404 - Page Not Found</h1>
      <p className="text-gray-600">Oops! The page you’re looking for doesn’t exist.</p>
    </div>
  );
};


const CoreRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<PublicRoute />}>
          <Route path="/login" element={<LoginForm />} />
          <Route path="/register" element={<RegisterForm />} />
        </Route>

        <Route path="/" element={<Navigate to="/home/connections" />} />

        <Route element={<PrivateRoute />}>
          <Route path="/home" element={<Home />}>
            <Route index element={<Navigate to="connections" />} />
            <Route path="connections" element={<ConnectionBlock />} />
            <Route path="export" element={<ExportBlock />} />
            <Route path="history/:job_id" element={<SingleHistory />} />
          </Route>
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
};

export default CoreRoutes;

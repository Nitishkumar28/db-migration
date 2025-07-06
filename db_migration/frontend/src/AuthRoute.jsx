import { Navigate, Outlet } from "react-router-dom";


const isAuthenticated = () =>
  window.localStorage.getItem("is_logged") === "true";

export const PrivateRoute = () => {
  return isAuthenticated() ? <Outlet /> : <Navigate to="/login" replace />;
};

export const PublicRoute = () => {
  return isAuthenticated() ? (
    <Navigate to="/home/connections" replace />
  ) : (
    <Outlet />
  );
};

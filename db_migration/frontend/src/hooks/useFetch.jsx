import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export function useFetch(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [trigger, setTrigger] = useState(0);
  const navigate = useNavigate();

  const refetch = useCallback(() => {
    setTrigger((prev) => prev + 1);
  }, []);

  useEffect(() => {
    if (!url) return;

    setLoading(true);
    fetch(url, {
      ...options,
      credentials: "include",
    })
      .then((res) => {
        if (res.status === 401) {
          localStorage.setItem("is_logged", "false");
          navigate("/login")
          throw new Error("Unauthorized");
        }
        if (!res.ok) {
          const backendMessage = json?.detail?.message || JSON.stringify(json.detail) || "Unknown error";
          throw new Error(backendMessage);
        }
        return res.json();
      })
      .then(setData)
      .catch(err => setError(err))
      .finally(() => setLoading(false));
  }, [url, trigger]);

  return { data, loading, error, refetch };
}

import { useState } from "react";
import { useNavigate } from "react-router-dom";

export function usePost(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const post = async (payload) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(url, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(payload),
      });
      
      if (res.status === 401) {
          localStorage.setItem("is_logged", "false");
          navigate("/login")
          throw new Error("Unauthorized");
        }
      const json = await res.json();

      if (!res.ok) {
        const backendMessage = json?.detail?.message || JSON.stringify(json.detail) || "Unknown error";
        throw new Error(backendMessage);
      }
      if (!res.ok) throw new Error("Failed to post data");
      
      setData(json);
      return json;

    } catch (err) {
      setError(err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { post, data, loading, error };
}

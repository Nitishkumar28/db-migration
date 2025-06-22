import { useState } from 'react';

export function useUpdate(url) {
  const [data, setData] = useState(null);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState(null);

  const update = async (payload) => {
    setUpdating(true);
    setError(null);
    try {
      const res = await fetch(url, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error('Failed to update data');
      const json = await res.json();
      setData(json);
    } catch (err) {
      setError(err);
    } finally {
      setUpdating(false);
    }
  };

  return { update, data, updating, error };
}

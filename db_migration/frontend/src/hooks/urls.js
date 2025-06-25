const BASE_URL = "http://localhost:8001/api";

// http://127.0.0.1:8000/api/export
// http://127.0.0.1:8000/api/migration-history-brief
// http://127.0.0.1:8000/api/migration-history/{job_id}
// http://127.0.0.1:8000/api/migration-history/create
// http://127.0.0.1:8000/api/migration-history/{job_id}
// http://127.0.0.1:8000/api/get-stats

export const healthCheck = () => `${BASE_URL}/`;
export const testAPI = () => `${BASE_URL}/test`;
export const patchTestAPI = (id) => `${BASE_URL}/test/${id}`;
export const checkConnectionAPI = () => `${BASE_URL}/check-connection`;
export const exportAPI = () => `${BASE_URL}/export`;
export const getStatsAPI = () => `${BASE_URL}/get-stats`;
export const validateAPI = () => `${BASE_URL}/validate`;
export const getHistoryBriefAPI = () => `${BASE_URL}/migration-history/brief/`;
export const getHistoryForJobidAPI = (job_id) =>
  `${BASE_URL}/migration-history/${job_id}`;
export const createHistoryJobAPI = () => `${BASE_URL}/migration-history/create`;

export const migrations = [
  {
    id: "96736865",
    name: "Photo",
    totalRows: 8920,
    imported: 8920,
    unimported: 0,
    messages: 0,
    throughput: "Unknown",
    source: "Mysql",
    target: "PostgreSql",
    date: "2011-08-03 02:26:32",
    status: "Completed"
  },
  {
    id: "9673465",
    name: "User",
    totalRows: 9920,
    imported: 8920,
    unimported: 0,
    messages: 0,
    throughput: "Unknown",
    source: "Mysql",
    target: "PostgreSql",
    date: "2011-08-03 02:26:32",
    status: "Idle"
  },
    {
    id: "92373465",
    name: "User",
    totalRows: 9920,
    imported: 8920,
    unimported: 0,
    messages: 0,
    throughput: "Unknown",
    source: "Mysql",
    target: "PostgreSql",
    date: "2011-08-03 02:26:32",
    status: "Idle"
  },
    {
    id: "9673465",
    name: "User",
    totalRows: 9920,
    imported: 8920,
    unimported: 0,
    messages: 0,
    throughput: "Unknown",
    source: "Mysql",
    target: "PostgreSql",
    date: "2011-08-03 02:26:32",
    status: "Idle"
  },
    {
    id: "9673465",
    name: "User",
    totalRows: 9920,
    imported: 8920,
    unimported: 0,
    messages: 0,
    throughput: "Unknown",
    source: "Mysql",
    target: "PostgreSql",
    date: "2011-08-03 02:26:32",
    status: "Idle"
  },
    {
    id: "9673465",
    name: "User",
    totalRows: 9920,
    imported: 8920,
    unimported: 0,
    messages: 0,
    throughput: "Unknown",
    source: "Mysql",
    target: "PostgreSql",
    date: "2011-08-03 02:26:32",
    status: "Idle"
  },
    {
    id: "9673465",
    name: "User",
    totalRows: 9920,
    imported: 8920,
    unimported: 0,
    messages: 0,
    throughput: "Unknown",
    source: "Mysql",
    target: "PostgreSql",
    date: "2011-08-03 02:26:32",
    status: "Idle"
  },
    {
    id: "1673465",
    name: "User",
    totalRows: 9920,
    imported: 8920,
    unimported: 0,
    messages: 0,
    throughput: "Unknown",
    source: "Mysql",
    target: "PostgreSql",
    date: "2011-08-03 02:26:32",
    status: "Idle"
  },
    {
    id: "53733465",
    name: "User",
    totalRows: 9920,
    imported: 8920,
    unimported: 0,
    messages: 0,
    throughput: "Unknown",
    source: "Mysql",
    target: "PostgreSql",
    date: "2011-08-03 02:26:32",
    status: "Idle"
  },
    {
    id: "9673465",
    name: "User",
    totalRows: 9920,
    imported: 8920,
    unimported: 0,
    messages: 0,
    throughput: "Unknown",
    source: "Mysql",
    target: "PostgreSql",
    date: "2011-08-03 02:26:32",
    status: "Idle"
  },

    {
    id: "7673465",
    name: "User",
    totalRows: 9920,
    imported: 8920,
    unimported: 0,
    messages: 0,
    throughput: "Unknown",
    source: "Mysql",
    target: "PostgreSql",
    date: "2011-08-03 02:26:32",
    status: "Idle"
  },
  {
    id: "67743465",
    name: "Image",
    totalRows: 8920,
    imported: 8920,
    unimported: 0,
    messages: 0,
    throughput: "Unknown",
    source: "Mysql",
    target: "PostgreSql",
    date: "2011-08-03 02:26:32",
    status: "Running"
  },
  {
    id: "16761365",
    name: "Image",
    totalRows: 8920,
    imported: 8920,
    unimported: 0,
    messages: 0,
    throughput: "Unknown",
    source: "Mysql",
    target: "PostgreSql",
    date: "2011-08-03 02:26:32",
    status: "Completed"
  },
  // add others similarly...
];

export const mockLogs = [
  { time: "09:58:21 AM", message: "✓ done" },
  { time: "09:58:21 AM", message: "✓ built in 2.97s" },
  { time: "09:58:22 AM", message: "==> Uploading build..." },
  { time: "09:58:24 AM", message: "==> Build uploaded in 2s" },
  { time: "09:58:24 AM", message: "==> Build successful 🎉" },
  { time: "09:58:25 AM", message: "==> Deploying..." },
  { time: "09:58:25 AM", message: "==> Installing dependencies..." },
  { time: "09:58:30 AM", message: "==> Dependencies installed" },
  { time: "09:58:31 AM", message: "==> Requesting Node version 20" },
  { time: "09:58:31 AM", message: "==> Using Node version 20.11.1 via env var" },
  { time: "09:58:31 AM", message: "==> Docs: https://render.com/docs/node-version" },
  { time: "09:58:32 AM", message: "==> Running 'node server.js'" },
  { time: "09:58:33 AM", message: "Listening on http://0.0.0.0:3000" },
  { time: "09:58:35 AM", message: "Your service is live 🎉" },
];


export const columns = [
  { key: "id", label: "ID" },
  { key: "name", label: "Name" },
  { key: "source_total_rows", label: "Source Total Rows" },
  { key: "target_total_rows", label: "Target Total Rows" },
  { key: "indexes_count", label: "Indexes" },
  { key: "primary_key", label: "Primary Keys" },
  { key: "foreign_key", label: "Foreign Keys" },
  { key: "status", label: "Status" },
  { key: "timestamp", label: "Created At" },
];

export const data = [
  {
    id: 1,
    name: "user",
    source_total_rows: "1045",
    target_total_rows: "1045",
    indexes_count: "3/3",
    primary_key: "1/1",
    foreign_key: "3/3",
    status: "Completed",
    timestamp: "2024-06-17"
  },
  {
    id: 2,
    name: "logs",
    source_total_rows: "3402",
    target_total_rows: "3402",
    indexes_count: "2/2",
    primary_key: "2/2",
    foreign_key: "1/1",
    status: "Running",
    timestamp: "2024-06-18"
  },
  {
    id: 3,
    name: "flex_pool_devices",
    source_total_rows: "4325",
    target_total_rows: "4325",
    indexes_count: "2/2",
    primary_key: "2/2",
    foreign_key: "4/4",
    status: "Idle",
    timestamp: "2024-06-19"
  }
];
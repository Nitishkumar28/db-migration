import { useState, useMemo } from "react";

const SummaryTable = ({ columns, data }) => {
  const [sortKey, setSortKey] = useState(null);
  const [sortAsc, setSortAsc] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  const handleSort = (key) => {
    if (sortKey === key) setSortAsc(!sortAsc);
    else {
      setSortKey(key);
      setSortAsc(true);
    }
  };

  const filteredData = useMemo(() => {
    if (!searchTerm) return data;
    return data.filter((row) =>
      columns.some((col) =>
        String(row[col.key] || "")
          .toLowerCase()
          .includes(searchTerm.toLowerCase())
      )
    );
  }, [data, searchTerm, columns]);

  const sortedData = useMemo(() => {
    const temp = [...filteredData];
    if (!sortKey) return temp;
    return temp.sort((a, b) => {
      const valA = a[sortKey];
      const valB = b[sortKey];
      if (typeof valA === "number") {
        return sortAsc ? valA - valB : valB - valA;
      }
      return sortAsc
        ? String(valA).localeCompare(String(valB))
        : String(valB).localeCompare(String(valA));
    });
  }, [filteredData, sortKey, sortAsc]);

  return (
    <div className="w-full h-full overflow-x-auto rounded-md border-0 border-sky-300 shadow-sm bg-white">
      {/* Search Bar */}
      <div className="p-2 flex justify-start items-center gap-10">
        <div className="w-[30%] flex justify-start items-center divide-x divide-sky-800 gap-3">
          <h2 className="w-full text-base font-semibold text-gray-700">Migration Summary</h2>
          <h2 className="w-full text-base font-light text-gray-700">Total rows: {data.length}</h2>
        </div>
        <input
          type="text"
          placeholder="Search..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-[70%] border border-sky-200 rounded px-2 py-1 text-sm outline-none focus:ring-1 focus:ring-sky-300"
        />
      </div>

      {/* Table or Empty Message */}
      {sortedData.length !== 0 ? (
        <table className="min-w-full divide-y divide-sky-200 text-sm">
          <thead className="bg-sky-100">
            <tr>
              {columns.map((col) => (
                <th
                  key={col.key}
                  onClick={() => handleSort(col.key)}
                  className="px-4 py-2 text-left font-medium text-gray-700 cursor-pointer hover:text-blue-600"
                >
                  {col.label}
                  {sortKey === col.key && (
                    <span className="ml-1">{sortAsc ? "↑" : "↓"}</span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {sortedData.map((row, idx) => (
              <tr key={idx} className="hover:bg-gray-50">
                {columns.map((col) => (
                  <td key={col.key} className="px-4 py-2 text-gray-700">
                    {row[col.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <span className="block p-4 text-gray-500 text-sm">No data to display</span>
      )}
    </div>
  );
};

export default SummaryTable;

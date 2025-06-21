import { useState } from "react";

const SummaryTable = ({ columns, data }) => {
  const [sortKey, setSortKey] = useState(null);
  const [sortAsc, setSortAsc] = useState(true);

  const handleSort = (key) => {
    if (sortKey === key) setSortAsc(!sortAsc);
    else {
      setSortKey(key);
      setSortAsc(true);
    }
  };

  const sortedData = [...data].sort((a, b) => {
    if (!sortKey) return 0;
    const valA = a[sortKey];
    const valB = b[sortKey];
    if (typeof valA === "number") {
      return sortAsc ? valA - valB : valB - valA;
    }
    return sortAsc
      ? String(valA).localeCompare(String(valB))
      : String(valB).localeCompare(String(valA));
  });

  return (
    <div className="w-full h-full overflow-x-auto rounded-md border border-cyan-300 shadow-sm bg-gray-0">
      {data.length !== 0 ? <table className="min-w-full divide-y divide-gray-200 bg-white text-[0.8rem]">
        <thead className="bg-cyan-100">
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
      </table> : <span className="p-2">No data to display</span>}
    </div>
  );
};

export default SummaryTable;

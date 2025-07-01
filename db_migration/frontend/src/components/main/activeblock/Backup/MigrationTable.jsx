import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const MigrationTableMain = () => {
  const { migrationName } = useParams();
  const navigate = useNavigate();

  const [selectedMigration, setSelectedMigration] = useState(() => {
    if (migrationName) {
      const found = migrations.find((m) => m.name === migrationName);
      return found ? [found] : null;
    }
    return null;
  });

  const handleBack = () => {
    setSelectedMigration(null);
    navigate("/home/history");
  };

  return (
    <div>
      <button
        onClick={handleBack}
        className="mb-4 px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded"
      >
        Back
      </button>
      <MigrationTable data={selectedMigration} />
    </div>
  );
};

const MigrationTable = ({ data }) => {
  //   const migration = data[0]; // Assume one selected migration
  //   const pageSize = 5; // Rows per page
  //   const [currentPage, setCurrentPage] = useState(1);

  //   const totalPages = Math.ceil(migration.tables.length / pageSize);

  //   const paginatedTables = migration.tables.slice(
  //     (currentPage - 1) * pageSize,
  //     currentPage * pageSize
  //   );
  return (
    <div className="overflow-x-auto mt-4">
      <table className="min-w-full bg-white border border-gray-200">
        <thead>
          <tr className="bg-gray-100 text-left">
            <th className="px-4 py-2">Migration</th>
            <th className="px-4 py-2">Total</th>
            <th className="px-4 py-2">Imported</th>
            <th className="px-4 py-2">Unimported</th>
            <th className="px-4 py-2">Messages</th>
            <th className="px-4 py-2">Throughput</th>
            <th className="px-4 py-2">Last Imported</th>
            <th className="px-4 py-2">Date</th>
            <th className="px-4 py-2"> Status</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, idx) => (
            <tr key={idx} className="border-t">
              <td className="px-4 py-2">{item.name}</td>
              <td className="px-4 py-2">{item.totalRows}</td>
              <td className="px-4 py-2">{item.imported}</td>
              <td className="px-4 py-2">{item.unimported}</td>
              <td className="px-4 py-2">{item.messages}</td>
              <td className="px-4 py-2">{item.throughput}</td>
              <td className="px-4 py-2">{item.lastImported}</td>
              <td className="px-4 py-2">{item.date}</td>
              <td className="px-4 py-2">{item.status}</td>
            </tr>
          ))}
        </tbody>
        {/* <tbody>
                {paginatedTables.map((table, index) => (
                    <tr key={index} className="border-t hover:bg-gray-50">
                    <td className="px-4 py-2">{table.tableName}</td>
                    <td className="px-4 py-2">{table.totalRows}</td>
                    <td className="px-4 py-2">{table.imported}</td>
                    <td className="px-4 py-2">{table.unimported}</td>
                    <td className="px-4 py-2">{table.messages}</td>
                    <td className="px-4 py-2">{table.throughput}</td>
                    <td className="px-4 py-2">{table.lastImported}</td>
                    </tr>
                ))}
</tbody> */}
      </table>
      {/* <div className="flex justify-end items-center gap-2 mt-4 text-sm">
  <button
    onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
    disabled={currentPage === 1}
    className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
  >
    Previous
  </button>
  <span>Page {currentPage} of {totalPages}</span>
  <button
    onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
    disabled={currentPage === totalPages}
    className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
  >
    Next
  </button>
</div> */}
    </div>
  );
};

export default MigrationTableMain;

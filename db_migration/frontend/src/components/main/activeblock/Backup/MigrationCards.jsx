const statusColors = {
  Idle: "bg-yellow-200 text-yellow-800",
  Completed: "bg-green-200 text-green-800",
  "in progress": "bg-blue-200 text-blue-800",
};

const MigrationCards = ({ migrations = [], selectedMigration, onSelect }) => {
  return (
    <div className="grid items-center justify-around grid-cols-3 gap-4 p-4 bg-red-300">
      {migrations.map((migration, index) => (
        <div
          key={index}
          className="relative w-[240px] bg-white border rounded-lg p-4 shadow cursor-pointer hover:shadow-md transition"
          onClick={() => onSelect(migration.name)}
        >
          <span className={`absolute top-2 right-2 text-xs px-2 py-1 rounded ${statusColors[migration.status]}`}>
            {migration.status}
          </span>
          <h3 className="mb-2 font-semibold">{migration.name}</h3>
          <p className="mb-1 text-gray-700">
            {migration.source} ➝ {migration.target}
          </p>
          <p className="mb-1 text-gray-600">Total Rows: {migration.totalRows}</p>
          <p className="mb-1 text-gray-600">Date: {migration.date}</p>

        </div>
      ))}
    </div>
  );
};

export default MigrationCards;
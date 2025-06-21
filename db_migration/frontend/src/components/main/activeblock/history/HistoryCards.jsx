import { getDBIcon } from "../../../../base/Icons";

const statusColors = {
  Idle: "bg-yellow-200 text-yellow-800",
  Completed: "bg-green-200 text-green-800",
  Running: "bg-blue-200 text-blue-800",
};

export const MigrationStatusTag = ({ status }) => {
  return (
    <span className={`text-xs px-2 py-1 rounded ${statusColors[status]}`}>
      {status}
    </span>
  );
};

const HistoryCards = ({ migrations = [], selectedMigration, onSelect }) => {
  return (
    <div className="flex flex-wrap items-center justify-between gap-5">
      {migrations.map((migration, index) => (
        <div
          key={index}
          className="relative h-40 w-[250px] flex flex-col justify-between items-center p-2 bg-white border border-cyan-300 rounded-lg shadow cursor-pointer hover:shadow-md transition"
          onClick={() => onSelect(migration.id)}
        >
          <div className="w-full flex justify-between items-center mb-2">
            <h3 className="leading-7 tracking-wider font-medium">
              Job ID: {migration.id}
            </h3>
            <MigrationStatusTag status={migration.status} />
          </div>

          <div className="w-full flex justify-evenly items-center gap-2">
            <div className="flex flex-col justify-start items-center">
              {getDBIcon(migration.source.toLowerCase(), 40)}
              <span className="text-xs">{migration.source}</span>
            </div>
            ➝
            <div className="flex flex-col justify-start items-center">
              {getDBIcon(migration.target.toLowerCase(), 40)}
              <span className="text-xs">{migration.target}</span>
            </div>
          </div>
          <span className="w-full text-xs leading-7 tracking-wide">
            Created: {migration.date}
          </span>
        </div>
      ))}
    </div>
  );
};

export default HistoryCards;

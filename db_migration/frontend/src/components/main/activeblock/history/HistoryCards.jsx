import { getDBIcon } from "../../../../base/Icons";
import { handle_datetime } from "../../../../base/utils";
import useDBStore from "../../../../store/dbStore";

const statusColors = {
  failed: "bg-red-200 text-red-800",
  completed: "bg-green-200 text-green-800",
  running: "bg-blue-200 text-blue-800",
};

export const MigrationStatusTag = ({ status }) => {
  return (
    <span className={`text-xs px-2 py-1 rounded ${statusColors[status]}`}>
      {status}
    </span>
  );
};

const HistoryCards = ({ onSelect }) => {
  const { historyCardsLocal:history_cards } = useDBStore();
  if (!history_cards) {
    return <div>Loading...</div>
  }
  return (
      <div className="grid grid-cols-4 gap-5">
        {history_cards.map((card, index) => (
          <div
            key={index}
            className="relative h-40 w-[250px] flex flex-col justify-between items-center p-2 bg-white border border-cyan-300 rounded-lg shadow cursor-pointer hover:shadow-md transition"
            onClick={() => onSelect(card.job_id)}
          >
            <div className="w-full flex justify-between items-center mb-2">
              <h3 className="leading-7 tracking-wider font-medium">
                Job ID: {card.job_id}
              </h3>
              <MigrationStatusTag status={card.status} />
            </div>

            <div className="w-full flex justify-evenly items-center gap-2">
              <div className="flex flex-col justify-start items-center">
                {getDBIcon(card.source_db_type.toLowerCase(), 45)}
                <span className="text-xs">{card.source_db_type}</span>
              </div>
              ➝
              <div className="flex flex-col justify-start items-center">
                {getDBIcon(card.target_db_type.toLowerCase(), 45)}
                <span className="text-xs">{card.target_db_type}</span>
              </div>
            </div>
            <span className="w-full text-xs leading-7 tracking-wide">
              Created: {handle_datetime(card.created_at)}
            </span>
          </div>
        ))}
      </div>
  );
};

export default HistoryCards;

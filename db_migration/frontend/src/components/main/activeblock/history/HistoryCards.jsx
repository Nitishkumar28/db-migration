import { useEffect, useState } from "react";
import { getDBIcon } from "../../../../base/Icons";
import { handle_datetime } from "../../../../base/utils";
import { getHistoryBriefAPI } from "../../../../hooks/urls";
import { useFetch } from "../../../../hooks/useFetch";
import useDBStore from "../../../../store/dbStore";

const statusColors = {
  failed: "bg-red-200 text-red-800",
  completed: "bg-green-200 text-green-800",
  running: "bg-blue-200 text-blue-800",
};

export const MigrationStatusTag = ({ status }) => (
  <span className={`text-xs px-2 py-1 rounded ${statusColors[status]}`}>
    {status}
  </span>
);

const HistoryCards = ({ onSelect }) => {
  const { data: history_cards, loading, error, refetch } = useFetch(getHistoryBriefAPI());
  const {
    historyCardsLocal,
    setHistoryCards,
    exportFinalStatus,
    activeJobID,
  } = useDBStore();
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    refetch();
    setHistoryCards(history_cards);
  }, [history_cards, setHistoryCards, exportFinalStatus]);

  const filteredCards = historyCardsLocal?.filter((card) => {
    const query = searchTerm.toLowerCase();
    return (
      card.job_id.toString().includes(query) ||
      card.source_db_name?.toLowerCase().includes(query) ||
      card.target_db_name?.toLowerCase().includes(query) ||
      card.status?.toLowerCase().includes(query)
    );
  });

  if (!historyCardsLocal) {
    return <div>Loading migration history...</div>;
  }

  return (
    <div className="w-full flex flex-col gap-4">
      <div className="w-full flex justify-between items-center">
        <h2 className="text-base font-semibold text-gray-700 mb-3">History</h2>
        <input
          type="text"
          placeholder="Search by job ID, DB name, or status"
          className="px-3 py-2 border outline-none focus:border-sky-600 border-gray-400 rounded-md text-sm w-full max-w-sm"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-4 gap-5">
        {filteredCards.map((card, index) => (
          <div
            key={index}
            className="relative h-40 w-[250px] flex flex-col justify-between items-center p-2 bg-white border border-cyan-300 rounded-lg shadow cursor-pointer hover:shadow-md transition"
            onClick={() => onSelect(card.job_id)}
          >
            <div className="w-full flex justify-between items-center mb-2">
              <h3 className="leading-7 tracking-wider font-medium">
                Job ID: {card.job_id}
              </h3>
              <MigrationStatusTag
                status={
                  activeJobID && card.job_id === activeJobID
                    ? exportFinalStatus
                    : card.status
                }
              />
            </div>

            <div className="w-full flex justify-evenly items-center gap-2">
              <div className="flex flex-col justify-start items-center">
                {getDBIcon(card.source_db_type.toLowerCase(), 45)}
                <span className="text-xs">{card.source_db_name}</span>
              </div>
              ➝
              <div className="flex flex-col justify-start items-center">
                {getDBIcon(card.target_db_type.toLowerCase(), 45)}
                <span className="text-xs">{card.target_db_name}</span>
              </div>
            </div>
            <span className="w-full text-xs leading-7 tracking-wide">
              Created: {handle_datetime(card.created_at)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HistoryCards;

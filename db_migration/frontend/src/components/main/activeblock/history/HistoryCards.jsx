import { useEffect, useState } from "react";
import { getDBIcon } from "../../../../base/Icons";
import { handle_datetime } from "../../../../base/utils";
import { getHistoryBriefAPI } from "../../../../hooks/urls";
import { useFetch } from "../../../../hooks/useFetch";
import useDBStoreHistory from "../../../../store/dbStoreHistory";

const statusColors = {
  failed: "bg-red-200 text-red-800",
  completed: "bg-green-200 text-green-800",
  "in progress": "bg-blue-200 text-blue-800",
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
  } = useDBStoreHistory();
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    if (history_cards && history_cards.length > 0) {
      setHistoryCards(history_cards);
    }
  }, [history_cards]);

  useEffect(() => {
    if (exportFinalStatus) {
      refetch();
    }
  }, [exportFinalStatus]);

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
    <div className="flex flex-col w-full gap-4">
      <div className="flex items-center justify-between w-full">
        <h2 className="mb-3 text-base font-semibold text-gray-700">History</h2>
        <input
          type="text"
          placeholder="Search by job ID, DB name, or status"
          className="w-full max-w-sm px-3 py-2 text-sm border border-gray-400 rounded-md outline-none focus:border-sky-600"
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
            <div className="flex items-center justify-between w-full mb-2">
              <h3 className="font-medium leading-7 tracking-wider">
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

            <div className="flex items-center w-full gap-2 justify-evenly">
              <div className="flex flex-col items-center justify-start">
                {getDBIcon(card.source_db_type.toLowerCase(), 45)}
                <span className="text-xs">{card.source_db_name}</span>
              </div>
              ➝
              <div className="flex flex-col items-center justify-start">
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

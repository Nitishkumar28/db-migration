import { useEffect, useState } from "react";
import { migrations } from "../../../data/Migration";
import { useParams, useNavigate } from "react-router-dom";
import useUIStore from "../../../../store/uistore";
import { getHistoryBriefAPI, testAPI } from "../../../../hooks/urls";
import { useFetch } from "../../../../hooks/useFetch";
import HistoryCards from "./HistoryCards";
import useDBStore from "../../../../store/dbStore";

const HistoryBlock = () => {
  const { migrationName } = useParams();
  const { setPipelineOption } = useUIStore();
  const { historyCardsLocal, setHistoryCards } = useDBStore();
  const navigate = useNavigate();
  const {data: history_cards, loading, error} = useFetch(getHistoryBriefAPI());

  useEffect(() => {
    setPipelineOption("history");
  }, []);

  useEffect(() => {
    if(history_cards) {
      setHistoryCards(history_cards)
    }
  }, [history_cards, loading])

  const [selectedMigration, setSelectedMigration] = useState(() => {
    if (migrationName) {
      const found = migrations.find((m) => m.name === migrationName);
      return found ? [found] : null;
    }
    return null;
  });

  const handleCardClick = (jobid) => {
    navigate(`/home/history/${jobid}`);
  };

  if(loading) {
    return <span>Loading...</span>
  }

  return (
    <div className="w-full h-[450px] overflow-y-scroll">
      <HistoryCards
        onSelect={handleCardClick}
      />
    </div>
  );
};

export default HistoryBlock;

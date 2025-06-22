import { useEffect, useState } from "react";
import { migrations } from "../../../data/Migration";
import { useParams, useNavigate } from "react-router-dom";
import useUIStore from "../../../../store/uistore";
import { getHistoryBriefAPI, testAPI } from "../../../../hooks/urls";
import { useFetch } from "../../../../hooks/useFetch";
import HistoryCards from "./HistoryCards";

const HistoryBlock = () => {
  const { migrationName } = useParams();
  const { setPipelineOption } = useUIStore();
  const navigate = useNavigate();
  const {data: history_cards, loading, error} = useFetch(getHistoryBriefAPI());

  useEffect(() => {
    setPipelineOption("history");
  }, []);

  const [selectedMigration, setSelectedMigration] = useState(() => {
    if (migrationName) {
      const found = migrations.find((m) => m.name === migrationName);
      return found ? [found] : null;
    }
    return null;
  });

  const handleCardClick = (jobid) => {
    // const selected = migrations.find((m) => m.name === name);
    // setSelectedMigration([selected]);
    navigate(`/home/history/${jobid}`);
  };

  if(!history_cards) {
    return <span>Loading...</span>
  }

  return (
    <div className="w-full h-[450px] overflow-y-scroll">
      <HistoryCards
        history_cards={history_cards}
        selectedMigration={selectedMigration}
        onSelect={handleCardClick}
      />
    </div>
  );
};

export default HistoryBlock;

import { useEffect, useState } from "react";
import { migrations } from "../../../data/Migration";
import { useParams, useNavigate } from "react-router-dom";
import HistoryCards from "./HistoryCards";
import useUIStore from "../../../../store/uistore";

const HistoryBlock = () => {
  const { migrationName } = useParams();
  const { setPipelineOption } = useUIStore();
  const navigate = useNavigate();

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
    const selected = migrations.find((m) => m.name === name);
    setSelectedMigration([selected]);
    navigate(`/home/history/${jobid}`);
  };

  return (
    <div className="w-full h-[450px] overflow-y-scroll">
      <HistoryCards
        migrations={migrations}
        selectedMigration={selectedMigration}
        onSelect={handleCardClick}
      />
    </div>
  );
};

export default HistoryBlock;

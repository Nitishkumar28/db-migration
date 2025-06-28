import React, { useState } from "react";
import { migrations } from "../../../data/Migration"; // Create this
import MigrationCards from "./MigrationCards";      // Create this
import MigrationTable from "./MigrationTable";      // Create this
import { header_sizes } from "../../../../base/Base";

import { useParams, useNavigate } from "react-router-dom";

const HistoryBlock = () => {

  const { migrationName } = useParams();
  const navigate = useNavigate();

  const [selectedMigration, setSelectedMigration] = useState(() => {
    if (migrationName) {
      const found = migrations.find((m) => m.name === migrationName);
      return found ? [found] : null;
    }
    return null;
  });

  const handleCardClick = (name) => {
    const selected = migrations.find(m => m.name === name);
    setSelectedMigration([selected]);
    navigate(`/home/history/${name}`);
  };

  return (
    <div className="w-full p-1 bg-purple-400">
        <MigrationCards migrations={migrations} selectedMigration={selectedMigration} onSelect={handleCardClick} />
    </div>
  );
};


export default HistoryBlock;
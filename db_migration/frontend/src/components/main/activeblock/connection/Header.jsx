import { useEffect } from "react";
import DropdownBlock from "../../../../base/DropdownBlock";
import useDBStore from "../../../../store/dbStore";

const ConnectionHeader = ({
  selectedSource,
  setSelectedSource,
  selectedTarget,
  setSelectedTarget,
}) => {
  const dbOptions = ["MySQL", "PostgreSQL", "Oracle"];
  const {selectSourceDetails, selectTargetDetails, setSelectedSourceDetails, setSelectedTargetDetails, connectionDetails} = useDBStore();
  
  useEffect(() => {
    if (selectedSource !== "") {
      const current = connectionDetails.find(conn => conn.db_type === selectedSource?.toLowerCase())
      setSelectedSourceDetails(current);
    } 
    
    if (selectedTarget !== "") {
      const current = connectionDetails.find(conn => conn.db_type === selectedTarget?.toLowerCase())
      console.log(`inside header.jsx ${selectedTarget} ${current}`)
      setSelectedTargetDetails(current)
    }
  }, [selectedSource, selectedTarget])

  return (
    <header className="w-full flex justify-center items-center gap-8 pb-3">
      <DropdownBlock
        text="source database"
        options={dbOptions.filter((option) => option !== selectedTarget)}
        selectedOption={selectedSource}
        setSelectedOption={setSelectedSource}
      />

      <DropdownBlock
        text="target database"
        options={dbOptions.filter((option) => option !== selectedSource)}
        selectedOption={selectedTarget}
        setSelectedOption={setSelectedTarget}
      />
    </header>
  );
};

export default ConnectionHeader;

import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useUIStore from "../../../../store/uistore";
import HistoryCards from "./HistoryCards";

const HistoryBlock = () => {
  const navigate = useNavigate();
  const { setPipelineOption } = useUIStore();

  useEffect(() => {
    setPipelineOption("history");
  }, []);

  const handleCardClick = (jobid) => {
    navigate(`/home/history/${jobid}`);
  };

  return (
    <div className="w-full h-[500px] overflow-y-scroll">
      <HistoryCards
        onSelect={handleCardClick}
      />
    </div>
  );
};

export default HistoryBlock;

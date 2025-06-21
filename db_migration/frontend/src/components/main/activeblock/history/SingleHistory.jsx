import { useNavigate, useParams } from "react-router-dom";
import ExportHeader from "../export/ExportHeader";
import SummaryTable from "../export/SummaryTable";
import { columns, data } from "../../../data/Migration";
import { LeftArrowIcon } from "../../../../base/Icons";
import useDBStore from "../../../../store/dbStore";

const GoBack = () => {
  const navigate = useNavigate();
  const handleBack = () => {
    // setSelectedMigration(null);
    navigate("/home/export");
  };
  return (
    <button
      onClick={handleBack}
      className="px-2 py-1 flex justify-center items-center-safe gap-2 border border-sky-300 hover:bg-sky-200 cursor-pointer rounded"
    >
      <LeftArrowIcon />
      <span className="">Back</span>
    </button>
  );
};

const SingleHistory = () => {
  const { jobid } = useParams();
  const { selectedSource, selectedTarget } = useDBStore();
  return (
    <div className="w-full h-full flex flex-col justify-start items-start p-2 gap-y-3">
      <GoBack />
      <ExportHeader isHistory={true} selectedSource={selectedSource} selectedTarget={selectedTarget}  />
      <SummaryTable columns={columns} data={data} />
    </div>
  );
};

export default SingleHistory;

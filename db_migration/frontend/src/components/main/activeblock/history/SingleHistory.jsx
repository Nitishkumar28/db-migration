import { useNavigate, useParams } from "react-router-dom";
import ExportHeader from "../export/ExportHeader";
import SummaryTable from "../export/SummaryTable";
import { full_history, history_columns } from "../../../data/Migration";
import { LeftArrowIcon } from "../../../../base/Icons";
import useDBStore from "../../../../store/dbStore";
import { useFetch } from "../../../../hooks/useFetch";
import { getHistoryForJobidAPI } from "../../../../hooks/urls";

const GoBack = () => {
  const navigate = useNavigate();
  const handleBack = () => {
    // setSelectedMigration(null);
    navigate("/home/export");
  };
  return (
    <button
      onClick={handleBack}
      className="px-2 py-0.5 flex justify-center items-center-safe gap-2 border border-sky-300 hover:bg-sky-200 cursor-pointer rounded"
    >
      <LeftArrowIcon />
      <span className="">Back</span>
    </button>
  );
};

const SingleHistory = () => {
  const { job_id } = useParams();
  const { selectedSource, selectedTarget } = useDBStore();
  const {data: history_for_jobid, loading, error} = useFetch(getHistoryForJobidAPI(job_id));
  // const history_for_jobid = full_history.find(curr => curr.job_id === job_id);    // full_history from API
  if(loading) {
    return <div>Loading...</div>
  }
  return (
    <div className="w-full h-full flex flex-col justify-start items-start p-2 gap-y-3">
      <div className="w-full flex justify-between items-center">
        <GoBack />
        <span className="font-semibold text-lg">Job ID: {job_id}</span>
      </div>
      <ExportHeader isHistory={true} selectedSource={selectedSource} selectedTarget={selectedTarget}  />
      {history_for_jobid.items && <SummaryTable columns={history_columns} data={history_for_jobid?.items} />}
      {/* {JSON.stringify(history_for_jobid.items)} */}
    </div>
  );
};

export default SingleHistory;

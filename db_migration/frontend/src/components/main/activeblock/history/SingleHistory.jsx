import { useNavigate, useParams } from "react-router-dom";
import ExportHeader from "../export/ExportHeader";
import SummaryTable from "../export/SummaryTable";
import { full_history, history_columns } from "../../../data/Migration";
import { LeftArrowIcon } from "../../../../base/Icons";
import useDBStore from "../../../../store/dbStore";
import { useFetch } from "../../../../hooks/useFetch";
import { getHistoryForJobidAPI } from "../../../../hooks/urls";
import { useEffect } from "react";

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
  const { selectedSource, selectedTarget, exportFinalStatus } = useDBStore();
  const {data: history_for_jobid, loading, error, refetch} = useFetch(job_id ? getHistoryForJobidAPI(job_id) : null);
  // const history_for_jobid = full_history.find(curr => curr.job_id === job_id);    // full_history from API
  useEffect(() => {
    console.log("REFECTCHED");
    if (exportFinalStatus && job_id) {
      refetch();
    }
  }, [exportFinalStatus, job_id])

    if (!job_id) {
    return <div className="text-red-600">Invalid Job ID</div>;
  }

  if (loading) {
    return <div className="text-gray-500">Loading history...</div>;
  }

  if (error || !history_for_jobid) {
    return <div className="text-red-500">Failed to load history.</div>;
  }

  return (
    <div className="w-full h-full flex flex-col justify-start items-start p-4 gap-y-4">
      <div className="w-full flex justify-between items-center">
        <GoBack />
        <span className="font-semibold text-lg">Job ID: {job_id}</span>
      </div>

      <ExportHeader
        isHistory={true}
        selectedSource={selectedSource}
        selectedTarget={selectedTarget}
      />
      {Array.isArray(history_for_jobid.items) && history_for_jobid.items.length > 0 ? (
        <SummaryTable columns={history_columns} data={history_for_jobid.items} />
      ) : (
        <div className="text-gray-500">No item history available.</div>
      )}
    </div>
  );
};

export default SingleHistory;

import { Icon } from "@iconify/react";
import { useEffect, useState } from "react";
import { BaseButton, LongArrowCustom } from "../../../../base/Base";
import { getDBIcon } from "../../../../base/Icons";
import useDBStore from "../../../../store/dbStore";
import { MigrationStatusTag } from "../history/HistoryCards";
import {
  createHistoryJobAPI,
  exportAPI,
  getHistoryForJobidAPI,
  getStatsAPI,
  validateAPI,
} from "../../../../hooks/urls";
import { usePost } from "../../../../hooks/usePost";
import { useFetch } from "../../../../hooks/useFetch";
import { useParams } from "react-router-dom";
import useDBStoreHistory from "../../../../store/dbStoreHistory";

const ExportCard = ({ text, children }) => {
  const activeConnection = useDBStore((state) =>
    text === "source" ? state.selectedSource : state.selectedTarget
  );

  return (
    <div className="w-[20%] h-full flex flex-col justify-start items-start -space-y-1.5">
      <span className="px-2 pb-0 ml-1 text-sm font-medium leading-7 tracking-wider bg-white border border-gray-300">
        {text}
      </span>
      <div className="flex flex-col items-center justify-center w-full h-full bg-white border border-gray-300 rounded">
        {activeConnection ? children : <span>No {text} is selected</span>}
      </div>
    </div>
  );
};

const ExportHeader = ({
  isHistory = false,
  selectedSource,
  selectedTarget,
}) => {
  const { job_id } = useParams();
  const {
    addNewHistoryCard,
    setExportFinalStatus,
    exportFinalStatus,
    setActiveJobID,
  } = useDBStoreHistory();
  const shouldFetch = !!job_id;
  const {
    data: history_for_jobid,
    loading,
    error,
  } = useFetch(shouldFetch ? getHistoryForJobidAPI(job_id) : null);
  // const exportFinalStatus = (shouldFetch && history_for_jobid) ? history_for_jobid.status  : "running";

  useEffect(() => {
    if (history_for_jobid) {
      console.log("status changed");
      const currStatus =
        shouldFetch && history_for_jobid ? history_for_jobid.status : "in progress";
      setExportFinalStatus(currStatus);
    }
  }, [shouldFetch, history_for_jobid]);

  const {
    post: initialPost,
    data: initialJobData,
    posting: isCreatingJob,
    error: initialJobError,
  } = usePost(createHistoryJobAPI());

  const {
    post: exportPost,
    data: exportJobData,
    posting: isExporting,
    error: exportJobError,
  } = usePost(exportAPI());

  const {
    post: statsPost,
    posting: isPostingStats,
    error: statsJobError,
  } = usePost(getStatsAPI());

  const {
    post: validatePost,
    data: validateJobData,
    posting: isValidating,
    error: validateJobError,
  } = usePost(validateAPI());

  const selectDetails = (type) =>
    useDBStore
      .getState()
      .connectionDetails.find(
        (conn) =>
          conn.db_type ===
          (type === "source" ? selectedSource : selectedTarget)?.toLowerCase()
      );

  const sourceDetails = selectDetails("source");
  const targetDetails = selectDetails("target");

  const isConnectionReady =
    sourceDetails?.status === "success" && targetDetails?.status === "success";

  const delay = (ms) => new Promise((res) => setTimeout(res, ms));

  const handleExport = async () => {
    try {
      const jobPayload = {
        source_db_type: sourceDetails.db_type,
        target_db_type: targetDetails.db_type,
        source_db_name: sourceDetails.db_name,
        target_db_name: targetDetails.db_name,
      };

      const job = await initialPost(jobPayload);

      // console.log(`Job result: ${JSON.stringify(job)}`);

      if (!job?.job_id) throw new Error("Job creation failed");

      addNewHistoryCard(job);

      await delay(5000);

      setActiveJobID(job?.job_id);

      // console.log(`Job card ${job?.job_id} added!`);

      const basePayload = {
        job_id: job.job_id,
        source: {
          host_name: sourceDetails.host_name,
          username: sourceDetails.username,
          password: sourceDetails.password,
          port: sourceDetails.port,
          db_name: sourceDetails.db_name,
          db_type: sourceDetails.db_type,
        },
        target: {
          host_name: targetDetails.host_name,
          username: targetDetails.username,
          password: targetDetails.password,
          port: targetDetails.port,
          db_name: targetDetails.db_name,
          db_type: targetDetails.db_type,
        },
      };

      // console.log(`export request body: ${JSON.stringify(basePayload)}`);
      
      const exportResult = await exportPost(basePayload);

      console.log(`Export API called: ${exportResult} ${exportJobError}`);

      await delay(5000);

      await statsPost({ ...basePayload, durations: exportResult?.durations });
      // console.log(`Stat API called!`);
      const validation = await validatePost(basePayload);
      // console.log(`Validation API called: ${validation}`);
      setExportFinalStatus(
        (exportJobError || statsJobError) ? "failed" : validation
      );
    } catch (error) {
      console.error("Export failed:", error);
      setExportFinalStatus("failed");
    }
  };

  const anyError =
    initialJobError || exportJobError || statsJobError || validateJobError;

  return (
    <div className="w-full h-[25%] flex justify-evenly items-center gap-4 p-2 bg-sky-50 rounded-lg">
      <ExportCard text="source">
        {getDBIcon(selectedSource?.toLowerCase(), 60)}
      </ExportCard>
      <span>
        <LongArrowCustom />
      </span>
      <ExportCard text="target">
        {getDBIcon(selectedTarget?.toLowerCase(), 60)}
      </ExportCard>

      {isHistory ? (
        <MigrationStatusTag status={anyError ? "failed" : exportFinalStatus} />
      ) : (
        <BaseButton
          text="export"
          onClick={handleExport}
          className={`font-medium py-1.5 px-2 bg-[#0492C2] text-white rounded-lg border ${
            !isConnectionReady && "pointer-events-none opacity-70"
          }`}
        >
          <Icon icon="mdi:database-export" width="24" height="24" />
        </BaseButton>
      )}
    </div>
  );
};

export default ExportHeader;

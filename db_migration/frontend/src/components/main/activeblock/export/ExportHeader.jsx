import { Icon } from "@iconify/react/dist/iconify.js";
import { BaseButton, LongArrowCustom } from "../../../../base/Base";
import { getDBIcon } from "../../../../base/Icons";
import useDBStore from "../../../../store/dbStore";
import { MigrationStatusTag } from "../history/HistoryCards";
import { createHistoryJobAPI, exportAPI, validateAPI } from "../../../../hooks/urls";
import { usePost } from "../../../../hooks/usePost";
import { useState } from "react";

const ExportCard = ({ text, children }) => {
  const activeConnection = useDBStore((state) => {
    if (text === "source") {
      return state.selectedSource;
    } else if (text === "target") {
      return state.selectedTarget;
    }
  });
  return (
    <div className="w-[20%] h-full flex flex-col justify-start items-start -space-y-1.5">
      <span className="text-sm font-medium border border-gray-300 bg-white pb-0 px-2 ml-1 leading-7 tracking-wider">
        {text}
      </span>
      <div className="w-full h-full flex flex-col justify-center items-center rounded border border-gray-300 bg-white">
        {activeConnection ? children : <span>No {text} is selected</span>}
      </div>
    </div>
  );
};

const ExportHeader = ({isHistory=false, selectedSource, selectedTarget}) => {
  // const { selectedSource, selectedTarget } = useDBStore();
  const [exportStatus, setExportStatus] = useState("running");
  const { addNewHistoryCard } = useDBStore();


  const {post: initial_post, data: initial_job_data, posting: initial_job_status, error: inital_job_error} = usePost(createHistoryJobAPI())
  const {post: export_post, data: export_job_data, posting: export_job_status, error: export_job_error} = usePost(exportAPI())
  const {post: stats_post, data: stats_job_data, posting: stats_job_status, error: stats_job_error} = usePost(exportAPI())
  const {post: validate_post, data: validate_job_data, posting: validate_job_status, error: validate_job_error} = usePost(validateAPI())

  const selectSourceDetails = useDBStore((state) => {
    const current = state.connectionDetails.find(
      (conn) => conn.db_type === selectedSource?.toLowerCase()
    );
    return current;
  });

  const selectTargetDetails = useDBStore((state) => {
    const current = state.connectionDetails.find(
      (conn) => conn.db_type === selectedTarget?.toLowerCase()
    );
    return current;
  });

  const isConnectionStatus =
    selectSourceDetails?.status === "success" &&
    selectTargetDetails?.status === "success";

  const handle_export = () => {
    // API call to migration-history/create
    const initial_job_request_body = {
      "source_db_type": selectSourceDetails.db_type,
      "target_db_type": selectTargetDetails.db_type,
      "source_db_name": selectSourceDetails.db_name,
      "target_db_name": selectTargetDetails.db_name,
    }
    initial_post(initial_job_request_body)

    if (inital_job_error) {
      return 
    }

    addNewHistoryCard(initial_job_data)

    // API call to export
    const request_body = {
      source: {
        db_type: selectSourceDetails.db_type,
        db_name: selectSourceDetails.db_name
      },
      target: {
        db_type: selectTargetDetails.db_type,
        db_name: selectTargetDetails.db_name
      }
    }
    const export_request_body = {
      "job_id": initial_job_data.job_id,
      ...request_body
    }
    export_post(export_request_body)

    if (export_job_error) {
      return 
    }

    // API call to stats
    const stats_request_body = {
      ...export_request_body,
      durations: export_job_data.durations
    }

    stats_post(stats_request_body)

    if (stats_job_error) {
      return 
    }

    // API call to validate
    validate_post(export_request_body)

    if (validate_job_error) {
      return 
    }

    console.log("export completed")
    setExportStatus(validate_job_data)
  }

  

  return (
    <div className="w-full h-[28%] flex justify-evenly items-center gap-4 p-2 bg-sky-50 rounded-lg">
      <ExportCard text="source">
        {getDBIcon(selectedSource?.toLowerCase(), 60)}
      </ExportCard>
      <span>
        <LongArrowCustom />
      </span>
      <ExportCard text="target">
        {getDBIcon(selectedTarget?.toLowerCase(), 60)}
      </ExportCard>
      {isHistory ? (inital_job_error || export_job_error || stats_job_error) ? <MigrationStatusTag status="failed" /> : <MigrationStatusTag status={exportStatus} /> : 
      <BaseButton
      text="export"
      onClick={() => handle_export()}
      className={`font-medium py-1.5 px-2 bg-[#0492C2] text-white rounded-lg border ${
          !isConnectionStatus && "pointer-events-none opacity-70"
          } `}
          >
        <Icon icon="mdi:database-export" width="24" height="24" />
      </BaseButton>
    }
    {initial_job_status}
    {export_job_status}
    {stats_job_status}
    {validate_job_status}
    </div>
  );
};

export default ExportHeader;

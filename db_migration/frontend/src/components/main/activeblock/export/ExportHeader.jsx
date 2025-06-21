import { Icon } from "@iconify/react/dist/iconify.js";
import { BaseButton, LongArrowCustom } from "../../../../base/Base";
import { getDBIcon } from "../../../../base/Icons";
import useDBStore from "../../../../store/dbStore";
import { MigrationStatusTag } from "../history/HistoryCards";

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
//   const { selectedSource, selectedTarget } = useDBStore();

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
      {isHistory ? <MigrationStatusTag status="completed" /> : 
      <BaseButton
      text="export"
      className={`font-medium py-1.5 px-2 bg-[#0492C2] text-white rounded-lg border ${
          !isConnectionStatus && "pointer-events-none opacity-70"
          } `}
          >
        <Icon icon="mdi:database-export" width="24" height="24" />
      </BaseButton>
    }
    </div>
  );
};

export default ExportHeader;

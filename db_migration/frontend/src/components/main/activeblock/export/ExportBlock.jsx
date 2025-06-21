import {
  BaseButton,
  header_sizes,
  LongArrowCustom,
} from "../../../../base/Base";
import {getDBIcon} from "../../../../base/Icons";

import { mockLogs, columns, data as tabledata } from "../../../data/Migration";
import MigrationLogs from "./MigrationLogs";

import { Icon } from "@iconify/react";
import useUIStore from "../../../../store/uistore";
import { useEffect } from "react";
import useDBStore from "../../../../store/dbStore";
import SummaryTable from "./SummaryTable";
import HistoryBlock from "../history/HistoryBlock";

const ExportCard = ({ text, children }) => {
    const activeConnection = useDBStore(state => {
    if(text === "source") {
      return state.selectedSource
    } else if (text === "target") {
      return state.selectedTarget
    }
  })
  return (
    <div className="w-[20%] h-full flex flex-col justify-start items-start -space-y-1.5">
        <span className="font-medium border border-gray-300 bg-white pb-1 px-2 ml-1 leading-7 tracking-wider">
          {text}
        </span>
        <div className="w-full p-1 h-full flex flex-col justify-center items-center rounded border border-gray-300 bg-white">
          { activeConnection ? children : <span>No {text} is selected</span> }
        </div>
    </div>
  );
};


const ExportBlock = () => {
    const { setPipelineOption } = useUIStore();
    const { selectedSource, selectedTarget } = useDBStore();

    useEffect(() => {
      setPipelineOption("export")
    }, [])

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

    const isConnectionStatus = selectSourceDetails?.status === "success" && selectTargetDetails?.status === "success";

  return (
    <div
      style={{ fontSize: header_sizes.normal }}
      className="w-full h-full"
    >
      <div className="w-full h-full flex flex-col justify-around items-center gap-4 py-2">
        <div className="w-full h-[25%] flex justify-evenly items-center gap-4 p-4 bg-gray-100 rounded-lg">
          <ExportCard text="source">
            {getDBIcon(selectedSource?.toLowerCase(), 60)}
          </ExportCard>
          <span>
            <LongArrowCustom />
          </span>
          <ExportCard text="target">
            {getDBIcon(selectedTarget?.toLowerCase(), 60)}
          </ExportCard>
          <BaseButton
            text="export"
            className={`font-medium py-1.5 px-2 bg-[#0492C2] text-white rounded-lg ${!isConnectionStatus && "pointer-events-none opacity-70"} `}
          >
            <Icon icon="mdi:database-export" width="24" height="24" />
          </BaseButton>
        </div>
        <div className="w-full h-full flex-1 border-t pt-4 px-2">
          <h2 className="text-base font-semibold text-gray-700 mb-3">History</h2>
          <HistoryBlock />
        </div>
      </div>
    </div>
  );
};

export default ExportBlock;

{/* <MigrationLogs logs={mockLogs} /> */}
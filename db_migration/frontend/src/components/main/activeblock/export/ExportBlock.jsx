import {header_sizes} from "../../../../base/Base";
import useUIStore from "../../../../store/uistore";
import { useEffect } from "react";
import useDBStore from "../../../../store/dbStore";
import HistoryBlock from "../history/HistoryBlock";
import ExportHeader from "./ExportHeader";




const ExportBlock = () => {
  const { selectedSource, selectedTarget } = useDBStore();
    const { setPipelineOption } = useUIStore();

    useEffect(() => {
      setPipelineOption("export")
    }, [])


  return (
    <div
      style={{ fontSize: header_sizes.normal }}
      className="w-full h-full"
    >
      <div className="w-full h-full flex flex-col justify-around items-center gap-4 py-2">
        <ExportHeader selectedSource={selectedSource} selectedTarget={selectedTarget}   />
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
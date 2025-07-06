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
      <div className="flex flex-col items-center justify-around w-full h-full gap-4 py-2">
        <ExportHeader selectedSource={selectedSource} selectedTarget={selectedTarget}   />
        <div className="flex-1 w-full h-full px-2 pt-4 border-t">
          <HistoryBlock />
        </div>
      </div>
    </div>
  );
};

export default ExportBlock;

{/* <MigrationLogs logs={mockLogs} /> */}
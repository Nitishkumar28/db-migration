import {
  BaseButton,
  header_sizes,
  LongArrowCustom,
} from "../../../../base/Base";
import {
  DarkIcon,
  ExportIcon,
  LightIcon,
  MySQLIcon,
  PostgresqlIcon,
  RightArrowIcon,
} from "../../../../base/Icons";

import { mockLogs } from "../../../data/Migration";
import { Icon } from "@iconify/react";
import useUIStore from "../../../../store/uistore";

const ToggleTheme = () => {
  const { mode, setMode } = useUIStore();

  return (
    <button
      onClick={() => setMode(mode === "light" ? "dark" : "light")}
      className="px-3 py-1 bg-gray-100 rounded hover:bg-gray-200"
    >
      {mode === "light" ? <LightIcon /> : <DarkIcon />}
    </button>
  );
};

const MigrationLogs = ({ logs = [] }) => {
  const mode = useUIStore((state) => state.mode);

  const bgColor = mode === "dark" ? "bg-slate-800" : "bg-slate-200";
  const textColor = mode === "dark" ? "text-gray-100" : "text-gray-800";
  const headerColor =
    mode === "dark" ? "bg-slate-700 text-white" : "bg-slate-400 text-slate-900";

  return (
    <div className="w-full h-[70%] rounded-lg border overflow-hidden">
      {/* Heading Bar */}
      <div
        className={`h-10 w-full flex items-center justify-between px-4 ${headerColor}`}
      >
        <div className="flex items-center gap-2">
          <Icon icon="mdi:database" className="text-xl" />
          <span className="font-light">Migration Logs</span>
        </div>
        <span className="text-xs italic tracking-wide">
          <ToggleTheme />
        </span>
      </div>

      {/* Logs Section */}
      <div
        className={`w-full flex flex-col justify-start items-start p-4 overflow-y-auto h-[calc(100%-2.5rem)] ${bgColor}`}
      >
        {logs.length === 0 ? (
          <span className={`text-sm italic ${textColor}`}>
            No logs available.
          </span>
        ) : (
          logs.map((log, idx) => (
            <span key={idx} className={`py-1 font-mono text-xs ${textColor}`}>
              {log.time} <i className="fa fa-info-circle text-blue-400" />{" "}
              {log.message}
            </span>
          ))
        )}
      </div>
    </div>
  );
};

const ExportCard = ({ text, children }) => {
  return (
    <div className="w-[30%] h-full flex flex-col justify-start items-start -space-y-1.5">
      <span className="font-semibold border border-gray-300 bg-gray-50 pb-1 px-2 ml-1 leading-7 tracking-wider">
        {text}
      </span>
      <div className="w-full p-2 h-full flex flex-col justify-center items-center rounded border border-gray-300 bg-gray-50">
        {children}
      </div>
    </div>
  );
};

const ExportBlock = () => {
  return (
    <div
      style={{ fontSize: header_sizes.normal }}
      className="w-full h-full px-[5%] py-[1%]"
    >
      <div className="w-full h-full flex flex-col justify-around items-center gap-2 py-2">
        <div className="w-full h-[30%] flex justify-around items-center gap-4 p-2">
          <ExportCard text="Source">
            <PostgresqlIcon size={80} />
          </ExportCard>
          <span>
            <LongArrowCustom />
          </span>
          <ExportCard text="Target">
            <MySQLIcon size={80} />
          </ExportCard>
          <BaseButton
            text="export"
            className="font-medium py-1.5 px-2 bg-[#0492C2] text-white rounded-lg"
          >
            <Icon icon="mdi:database-export" width="24" height="24" />
          </BaseButton>
        </div>

        <MigrationLogs logs={mockLogs} />
      </div>
    </div>
  );
};

export default ExportBlock;

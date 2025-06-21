import { Icon } from "@iconify/react/dist/iconify.js";
import useUIStore from "../../../../store/uistore";
import { DarkIcon, LightIcon } from "../../../../base/Icons";

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

export default MigrationLogs;
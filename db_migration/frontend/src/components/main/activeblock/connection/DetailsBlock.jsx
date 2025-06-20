import { BaseButton } from "../../../../base/Base";
import { themePalette } from "../../../../base/colorPalette";
import InputBar from "../../../../base/InputBar";
import WarningMessages from "../../../../base/main/activeblock/WarningMessages";
import useUIStore from "../../../../store/uistore";
import Legend from "../../../../base/main/activeblock/Legend";
import { checkConnectionURL } from "../../../../hooks/urls";
import useDBStore from "../../../../store/dbStore";
import { usePost } from "../../../../hooks/usePost";

const FirstColumn = ({ db_type }) => {
  return (
    <div className="w-[55%] h-full py-[2%] flex flex-col justify-start items-between gap-2">
      <InputBar
        title="Server Address"
        field="host_name"
        db_type={db_type}
      />
      <InputBar title="Username" field="username" db_type={db_type} />
      <InputBar title="Database Name" field="db_name" db_type={db_type} />
    </div>
  );
};

const SecondColumn = ({ db_type }) => {
  return (
    <div className="w-[25%] h-full py-[2%] flex flex-col justify-start items-between gap-2">
      <InputBar title="Port" size="small" field="port" db_type={db_type} />
      <InputBar
        title="Password"
        field="password"
        type="password"
        db_type={db_type}
      />
    </div>
  );
};

const DetailsBlock = ({ db_type, title }) => {
  const {
    post,
    data: result,
    loading: posting,
    error: postError,
  } = usePost(checkConnectionURL);

  const { connectionDetails, setConnectionDetails, updateConnectionDetails } = useDBStore();
  const activeTheme = useUIStore((state) => state.theme);

  const activeConnection = useDBStore((state) => {
    if (db_type === "source") {
      return state.selectedSource?.toLowerCase();
    } else if (db_type === "target") {
      return state.selectedTarget?.toLowerCase();
    }
  });

  const activeConnectionDetails = useDBStore((state) => {
    const current = state.connectionDetails.find(
      (conn) => conn.db_type === activeConnection?.toLowerCase()
    );
    return current;
  });

  const handleReset = () => {
    const updatedConnections = connectionDetails.map((conn) => {
      if (conn.db_type === activeConnection.toLowerCase()) {
        return {
          ...conn,
          host_name: "",
          username: "",
          password: "",
          db_name: "",
          status: "idle",
        };
      }
      return conn;
    });

    setConnectionDetails(updatedConnections);
  };

  const handlePost = async () => {
    console.log(activeConnectionDetails, activeConnection);

    if (!activeConnectionDetails)
      return console.warn("No matching connection found for", db_type);

    try {
      await post({...activeConnectionDetails, "db_type": activeConnection.toLowerCase()});
      updateConnectionDetails(activeConnection, "status", "success");
    } catch (err) {
      console.error("Post failed:", err.message);
      updateConnectionDetails(activeConnection, "status", "failed");
    }
  };

  return (
    <div
      style={{ borderColor: themePalette[activeTheme].borderPrimary }}
      className={`relative border rounded-lg shadow-md w-[90%] h-[60%] flex flex-col justify-center items-center gap-1 py-3`}
    >
      <Legend title={title} />
      <div
        className={`w-full h-fit flex justify-around items-center gap-4 px-[2%]`}
      >
        <FirstColumn db_type={db_type} />
        <SecondColumn db_type={db_type} />
        <WarningMessages />
      </div>
      <div
        className={`flex justify-center items-center gap-4 ${
          !activeConnection && "cursor-default opacity-50 pointer-events-none"
        }`}
      >
        <BaseButton
          onClick={() => handlePost()}
          text={posting ? "checking..." : "check connection"}
          styles={`bg-sky-50`}
        />
        <span
          onClick={() => handleReset()}
          className="underline underline-offset-2 text-sky-800 text-xs font-extralight cursor-pointer capitalize"
        >
          reset details
        </span>
      </div>
    </div>
  );
};

export default DetailsBlock;

// Modernized DetailsBlock.jsx
import { BaseButton } from "../../../../base/Base";
import { themePalette } from "../../../../base/colorPalette";
import InputBar from "../../../../base/InputBar";
import WarningMessages from "../../../../base/main/activeblock/WarningMessages";
import useUIStore from "../../../../store/uistore";
import Legend from "../../../../base/main/activeblock/Legend";
import { checkConnectionURL } from "../../../../hooks/urls";
import useDBStore from "../../../../store/dbStore";
import { usePost } from "../../../../hooks/usePost";

const Row = ({ db_type, fields }) => (
  <div className="flex gap-6 w-full h-full px-[2%]">
    {fields.map(({ title, field, type = "text" }) => (
      <InputBar
        key={field}
        title={title}
        field={field}
        db_type={db_type}
        type={type}
      />
    ))}
  </div>
);

const DetailsBlock = ({ db_type, title }) => {
  const { post, data: result, loading: posting } = usePost(checkConnectionURL);
  const {
    connectionDetails,
    setConnectionDetails,
    updateConnectionDetails,
    selectedSource,
    selectedTarget,
  } = useDBStore();
  const activeTheme = useUIStore((state) => state.theme);

  const activeConnection =
    db_type === "source" ? selectedSource?.toLowerCase() : selectedTarget?.toLowerCase();

  const activeConnectionDetails = connectionDetails.find(
    (conn) => conn.db_type === activeConnection
  );

  const handleReset = () => {
    const updatedConnections = connectionDetails.map((conn) =>
      conn.db_type === activeConnection
        ? {
            ...conn,
            host_name: "",
            username: "",
            password: "",
            db_name: "",
            status: "idle",
          }
        : conn
    );
    setConnectionDetails(updatedConnections);
  };

  const handlePost = async () => {
    if (!activeConnectionDetails) return;
    try {
      setTimeout(() => {}, [3000])
      await post({ ...activeConnectionDetails, db_type: activeConnection });
      updateConnectionDetails(
        activeConnection,
        "status",
        result?.results ? "success" : "failed"
      );
    } catch {
      updateConnectionDetails(activeConnection, "status", "failed");
    }
  };

  return (
    <div
      style={{ borderColor: themePalette[activeTheme].borderPrimary }}
      // [#E1F6FC]
      className="relative w-[70%] max-w-6xl h-auto bg-gradient-to-tr from-sky-50 via-white to-sky-50  border border-sky-200 rounded-xl shadow-lg py-7 px-6 bg-white flex flex-col gap-4"
    >
      <Legend title={title} />
      <div className="w-full flex flex-col justify-between gap-3">
        <Row
          db_type={db_type}
          fields={[
            { title: "Server Address", field: "host_name" },
            { title: "Port", field: "port" },
          ]}
          />
        <Row
          db_type={db_type}
          fields={[
            { title: "Username", field: "username" },
            { title: "Password", field: "password", type: "password" },
          ]}
          />
        <Row
          db_type={db_type}
          fields={[
            { title: "Database Name", field: "db_name" },
            { title: "", field: "" },
          ]}
        />
        {/* <WarningMessages /> */}
      </div>

      <div className={`flex justify-center items-center gap-4 ${!activeConnection && "opacity-50 pointer-events-none"}`}>
        <BaseButton
          onClick={handlePost}
          text={posting ? "Checking..." : "Check Connection"}
          className="border-none rounded-lg px-2 bg-[#D5E8EC] hover:opacity-80 text-[#03729A]"
        />
        <button
          onClick={handleReset}
          className="text-xs text-sky-700 underline underline-offset-2 hover:text-blue-900"
        >
          Reset Details
        </button>
      </div>
    </div>
  );
};

export default DetailsBlock;

import useDBStore from "../store/dbStore";
import useUIStore from "../store/uistore";
import { header_sizes, TextHolder } from "./Base";
import { themePalette } from "./colorPalette";

const InputBar = ({ title, db_type, field, type = "text" }) => {
  const activeTheme = useUIStore((state) => state.theme);
  const { updateConnectionDetails } = useDBStore();

  const activeConnection = useDBStore((state) => {
    if (db_type === "source") {
      return state.selectedSource;
    } else if (db_type === "target") {
      return state.selectedTarget;
    }
  });

  // const updateConnectionDetails = useDBStore((state) => {
  //   if(db_type === "source") {
  //     return state.updateSourceDetails
  //   } else if (db_type === "target") {
  //     return state.updateTargetDetails
  //   }
  // });

  const activeConnectionDetails = useDBStore((state) => {
    const current = state.connectionDetails.find(
      (conn) => conn.db_type === activeConnection?.toLowerCase()
    );
    return current;
    /*
    if(db_type === "source") {
      const current = state.connectionDetails.find(conn => conn.db_type === selectedSource?.toLowerCase())
      return current;
    } else if(db_type === "target") {
      const current = state.connectionDetails.find(conn => conn.db_type === selectedTarget?.toLowerCase())
      return current;
    }
      */
  });

  // const activeConnectionDetails = useDBStore(state => {
  //   if(db_type === "source") {
  //     return state.selectSourceDetails
  //   } else if (db_type === "target") {
  //     return state.selectTargetDetails
  //   }
  // })

  const value = activeConnectionDetails?.[field] || "";

  const handleChange = (e) => {
    updateConnectionDetails(
      activeConnection?.toLowerCase(),
      field,
      e.target.value
    );
  };

  return (
    <div className={`w-full flex flex-col justify-start items-start`}>
      {title && (
        <TextHolder
          text={title}
          size="small"
          weight="normal"
          className="select-none"
        />
      )}
      {title && (
        <input
          style={{ fontSize: header_sizes.small }}
          type={type}
          value={value}
          onChange={(e) => handleChange(e)}
          className={`w-full outline-none border rounded border-gray-300 px-2 py-1 focus:border-gray-500 ${
            !activeConnection &&
            "cursor-default bg-gray-100 pointer-events-none"
          }`}
        />
      )}
    </div>
  );
};

export default InputBar;

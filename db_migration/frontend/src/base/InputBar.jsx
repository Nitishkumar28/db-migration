import useDBStore from "../store/dbStore";
import useUIStore from "../store/uistore";
import { header_sizes, TextHolder } from "./Base";
import { themePalette } from "./colorPalette";

const InputBar = ({ title, db_type, field, type = "text" }) => {
  const activeTheme = useUIStore((state) => state.theme);

  const activeConnection = useDBStore(state => {
    if(db_type === "source") {
      return state.selectedSource
    } else if (db_type === "target") {
      return state.selectedTarget
    }
  })

  const updateConnectionDetails = useDBStore((state) => {
    if(db_type === "source") {
      return state.updateSourceDetails
    } else if (db_type === "target") {
      return state.updateTargetDetails
    }
  });

  const activeConnectionDetails = useDBStore(state => {
    if(db_type === "source") {
      return state.selectSourceDetails
    } else if (db_type === "target") {
      return state.selectTargetDetails
    }
  })
  
  const value = activeConnectionDetails?.[field] || "";

  const handleChange = (e) => {
    updateConnectionDetails(field, e.target.value);
  }

  return (
    <div className={`flex flex-col justify-start items-start`}>
      <TextHolder text={title} size="small" weight="light" styles="select-none" />
      <input
        style={{ borderColor: themePalette[activeTheme].borderPrimary, fontSize: header_sizes.small }}
        type={type}
        value={value}
        onChange={e => handleChange(e)}
        className={`w-full outline-none border rounded px-2 py-1 ${!activeConnection && "cursor-default bg-gray-100 pointer-events-none"}`}
      />
    </div>
  );
};

export default InputBar;

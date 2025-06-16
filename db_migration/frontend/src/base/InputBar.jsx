import useDBStore from "../store/dbStore";
import useUIStore from "../store/uistore";
import { header_sizes, TextHolder } from "./Base";
import { themePalette } from "./colorPalette";

const InputBar = ({ title, db_type, field, type = "text" }) => {
  const activeTheme = useUIStore((state) => state.theme);
  const updateConnectionDetails = useDBStore((state) => state.updateConnectionDetails);
  
  const handleChange = (e) => {
    updateConnectionDetails(db_type, field, e.target.value)
  }

  return (
    <div className="flex flex-col justify-start items-start">
      <TextHolder text={title} size="small" weight="light" />
      <input
        style={{ borderColor: themePalette[activeTheme].borderPrimary, fontSize: header_sizes.small }}
        type={type}
        onChange={e => handleChange(e)}
        className="w-full outline-none border rounded px-2 py-1"
      />
    </div>
  );
};

export default InputBar;

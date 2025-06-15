import useUIStore from "../store/uistore";
import { TextHolder } from "./Base";
import { themePalette } from "./colorPalette";

const InputBar = ({title, type="text"}) => {
  const activeTheme = useUIStore(state => state.theme);
  return (
    <div className="flex flex-col justify-start items-start -gap-1">
        <TextHolder text={title} size="small" weight="extralight" />
        <input style={{borderColor: themePalette[activeTheme].borderPrimary}} type={type} className="w-full outline-none border rounded px-2 py-1"  />
    </div>
  );
};

export default InputBar;

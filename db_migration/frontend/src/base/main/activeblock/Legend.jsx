import useUIStore from "../../../store/uistore";
import { themePalette } from "../../colorPalette";

const Legend = ({title}) => {
  const activeTheme = useUIStore((state) => state.theme);
    return (
        <span
            style={{ color: themePalette[activeTheme].text }}
            className="text-[0.7rem] px-1 absolute -top-2 left-4 bg-white font-medium">
            {title}
        </span>
    )
}

export default Legend;
import useUIStore from "../../store/uistore";
import { header_sizes } from "../Base";
import { Link } from "react-router-dom";
import { themePalette } from "../colorPalette";
import { useEffect } from "react";

const HeaderOption = ({ text, path }) => {
  const activeTheme = useUIStore((state) => state.theme);
  const activeOption = useUIStore((state) => state.activePipelineOption);
  const setActiveOption = useUIStore((state) => state.setPipelineOption);

  if (text.length > 14) {
    return "text length exceeded";
  }

  return (
    <Link
      to={path}
      onClick={() => setActiveOption(text)}
      // style={{fontSize:header_sizes.small, backgroundColor: activeOption === text ? "#D1D1D1" : ""}}
      className={`w-44 h-full ${
        activeOption === text ? "font-bold" : ""
      } text-md flex justify-center items-center capitalize px-1 py-1 tracking-wide leading-6 cursor-pointer hover:opacity-90`}
    >
      {text}
    </Link>
  );
};

export default HeaderOption;

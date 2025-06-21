import { Header } from "../../../base/Base";
import { themePalette } from "../../../base/colorPalette";
import HeaderOption from "../../../base/main/HeaderOption";
import useUIStore from "../../../store/uistore";

const SideNavBarBlock = () => {
  const activeTheme = useUIStore((state) => state.theme);
  const border_color = themePalette[activeTheme].border;
  const background = themePalette[activeTheme].backgroundSecondary;
  return (
    <div className="w-[60%] h-full flex justify-start items-center gap-4">
      <header className={`w-full flex justify-start items-center divide-y divide-gray-300`}>
        <HeaderOption text="connections" path="/home/connections" />
        <HeaderOption text="export" path="/home/export" />
      </header>
    </div>
  );
};

export default SideNavBarBlock;


/*
import { Header } from "../../../base/Base";
import { themePalette } from "../../../base/colorPalette";
import HeaderOption from "../../../base/main/HeaderOption";
import useUIStore from "../../../store/uistore";

const SideNavBarBlock = () => {
  const activeTheme = useUIStore((state) => state.theme);
  const border_color = themePalette[activeTheme].border;
  const background = themePalette[activeTheme].backgroundSecondary;
  return (
    <div
      style={{ borderColor: border_color, backgroundColor: background }}
      className="absolute top-0 left-0 bottom-0 w-[200px] h-full border-r flex flex-col justify-start items-center gap-4 py-4">
      <Header text="options available" size="medium" weight="light" />
      <header className={`w-full flex flex-col justify-start items-center divide-y divide-gray-300`}>
        <HeaderOption text="connections" path="/home/connections" />
        <HeaderOption text="export" path="/home/export" />
        <HeaderOption text="history" path="/home/history" />
      </header>
    </div>
  );
};

export default SideNavBarBlock;
*/
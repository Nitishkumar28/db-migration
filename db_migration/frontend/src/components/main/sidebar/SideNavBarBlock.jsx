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
      className="w-[15%] h-full border-r flex flex-col justify-start items-center gap-4 py-4">
      <Header text="options available" size="medium" weight="light" />
      <header className={`w-full flex flex-col justify-start items-center divide-y divide-gray-300`}>
        <HeaderOption text="Connections" path="/home/connections" />
        <HeaderOption text="transfer" path="/home/transfer" />
        <HeaderOption text="validation" path="/home/validation" />
        <HeaderOption text="raw data" path="/home/raw-data" />
      </header>
    </div>
  );
};

export default SideNavBarBlock;

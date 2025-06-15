import { themePalette } from "../../base/colorPalette";
import useUIStore from "../../store/uistore";
import ActionBlock from "./activeblock/ActionBlock";
import SideNavBarBlock from "./sidebar/SideNavBarBlock";

const MainBody = () => {
  const activeTheme = useUIStore(state => state.theme);
  return (
    <div className="w-full h-screen flex flex-col items-center justify-start gap-2 px-[10%] pb-[1%]">
      <div 
      style={{borderColor: themePalette[activeTheme].border}}
      className="flex w-full h-full justify-start items-center gap-2 border border-[#E5E5E5] rounded-xl shadow overflow-hidden">
        <SideNavBarBlock />
        <ActionBlock />
      </div>
    </div>
  );
};

export default MainBody;
import { themePalette } from "../../base/colorPalette";
import useUIStore from "../../store/uistore";
import ActionBlock from "./activeblock/ActionBlock";
import SideNavBarBlock from "./sidebar/SideNavBarBlock";

const MainBody = () => {
  const activeTheme = useUIStore(state => state.theme);
  return (
    <div className="w-full h-screen flex flex-col items-center justify-start gap-2 border-b">
      <div 
      style={{borderColor: themePalette[activeTheme].borderPrimary}}
      className="flex w-full h-full justify-start items-center overflow-hidden">
        <SideNavBarBlock />
        <ActionBlock />
      </div>
    </div>
  );
};

export default MainBody;
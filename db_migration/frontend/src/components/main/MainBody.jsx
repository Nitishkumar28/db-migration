import { themePalette } from "../../base/colorPalette";
import useUIStore from "../../store/uistore";
import Footer from "../Footer";
import ActionBlock from "./activeblock/ActionBlock";
import SideNavBarBlock from "./sidebar/SideNavBarBlock";

const MainBody = () => {
  const activeTheme = useUIStore(state => state.theme);
  return (
    <div className="relative w-full h-screen flex flex-col items-center justify-between gap-10 px-[10%] overflow-scroll">
      <div 
      // style={{borderColor: themePalette[activeTheme].borderPrimary}}
      className="flex w-full min-h-[90%] justify-start items-center overflow-hidden border border-gray-400 rounded-xl">
        <SideNavBarBlock />
        <ActionBlock />
      </div>
      <Footer />
    </div>
  );
};

export default MainBody;
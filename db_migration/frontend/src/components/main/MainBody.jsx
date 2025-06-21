import { themePalette } from "../../base/colorPalette";
import useUIStore from "../../store/uistore";
import Footer from "../Footer";
import ActionBlock from "./activeblock/ActionBlock";
import SideNavBarBlock from "./sidebar/SideNavBarBlock";

const MainBody = () => {
  const activeTheme = useUIStore(state => state.theme);
  return (
    <div className="relative w-full h-screen flex justify-center items-center">
        {/* <SideNavBarBlock /> */}
        <ActionBlock />
    </div>
  );
};

export default MainBody;
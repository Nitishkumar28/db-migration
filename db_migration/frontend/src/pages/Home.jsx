import { themePalette } from "../base/colorPalette";
import MainBody from "../components/main/MainBody";
import Navbar from "../components/Navbar";
import useUIStore from "../store/uistore";

const Home = () => {
  const activeTheme = useUIStore(state => state.theme);
  return (
    <div
    style={{backgroundColor: themePalette[activeTheme].background, color: themePalette[activeTheme].text}}
    className="w-full h-screen flex flex-col items-center justify-start">
      <Navbar />
      <MainBody />
    </div>
  );
};

export default Home;

import { themePalette } from "../base/colorPalette";
import MainBody from "../components/main/MainBody";
import Navbar from "../components/Navbar";
import { healthCheck } from "../hooks/urls";
import { useFetch } from "../hooks/useFetch";
import useUIStore from "../store/uistore";
import WebsocketsTest from "./WebsocketsTest";

const Home = () => {
  const activeTheme = useUIStore(state => state.theme);
  // const {data, loading, error} = useFetch(healthCheck);
  // console.log("DEBUG", data, loading, error);
  return (
    <div
    style={{backgroundColor: themePalette[activeTheme].background, color: themePalette[activeTheme].text}}
    className="w-full h-screen flex flex-col items-center justify-start gap-4">
      <Navbar />
      {/* <WebsocketsTest /> */}
      <MainBody />
    </div>
  );
};

export default Home;

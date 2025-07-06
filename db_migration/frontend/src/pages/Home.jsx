import { useEffect } from "react";
import { themePalette } from "../base/colorPalette";
import MainBody from "../components/main/MainBody";
import Navbar from "../components/Navbar";
import { cookieTestAPI, userDetailsAPI } from "../hooks/urls";
import { useFetch } from "../hooks/useFetch";
import useUIStore from "../store/uistore";
import useUserStore from "../store/userStore";

const Home = () => {
  const activeTheme = useUIStore((state) => state.theme);
  const { userDetails, setUserDetails } = useUserStore();
  // const { data:cookies } = useFetch(cookieTestAPI()); 
  const { data } = useFetch(userDetailsAPI()); 

  useEffect(() => {
    if (data) {
      setUserDetails(data);
    }
}, [data])
  return (
    <div
      style={{
        // backgroundColor: themePalette[activeTheme].background,
        color: themePalette[activeTheme].text,
      }}
      className="flex flex-col items-center justify-start w-full h-screen bg-main"
    >
      <Navbar />
      <MainBody />
    </div>
  );
};

export default Home;

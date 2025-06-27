import { Outlet } from "react-router-dom";
import StatusBar from "./StatusBar";
import Footer from "../../Footer";


const ActionBlock = () => {
  return (
    <div className="px-[150px] w-full h-full">
      <div className="w-full h-full flex flex-col px-4">
        <StatusBar />
        <Outlet />
        <Footer />
      </div>
    </div>
  );
};


export default ActionBlock;
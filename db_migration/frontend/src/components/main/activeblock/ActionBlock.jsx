import { Outlet } from "react-router-dom";
import Footer from "./Footer";


const ActionBlock = () => {
  return (
    <div className="relative w-full h-full flex flex-col">
      <div className="flex-1 overflow-y-auto w-full">
        <Outlet />
      </div>
      <Footer />
    </div>
  );
};


export default ActionBlock;
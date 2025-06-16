import { Outlet } from "react-router-dom";
import Footer from "./Footer";


const ActionBlock = () => {
  return (
    <div className="relative w-full h-full flex flex-col justify-start items-center">
      <Outlet />
      <Footer />
    </div>
  );
};


export default ActionBlock;
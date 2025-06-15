import { Outlet } from "react-router-dom";
import Footer from "./Footer";


const ActionBlock = () => {
  return (
    <div className="relative w-full h-full border-0 text-center flex flex-col justify-start items-center gap-0">
      <Outlet />
      <Footer />
    </div>
  );
};


export default ActionBlock;
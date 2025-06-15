import { Outlet } from "react-router-dom";
import { Header } from "../../../base/Base";


const ActionBlock = () => {
  return (
    <div className="w-[80%] h-full border-0 text-center p-5 flex flex-col justify-start items-center gap-4">
      <Outlet />
    </div>
  );
};


export default ActionBlock;
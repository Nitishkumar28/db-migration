import { BaseButton } from "../base/Base";
import MainHeaderSection from "./MainHeaderSection";
import { Icon } from "@iconify/react";
import UserDropdown from "./UserDropdown";
import useUserStore from "../store/userStore";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
  const { isLogged, userDetails, setUserDetails } = useUserStore();
  const navigate = useNavigate();
  return (
    <div className="flex justify-between items-center gap-1 w-full border-b border-gray-200 px-2.5 py-2">
      <div className="w-[30%]">
        <span className="text-lg font-semibold leading-7 tracking-wider">
          Cloudserv.ai
        </span>
      </div>
      <MainHeaderSection />
      <div className="w-[30%] flex justify-end items-center gap-1">
        <UserDropdown
          isLogged={isLogged}
          userDetails={userDetails}
          onClearData={() => {
            console.log("Clearing data");
          }}
          onLogout={() => {
            console.log("Logging out");
            setUserDetails(null)
            localStorage.setItem("is_logged", "false");
            navigate("/login");
          }}
        />
      </div>
    </div>
  );
};

export default Navbar;

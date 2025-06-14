import { NavbarOption } from "../base/Base";
import MainHeaderSection from "./main/MainHeaderSection";

const Navbar = () => {
  return (
    <div className="flex justify-between items-center gap-1 w-full border-b-0 border-b-gray-200 px-2.5 py-5">
      <div className="w-[30%]">
        <NavbarOption text="logo" />
      </div>
      <MainHeaderSection />
      <div className="w-[30%] flex justify-end items-center gap-4">
        <NavbarOption text="services" />
        <NavbarOption text="history" />
        <NavbarOption text="login" />
      </div>
    </div>
  );
};

export default Navbar;

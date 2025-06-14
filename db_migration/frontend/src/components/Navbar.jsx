import { NavbarOption } from "../base/Base";

const Navbar = () => {
  return (
    <div className="flex justify-between items-center gap-1 w-full h-10 bg-teal-800 px-2.5 py-5">
      <div className="w-[30%]">
        <NavbarOption text="logo" />
      </div>
      <div className="w-[70%] flex justify-end items-center gap-2">
        <NavbarOption text="services" />
        <NavbarOption text="history" />
        <NavbarOption text="login" />
      </div>
    </div>
  );
};

export default Navbar;

import { BaseButton } from "../base/Base";
import MainHeaderSection from "./MainHeaderSection";
import { Icon } from '@iconify/react';

const Navbar = () => {
  return (
    <div className="flex justify-between items-center gap-1 w-full border-b border-gray-200 px-2.5 py-2">
      <div className="w-[30%]">
        <span className="tracking-wider leading-7 text-lg font-semibold">Cloudserv.ai</span>
      </div>
      <MainHeaderSection />
      <div className="w-[30%] flex justify-end items-center gap-1">
        <BaseButton text="Services" className="font-normal py-1 px-2 border-none shadow-none border-[#03729A] text-[#03729A] rounded-md">
          <Icon icon="mdi:cogs" width="20" height="20" />
        </BaseButton>
        <BaseButton text="" className="font-normal bg-none border-none shadow-none text-[#03729A]">
          <Icon icon="mdi:bell" width="20" height="20" />
        </BaseButton>
        <BaseButton text="login" className="font-normal py-1 px-2 border-none shadow-none border-[#03729A] text-[#03729A]  rounded-md">
          <Icon icon="mdi:login" width="20" height="20" />
        </BaseButton>
      </div>
    </div>
  );
};

export default Navbar;

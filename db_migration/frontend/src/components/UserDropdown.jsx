import { useEffect, useRef, useState } from "react";
import { Icon } from "@iconify/react";

const UserDropdown = ({ isLogged, userDetails, onClearData, onLogout }) => {
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef(null);

    useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setOpen(false);
      }
    };

    window.addEventListener("click", handleClickOutside);
    return () => window.removeEventListener("click", handleClickOutside);
  }, []);

  const toggleDropdown = () => setOpen((prev) => !prev);

  return (
    <div ref={dropdownRef} className="relative inline-block text-left">
      <button
        onClick={toggleDropdown}
        className="font-normal py-1 px-2 border-none shadow-none text-[#03729A] rounded-md flex items-center gap-1 capitalize"
      >
        {isLogged && userDetails
          ? `${userDetails.first_name} ${userDetails.last_name}`
          : "Login"}
        <Icon icon="mdi:chevron-down" width="20" height="20" />
      </button>

      {open && (
        <div className="absolute right-0 z-50 w-40 mt-2 bg-white border border-gray-200 rounded shadow-md">
          <button
            onClick={() => {
              onClearData();
              setOpen(false);
            }}
            className="block w-full px-4 py-2 text-sm text-left text-gray-700 hover:bg-gray-100"
          >
            Clear Data
          </button>
          <button
            onClick={() => {
              onLogout();
              setOpen(false);
            }}
            className="block w-full px-4 py-2 text-sm text-left text-gray-700 hover:bg-gray-100"
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
};

export default UserDropdown;

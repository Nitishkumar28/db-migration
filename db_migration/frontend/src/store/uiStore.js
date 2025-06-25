import { create } from "zustand";
import { persist } from "zustand/middleware";

const useUIStore = create(
  persist(
    (set) => ({
      // Variables
      theme: "calm",
      mode: "light",
      activeNavbarOption: "",
      activePipelineOption: "",
      isDropdownOpen: false,

      // Methods
      setTheme: (newTheme) => {
        set(() => ({ theme: newTheme }));
      },
      setMode: (newMode) => {
        set(() => ({ mode: newMode }));
      },
      setNavbarOption: (currentOption) => {
        set(() => ({ activeNavbarOption: currentOption }));
      },
      setPipelineOption: (currentOption) => {
        set(() => ({ activePipelineOption: currentOption }));
      },
      setIsDropdownOpen: (currentOption) => {
        set(() => ({ isDropdownOpen: currentOption }));
      },
    }),
    { name: "theme-store" }
  )
);

export default useUIStore;

import { create } from 'zustand';
import { persist } from 'zustand/middleware'

const useUIStore = create(
    persist(
        (set) => ({
            // Variables
            theme: "calm",
            activeNavbarOption: "",
            activePipelineOption: "",
            isDropdownOpen: false,
            
            // Methods
            setTheme: (newTheme) => {
                set(() => ({ theme: newTheme }))
            },
            setNavbarOption: (currentOption) => {
                set(() => ({ activeNavbarOption: currentOption }))
            },
            setPipelineOption: (currentOption) => {
                set(() => ({ activePipelineOption: currentOption }))
            },
            setIsDropdownOpen: (currentOption) => {
                set(() => ({ isDropdownOpen: currentOption }))
            }
        }),
        {name: "theme-store"}
    )
);

export default useUIStore;

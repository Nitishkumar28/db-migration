import { create } from 'zustand';
import { persist } from 'zustand/middleware'

const useUIStore = create(
    persist(
        (set) => ({
            // Variables
            theme: "calm",
            activeNavbarOption: "",
            activePipelineOption: "",
            
            // Methods
            setTheme: (newTheme) => {
                set(() => ({ theme: newTheme }))
            },
            setNavbarOption: (currentOption) => {
                set(() => ({ activeNavbarOption: currentOption }))
            },
            setPipelineOption: (currentOption) => {
                set(() => ({ activePipelineOption: currentOption }))
            }
        }),
        {name: "theme-store"}
    )
);

export default useUIStore;

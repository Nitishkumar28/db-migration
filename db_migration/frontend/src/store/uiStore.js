import { create } from 'zustand';
import { persist } from 'zustand/middleware'

const useUIStore = create(
    persist(
        (set) => ({
            // Variables
            isDarkMode: false,
            
            // Methods
            toggleDarkMode: () =>
                set((state) => ({ isDarkMode: !state.isDarkMode })),
            }),
        {name: "theme-store"}
    )
);

export default useUIStore;

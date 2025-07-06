import { create } from "zustand";


const useUserStore = create(
    (set) => ({
        // Variables
        userDetails: null,
        isLogged: JSON.parse(localStorage.getItem("is_logged", "false")),

        // Methods
        setIsLogged: (status) => {
            set(() => ({ isLogged: status }));
        },
        setUserDetails: (data) => {
            set(() => ({ userDetails: data }));
        }
    })
);

export default useUserStore;

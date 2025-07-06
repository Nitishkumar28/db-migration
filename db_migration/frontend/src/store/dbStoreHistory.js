import { create } from "zustand";

const useDBStoreHistoryMain = () => create(
    (set) => ({
      exportFinalStatus: "in progress",
      activeJobID: null,

      // Local history cards
      historyCardsLocal: [],

      // --- History actions ---
      setHistoryCards: (cards) =>
        set(() => ({
          historyCardsLocal: cards,
        })),

      addNewHistoryCard: (card) =>
        set((state) => ({
          historyCardsLocal: [card, ...state.historyCardsLocal],
        })),

      setExportFinalStatus: (status) =>
        set(() => ({ exportFinalStatus: status })),

      setActiveJobID: (job_id) => set(() => ({ activeJobID: job_id })),
    })
);

const useDBStoreHistory = useDBStoreHistoryMain(); 
export default useDBStoreHistory;

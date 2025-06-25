import { create } from "zustand";
import { persist } from "zustand/middleware";
import { initialConnections } from "./index";

const useDBStore = create(
  persist(
    (set, get) => ({
      // Selected DB types
      selectedSource: "",
      selectedTarget: "",

      // Individual DB details
      selectSourceDetails: {},
      selectTargetDetails: {},

      exportFinalStatus: "running",
      activeJobID: null,

      // All connection entries
      connectionDetails: initialConnections,

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

      // --- Selected source/target handlers ---
      setSelectedSource: (source) => set(() => ({ selectedSource: source })),

      setSelectedTarget: (target) => set(() => ({ selectedTarget: target })),

      // --- Source/Target connection detail updates ---
      setSelectedSourceDetails: (details) =>
        set(() => ({ selectSourceDetails: details })),

      setSelectedTargetDetails: (details) =>
        set(() => ({ selectTargetDetails: details })),

      updateSourceDetails: (field, value) =>
        set((state) => ({
          selectSourceDetails: {
            ...state.selectSourceDetails,
            [field]: value,
          },
        })),

      updateTargetDetails: (field, value) =>
        set((state) => ({
          selectTargetDetails: {
            ...state.selectTargetDetails,
            [field]: value,
          },
        })),

      // --- Connection detail handlers ---
      setConnectionDetails: (newDetails) =>
        set(() => ({ connectionDetails: newDetails })),

      readConnection: (db_type) => {
        const state = get();
        return state.connectionDetails.find((conn) => conn.db_type === db_type);
      },

      createConnection: (newConnection) =>
        set((state) => ({
          connectionDetails: [...state.connectionDetails, newConnection],
        })),

      updateConnectionDetails: (db_type, field, value) =>
        set((state) => ({
          connectionDetails: state.connectionDetails.map((conn) =>
            conn.db_type === db_type ? { ...conn, [field]: value } : conn
          ),
        })),

      deleteConnection: (db_type) =>
        set((state) => ({
          connectionDetails: state.connectionDetails.filter(
            (conn) => conn.db_type !== db_type
          ),
        })),
    }),
    {
      name: "db-store",
    }
  )
);

export default useDBStore;

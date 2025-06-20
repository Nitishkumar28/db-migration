import { create } from "zustand";
import { initialConnections } from "./index";
import { persist } from "zustand/middleware";

const initialConnectionDetails = {
  db_type: "",
  server_address: "",
  username: "",
  password: "",
  port: "",
  database_name: "",
  status: "idle",
};

const useDBStore = create(
  persist((set) => ({
    selectedSource: "",
    selectedTarget: "",
    selectSourceDetails: {},
    selectTargetDetails: {},

    connectionDetails: initialConnections,

    setSelectedSource: (source) => {
      set(() => ({
        selectedSource: source,
      }));
    },

    setSelectedTarget: (target) => {
      set(() => ({
        selectedTarget: target,
      }));
    },

    setSelectedSourceDetails: (newSourceDetails) => {
      set(() => ({
        selectSourceDetails: newSourceDetails,
      }));
    },

    setSelectedTargetDetails: (newTargetDetails) => {
      set(() => ({
        selectTargetDetails: newTargetDetails,
      }));
    },

    updateSourceDetails: (field, value) => {
      set((state) => ({
        selectSourceDetails: { ...state.selectSourceDetails, [field]: value },
      }));
    },

    updateTargetDetails: (field, value) => {
      set((state) => ({
        selectTargetDetails: { ...state.selectTargetDetails, [field]: value },
      }));
    },

    setConnectionDetails: (newDetails) => {
      set(() => ({
        connectionDetails: newDetails,
      }));
    },

    readConnection: (db_type) => {
      return connectionDetails.find((conn) => conn.db_type === db_type);
    },

    createConnection: (newConnection) => {
      set((state) => ({
        connectionDetails: [...state.connectionDetails, newConnection],
      }));
    },

    updateConnectionDetails: (db_type, field, value) => {
      set((state) => ({
        connectionDetails: state.connectionDetails.map((conn) =>
          conn.db_type === db_type ? { ...conn, [field]: value } : conn
        ),
      }));
    },

    deleteConnection: (db_type) => {
      set((state) => ({
        connectionDetails: state.connectionDetails.filter(
          (conn) => conn.db_type !== db_type
        ),
      }));
    },
  }))
);

export default useDBStore;

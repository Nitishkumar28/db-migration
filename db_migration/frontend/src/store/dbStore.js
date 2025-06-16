import { create } from 'zustand';
import { initialConnections } from './index';

const useDBStore = create((set, get) => ({
    selectedSource: "",
    selectedTarget: "",
    connectionDetails: initialConnections,

    setSelectedSource: (source) => {
        set(() => ({
            selectedSource: source
        }))
    },
    
    setSelectedTarget: (target) => {
        set(() => ({
            selectedTarget: target
        }))
    },

  createConnection: (newConnection) => {
    set((state) => ({
      connectionDetails: [...state.connectionDetails, newConnection]
    }));
  },

  readConnection: (db_type) => {
    return get().connectionDetails.find((conn) => conn.db_type === db_type);
  },

  updateConnectionDetails: (db_type, field, value) => {
    set((state) => ({
      connectionDetails: state.connectionDetails.map((conn) =>
        conn.db_type === db_type
          ? { ...conn, [field]: value }
          : conn
      )
    }));
  },

  deleteConnection: (db_type) => {
    set((state) => ({
      connectionDetails: state.connectionDetails.filter(
        (conn) => conn.db_type !== db_type
      )
    }));
  }
}));

export default useDBStore;

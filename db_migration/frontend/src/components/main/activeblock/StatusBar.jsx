import { header_sizes } from "../../../base/Base";
import { themePalette } from "../../../base/colorPalette";
import StatusLight from "../../../base/main/StatusLight";
import useDBStore from "../../../store/dbStore";
import useUIStore from "../../../store/uistore";
import SideNavBarBlock from "../sidebar/SideNavBarBlock";

const StatusBar = () => {
  const activeTheme = useUIStore(state => state.theme);
  const { selectedSource, selectedTarget } = useDBStore();

    const selectSourceDetails = useDBStore((state) => {
      const current = state.connectionDetails.find(
        (conn) => conn.db_type === selectedSource?.toLowerCase()
      );
      return current;
    });

    const selectTargetDetails = useDBStore((state) => {
      const current = state.connectionDetails.find(
        (conn) => conn.db_type === selectedTarget?.toLowerCase()
      );
      return current;
    });

  return (
    <footer
      style={{ fontSize: header_sizes.small }}
      className="w-full flex justify-start items-center border-b border-gray-200 py-1">
        <SideNavBarBlock />
      <div className="w-full flex justify-end items-center gap-4 py-1">
        <StatusLight text="Source" status={selectSourceDetails?.status} />
        <StatusLight text="Target" status={selectTargetDetails?.status} />
      </div>
    </footer>
  );
};


export default StatusBar;



/*
import { header_sizes } from "../../../base/Base";
import { themePalette } from "../../../base/colorPalette";
import StatusLight from "../../../base/main/StatusLight";
import useDBStore from "../../../store/dbStore";
import useUIStore from "../../../store/uistore";
import SideNavBarBlock from "../sidebar/SideNavBarBlock";

const StatusBar = () => {
  const activeTheme = useUIStore(state => state.theme);
  const { selectedSource, selectedTarget } = useDBStore();

    const selectSourceDetails = useDBStore((state) => {
      const current = state.connectionDetails.find(
        (conn) => conn.db_type === selectedSource?.toLowerCase()
      );
      return current;
    });

    const selectTargetDetails = useDBStore((state) => {
      const current = state.connectionDetails.find(
        (conn) => conn.db_type === selectedTarget?.toLowerCase()
      );
      return current;
    });

  return (
    <footer
      style={{ fontSize: header_sizes.small }}
      className="w-full border-t-0 px-4 tracking-wide leading-6">
      <div className="w-full flex justify-end items-center gap-4 py-1">
        <StatusLight text="Source" status={selectSourceDetails?.status} />
        <StatusLight text="Target" status={selectTargetDetails?.status} />
      </div>
    </footer>
  );
};


export default StatusBar;
*/
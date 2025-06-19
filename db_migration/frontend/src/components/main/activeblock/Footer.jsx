import { header_sizes } from "../../../base/Base";
import { themePalette } from "../../../base/colorPalette";
import StatusLight from "../../../base/main/StatusLight";
import useDBStore from "../../../store/dbStore";
import useUIStore from "../../../store/uistore";

const Footer = () => {
  const activeTheme = useUIStore(state => state.theme);
  const { selectSourceDetails, selectTargetDetails } = useDBStore();

  return (
    <footer
      style={{ fontSize: header_sizes.small }}
      className="w-full border-t-0 px-[2%] tracking-wide leading-6"
    >
      <div className="w-full flex justify-end items-center gap-4 py-1">
        <StatusLight text="Source" status={selectSourceDetails.status} />
        <StatusLight text="Target" status={selectTargetDetails.status} />
      </div>
    </footer>
  );
};


export default Footer;
import { header_sizes } from "../../../base/Base";
import { themePalette } from "../../../base/colorPalette";
import StatusOption from "../../../base/main/StatusOption";
import useUIStore from "../../../store/uistore";

const Footer = () => {
  const activeTheme = useUIStore(state => state.theme);

  return (
    <footer
      style={{ fontSize: header_sizes.small }}
      className="w-full border-t-0 px-[2%] tracking-wide leading-6"
    >
      <div className="w-full flex justify-end items-center gap-4 py-1">
        <StatusOption text="Source" status="connected" />
        <StatusOption text="Target" status="pending" />
      </div>
    </footer>
  );
};


export default Footer;
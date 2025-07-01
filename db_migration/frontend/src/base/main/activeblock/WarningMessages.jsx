import useUIStore from "../../../store/uistore";
import { TextHolder } from "../../Base";
import { themePalette } from "../../colorPalette";

const WarningMessages = () => {
  const activeTheme = useUIStore((state) => state.theme);
  return (
    <div
      style={{ borderColor: themePalette[activeTheme].border }}
      className="w-[20%] h-full flex flex-col justify-start items-start p-2 border-l"
    >
      <TextHolder
        text="* Servername: required"
        size="extrasmall"
        weight="light"
        type="error"
      />
      <TextHolder
        text="* Username: required"
        size="extrasmall"
        weight="light"
        type="error"
      />
      <TextHolder
        text="* Password: required"
        size="extrasmall"
        weight="light"
        type="error"
      />
      <TextHolder
        text="* Database: Not required "
        size="extrasmall"
        weight="light"
      />
    </div>
  );
};

export default WarningMessages;
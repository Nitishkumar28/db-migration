import { TextHolder } from "../../../../base/Base";
import { themePalette } from "../../../../base/colorPalette";
import InputBar from "../../../../base/InputBar";
import useUIStore from "../../../../store/uistore";

const ConnectionDetails = ({ title }) => {
  const activeTheme = useUIStore((state) => state.theme);
  return (
    <fieldset
      style={{ borderColor: themePalette[activeTheme].borderPrimary }}
      className="relative border rounded-lg shadow w-[80%] h-full flex flex-col justify-start items-center -gap-10 pb-3 pt-2"
    >
      <lagend
        style={{ color: themePalette[activeTheme].text }}
        className="text-[0.8rem] px-1 absolute -top-2 left-4 bg-white"
      >
        {title}
      </lagend>
      <div className="w-full h-full flex justify-around items-center gap-4 px-[2%]">
        <div className="w-[55%] h-full py-[2%] flex flex-col justify-start items-between gap-2">
          <InputBar title="Server Name" />
          <InputBar title="Username" />
          <InputBar title="Database" />
        </div>
        <div className="w-[25%] h-full py-[2%] flex flex-col justify-start items-between gap-2">
          <InputBar title="Port" size="small" />
          <InputBar title="Password" />
        </div>
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
      </div>
      <button
        style={{ backgroundColor: themePalette[activeTheme].backgroundPrimary }}
        className="bg-red-200 px-1 py-1.5 rounded shadow"
      >
        Test connection
      </button>
    </fieldset>
  );
};

export default ConnectionDetails;

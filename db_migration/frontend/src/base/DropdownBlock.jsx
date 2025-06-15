import { useState } from "react";
import { themePalette } from "./colorPalette";
import useUIStore from "../store/uistore";
import { Header, TextHolder } from "./Base";

const DropdownOption = ({ ...props }) => {
  const activeTheme = useUIStore((state) => state.theme);
  const selectedOptionBG = themePalette[activeTheme].backgroundPrimary;
  const handleOptionSelect = () => {
    props.setSelectedOption(props.option);
    setIsOpen(false);
  };
  return (
    <span
      style={{
        backgroundColor:
          props.option === props.selectedOption && selectedOptionBG
      }}
      className="w-full text-left px-2 py-1"
      onClick={() => handleOptionSelect()}
    >
      <TextHolder text={props.option || "Select a database"} size="small" weight="light" />
    </span>
  );
};

const DropdownOptions = ({ options, ...props }) => {
  const activeTheme = useUIStore((state) => state.theme);
  const _options = [null, ...options];    // null allows us to set default option
  return (
    <div
      style={{ borderColor: themePalette[activeTheme].borderPrimary }}
      className="absolute top-full mt-0.5 min-w-40 max-w-56 z-10 shadow bg-white flex flex-col justify-start items-start divide-y divide-sky-100 border"
    >
      {_options.map((option, idx) => (
        <DropdownOption key={idx} option={option} {...props} />
      ))}
    </div>
  );
};

const InnerDropdownBlock = ({ ...props }) => {
  const activeTheme = useUIStore((state) => state.theme);
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div
      onClick={() => setIsOpen((p) => !p)}
      style={{ borderColor: themePalette[activeTheme].borderPrimary }}
      className="relative w-40 max-w-56 border px-2 py-1 rounded-sm flex justify-between items-center gap-2 cursor-pointer select-none"
    >
      <TextHolder
        text={props.selectedOption || "Select a database"}
        size="small"
      />
      <i className="fa fa-caret-down"></i>
      {isOpen && <DropdownOptions setIsOpen={setIsOpen} {...props} />}
    </div>
  );
};

const DropdownBlock = ({ text = "", ...props }) => {
  return (
    <div className="flex justify-center items-center gap-2">
      {text && <Header text={text} size="normal" weight="medium" />}
      <InnerDropdownBlock {...props} />
    </div>
  );
};

export default DropdownBlock;

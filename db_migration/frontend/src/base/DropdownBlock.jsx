import { useState, useEffect, useRef } from "react";
import { themePalette } from "./colorPalette";
import useUIStore from "../store/uistore";
import { Header, TextHolder } from "./Base";

const DropdownOption = ({ option, selectedOption, setSelectedOption, setIsOpen }) => {
  const activeTheme = useUIStore((state) => state.theme);
  const isSelected = option === selectedOption;
  const selectedBG = themePalette[activeTheme].backgroundPrimary;

  return (
    <span
      onClick={() => {
        setSelectedOption(option);
        setIsOpen(false);
      }}
      style={{
        backgroundColor: isSelected ? selectedBG : "transparent",
      }}
      className="w-full text-left px-2 py-1 hover:bg-sky-100 cursor-pointer"
    >
      <TextHolder
        text={option || "Select a database"}
        size="small"
        weight={isSelected ? "medium" : "light"}
      />
    </span>
  );
};

const DropdownOptions = ({ options, selectedOption, setSelectedOption, setIsOpen }) => {
  const activeTheme = useUIStore((state) => state.theme);
  const fullOptions = [null, ...options];

  return (
    <div
      style={{ borderColor: themePalette[activeTheme].borderPrimary }}
      className="absolute top-full mt-0.5 w-full max-h-48 overflow-y-auto z-10 shadow bg-white flex flex-col justify-start items-start divide-y divide-sky-100 border rounded-sm"
    >
      {fullOptions.map((option, idx) => (
        <DropdownOption
          key={idx}
          option={option}
          selectedOption={selectedOption}
          setSelectedOption={setSelectedOption}
          setIsOpen={setIsOpen}
        />
      ))}
    </div>
  );
};

const InnerDropdownBlock = ({ selectedOption, setSelectedOption, options }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);
  const activeTheme = useUIStore((state) => state.theme);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    const handleKeyDown = (e) => {
      if (e.key === "Escape") setIsOpen(false);
    };

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, []);

  return (
    <div
      ref={dropdownRef}
      className="relative w-40 max-w-56"
    >
      <div
        onClick={() => setIsOpen((prev) => !prev)}
        style={{ borderColor: themePalette[activeTheme].borderPrimary }}
        className="border px-2 py-1 rounded-sm flex justify-between items-center gap-2 cursor-pointer select-none hover:bg-slate-50"
      >
        <TextHolder
          text={selectedOption || "Select a database"}
          size="small"
        />
        <i className="fa fa-caret-down text-xs" />
      </div>
      {isOpen && (
        <DropdownOptions
          options={options}
          selectedOption={selectedOption}
          setSelectedOption={setSelectedOption}
          setIsOpen={setIsOpen}
        />
      )}
    </div>
  );
};

const DropdownBlock = ({ text = "", selectedOption, setSelectedOption, options }) => {
  return (
    <div className="flex justify-center items-center gap-2">
      {text && <Header text={text} size="normal" weight="medium" />}
      <InnerDropdownBlock
        selectedOption={selectedOption}
        setSelectedOption={setSelectedOption}
        options={options}
      />
    </div>
  );
};

export default DropdownBlock;

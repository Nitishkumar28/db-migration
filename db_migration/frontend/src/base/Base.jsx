import { useState } from "react";
import useUIStore from "../store/uistore";
import { themePalette } from "./colorPalette";


export const header_sizes = {
  extrasmall: "10px",
  small: "13px",
  normal: "15px",
  medium: "18px",
  extramedium: "22px",
  large: "30px",
  extralarge: "35px",
};

export const header_weight = {
  extralight: "font-extralight",
  light: "font-light",
  normal: "font-normal",
  medium: "font-medium",
  semibold: "font-semibold",
  bold: "font-bold",
};

const Header = ({ text, size = "medium", weight = "normal", ...props }) => (
  <span
    {...props}
    className={`${header_weight[weight]} leading-6 tracking-wide capitalize w-fit`}
    style={{ fontSize: header_sizes[size] }}
  >
    {text}
  </span>
);

const TextHolder = ({text, size, weight, type, styles="", ...props}) => {
  const activeTheme = useUIStore((state) => state.theme);
  let textColor = "";

  if (type === "error") {
    textColor = themePalette[activeTheme].error;
  }

  return (
    <p
      {...props}
      className={`${header_weight[weight]} w-fit text-wrap ${styles}`}
      style={{ fontSize: header_sizes[size], color: textColor }}
    >
      {text}
    </p>
  )
}

const NavbarOption = ({ text }) => {
  const activeTheme = useUIStore((state) => state.theme);
  const activeOption = useUIStore((state) => state.activeNavbarOption);
  const setActiveOption = useUIStore((state) => state.setNavbarOption);

  if (text.length > 14) {
    return "text length exceeded";
  }

  return (
    <span
      onClick={() => setActiveOption(text)}
      style={{
        fontSize: header_sizes.small,
        borderColor: themePalette[activeTheme].border,
        backgroundColor:
          activeOption === text
            ? themePalette[activeTheme].backgroundPrimary
            : "",
      }}
      className="min-w-10 max-w-36 h-full flex justify-center items-center border px-2 py-1 rounded-md font-normal tracking-wide leading-6 cursor-pointer capitalize"
    >
      {text}
    </span>
  );
};

const BaseButton = ({text, type, styles="", ...props}) => {
  const activeTheme = useUIStore((state) => state.theme);
  return (
      <button
      {...props}
        style={{ 
          borderColor: themePalette[activeTheme].borderPrimary, 
          fontSize: header_sizes.small 
        }}
        className={`min-w-20 border px-1 py-1 rounded shadow cursor-pointer capitalize hover:opacity-80 ${styles}`}>
        {text}
      </button>
  )
}

export { Header, TextHolder, NavbarOption, BaseButton };

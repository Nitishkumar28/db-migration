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

const TextHolder = ({text, size, weight, type, ...props}) => {
  const activeTheme = useUIStore((state) => state.theme);
  let textColor = "";

  if (type === "error") {
    textColor = themePalette[activeTheme].error;
  }

  return (
    <span
      {...props}
      className={`${header_weight[weight]} w-fit`}
      style={{ fontSize: header_sizes[size], color: textColor }}
    >
      {text}
    </span>
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
      className="min-w-10 max-w-36 h-full flex justify-center items-center border capitalize px-2 py-1 rounded-md font-normal tracking-wide leading-6 cursor-pointer"
    >
      {text}
    </span>
  );
};


export { Header, TextHolder, NavbarOption };

const header_sizes = {
  extrasmall: "10px",
  small: "13px",
  medium: "20px",
  large: "30px",
  extralarge: "35px",
};

const header_weight = {
  extralight: "font-extralight",
  light: "font-light",
  normal: "font-normal",
  medium: "font-medium",
  semibold: "font-semibold",
  bold: "font-bold",
};

const Header = ({ text, size = "medium", weight = "normal" }) => (
  <span
    className={`${header_weight[weight]} leading-6 tracking-wide capitalize`}
    style={{ fontSize: header_sizes[size] }}
  >
    {text}
  </span>
);

const NavbarOption = ({ text }) => {
  if (text.length > 11) {
    return "text length exceeded";
  }
  return (
    <span className="min-w-10 max-w-20 h-full flex justify-center items-center border capitalize px-2 py-1 rounded-md font-normal text-md tracking-wide leading-6 cursor-pointer">
      {text}
    </span>
  );
};

export { Header, NavbarOption };

import { Icon } from "@iconify/react/dist/iconify.js";
import rightArrow from "../assets/arrow_right.png";
import exportIcon from "../assets/upload.png";
import lightIcon from "../assets/light.png";
import darkIcon from "../assets/dark.png";

export const PostgresqlIcon = ({ size = 20, className = "" }) => (
  <i
    style={{ fontSize: size }}
    className={`devicon-postgresql-plain-wordmark colored ${className}`}
  ></i>
);

export const MySQLIcon = ({ size = 20, className = "" }) => (
  <i
    style={{ fontSize: size }}
    className={`devicon-mysql-plain-wordmark colored ${className}`}
  ></i>
);

export const OracleIcon = ({ size = 20, className = "" }) => (
  <i
    style={{ fontSize: size }}
    className={`devicon-oracle-original colored ${className}`}
  ></i>
);

export const LeftArrowIcon = ({ size = "20" }) => (
  <Icon icon={`mdi:arrow-left`} width={size} height={size} />
);

export const rightArrowIcon = ({ size = "20" }) => (
  <Icon icon={`mdi:arrow-right`} width={size} height={size} />
);

export const getDBIcon = (db_type, size = 80) => {
  switch (db_type) {
    case "mysql":
      return <MySQLIcon size={size} />;
    case "postgresql":
      return <PostgresqlIcon size={size} />;
    case "oracle":
      return <OracleIcon size={size} />;
  }
};

export const ExportIcon = ({ size = 25, className = "" }) => (
  <img
    src={exportIcon}
    alt="exportIcon"
    width={size}
    height={size}
    className={className}
  />
);

export const LightIcon = ({ size = 20, className = "" }) => (
  <img
    src={lightIcon}
    alt="lightIcon"
    width={size}
    height={size}
    className={className}
  />
);

export const DarkIcon = ({ size = 20, className = "" }) => (
  <img
    src={darkIcon}
    alt="darkIcon"
    width={size}
    height={size}
    className={className}
  />
);

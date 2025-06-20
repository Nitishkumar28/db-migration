import rightArrow from '../assets/arrow_right.png';
import exportIcon from '../assets/upload.png'
import lightIcon from '../assets/light.png'
import darkIcon from '../assets/dark.png'

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

export const RightArrowIcon = ({ size = 20, className = "" }) => (
    <img src={rightArrow} alt="rightarrow" width={size} height={size} className={className} />
);

export const ExportIcon = ({ size = 25, className = "" }) => (
    <img src={exportIcon} alt="exportIcon" width={size} height={size} className={className} />
);

export const LightIcon = ({ size = 20, className = "" }) => (
    <img src={lightIcon} alt="lightIcon" width={size} height={size} className={className} />
);

export const DarkIcon = ({ size = 20, className = "" }) => (
    <img src={darkIcon} alt="darkIcon" width={size} height={size} className={className} />
);
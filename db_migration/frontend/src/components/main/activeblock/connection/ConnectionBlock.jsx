import { useState } from "react";
import { header_sizes } from "../../../../base/Base";
import ConnectionHeader from "./Header";
import DetailsBlock from "./DetailsBlock";

const ConnectionBlock = () => {
  const [selectedSource, setSelectedSource] = useState("");
  const [selectedTarget, setSelectedTarget] = useState("");
  const connectionHeaderProps = {
    selectedSource,
    selectedTarget,
    setSelectedSource,
    setSelectedTarget
  }
  return (
    <div 
    style={{fontSize: header_sizes.normal}}
    className="w-full h-full px-[5%] py-[1%]">
      <div className="w-full h-full flex flex-col justify-around items-center gap-4 divide-y-2 divide-sky-100 ">
        <ConnectionHeader {...connectionHeaderProps} />
        <div className="w-full h-full flex flex-col justify-start items-center gap-6">
          <DetailsBlock title={`Source: ${selectedSource || "select a source from above dropdown"}`} db_type={selectedSource?.toLowerCase()} />
          <DetailsBlock title={`Target: ${selectedTarget || "select a target from above dropdown"}`} db_type={selectedTarget?.toLowerCase()} />
        </div>
      </div>
    </div>
  );
};


export default ConnectionBlock;
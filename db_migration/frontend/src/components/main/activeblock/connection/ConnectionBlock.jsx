import { useState } from "react";
import { header_sizes, TextHolder } from "../../../../base/Base";
import ConnectionHeader from "./ConnectionHeader";
import ConnectionDetails from "./ConnectionDetails";

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
    className="w-full h-full px-[5%] py-[2.5%]">
      <div className="w-full h-full flex flex-col justify-start items-center gap-6">
        <ConnectionHeader {...connectionHeaderProps} />
        <div className="w-full flex flex-col justify-start items-center gap-10">
          <ConnectionDetails title={`Source: ${selectedSource || "select a source from above dropdown"}`} />
          <ConnectionDetails title={`Target: ${selectedTarget || "select a target from above dropdown"}`} />
        </div>
      </div>
    </div>
  );
};


export default ConnectionBlock;
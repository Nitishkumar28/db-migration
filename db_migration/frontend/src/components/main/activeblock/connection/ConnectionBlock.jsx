import { useEffect, useState } from "react";
import { header_sizes } from "../../../../base/Base";
import ConnectionHeader from "./Header";
import DetailsBlock from "./DetailsBlock";
import useDBStore from "../../../../store/dbStore";
import useUIStore from "../../../../store/uistore";
import connectionsBG from "../../../../assets/connections_bg.png";

const ConnectionBlock = () => {
  const {selectedSource, setSelectedSource} = useDBStore();
  const {selectedTarget, setSelectedTarget} = useDBStore();
  const { setPipelineOption } = useUIStore();

  useEffect(() => {
    setPipelineOption("connections")
  }, [])

  const connectionHeaderProps = {
    selectedSource,
    selectedTarget,
    setSelectedSource,
    setSelectedTarget
  }

  return (
    <div 
    style={{
      fontSize: header_sizes.normal,
      // backgroundImage: `url(${connectionsBG})`,
      // backgroundSize: "cover",
      // backgroundRepeat: "no-repeat",
    }}
    className="w-full h-full rounded-xl">
      <div className="w-full h-full flex flex-col justify-around items-center gap-4 divide-y-2 divide-sky-100 ">
        <ConnectionHeader {...connectionHeaderProps} />
        <div className="w-full h-full flex flex-col justify-start items-center gap-8">
          <DetailsBlock title={`Source: ${selectedSource || "select a source from above dropdown"}`} db_type="source" />
          <DetailsBlock title={`Target: ${selectedTarget || "select a target from above dropdown"}`} db_type="target" />
        </div>
      </div>
    </div>
  );
};


export default ConnectionBlock;
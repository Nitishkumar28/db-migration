import ActionBlock from "./ActionBlock";
import OutputBlock from "./OutputBlock";

const MainBody = () => {
  return (
    <div className="w-full h-screen flex flex-col items-center justify-start gap-2 px-[1%] pb-[1%]">
      <div className="flex w-full h-full justify-start items-center px-2 gap-2 border border-gray-[#1F2937] rounded-lg shadow">
        <ActionBlock />
        <OutputBlock />
      </div>
    </div>
  );
};

export default MainBody;
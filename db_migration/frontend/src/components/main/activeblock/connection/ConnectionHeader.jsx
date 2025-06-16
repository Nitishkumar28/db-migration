import DropdownBlock from "../../../../base/DropdownBlock";

const ConnectionHeader = ({
  selectedSource,
  setSelectedSource,
  selectedTarget,
  setSelectedTarget,
}) => {
  const dbOptions = ["MySQL", "PostgreSQL", "MySQL Server"];
  return (
    <header className="w-full flex justify-center items-center gap-8 pb-3">
      <DropdownBlock
        text="source database"
        options={dbOptions.filter((option) => option !== selectedTarget)}
        selectedOption={selectedSource}
        setSelectedOption={setSelectedSource}
      />

      <DropdownBlock
        text="target database"
        options={dbOptions.filter((option) => option !== selectedSource)}
        selectedOption={selectedTarget}
        setSelectedOption={setSelectedTarget}
      />
    </header>
  );
};

export default ConnectionHeader;

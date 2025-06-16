import { useEffect, useState } from "react";
import { BaseButton } from "../../../../base/Base";
import { themePalette } from "../../../../base/colorPalette";
import InputBar from "../../../../base/InputBar";
import Lengend from "../../../../base/main/activeblock/Legend";
import WarningMessages from "../../../../base/main/activeblock/WarningMessages";
import useDBStore from "../../../../store/dbStore";
import useUIStore from "../../../../store/uistore";
import Legend from "../../../../base/main/activeblock/Legend";

const FirstColumn = ({db_type}) => {
  return (
        <div className="w-[55%] h-full py-[2%] flex flex-col justify-start items-between gap-2">
          <InputBar title="Server Address" field="server_address" db_type={db_type} />
          <InputBar title="Username" field="username" db_type={db_type} />
          <InputBar title="Database Name" field="database_name" db_type={db_type} />
        </div>
  )
}

const SecondColumn = ({db_type}) => {
  return (
        <div className="w-[25%] h-full py-[2%] flex flex-col justify-start items-between gap-2">
          <InputBar title="Port" size="small" field="port" db_type={db_type} />
          <InputBar title="Password" field="password" type="password" db_type={db_type} />
        </div>
  )
}

const ConnectionDetailsBlock = ({ title, db_type }) => {
  const activeTheme = useUIStore((state) => state.theme);

  return (
    <div
      style={{ borderColor: themePalette[activeTheme].borderPrimary }}
      className="relative border rounded-lg shadow-md w-[90%] h-full flex flex-col justify-start items-center gap-1 py-3">
      <Legend title={title} />
      <div className="w-full h-fit flex justify-around items-center gap-4 px-[2%]">
        <FirstColumn db_type={db_type} />
        <SecondColumn db_type={db_type} />
        <WarningMessages />
      </div>
      <BaseButton text="test connection" />
    </div>
  );
};

export default ConnectionDetailsBlock;

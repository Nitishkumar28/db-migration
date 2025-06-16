import { BaseButton } from "../../../../base/Base";
import { themePalette } from "../../../../base/colorPalette";
import InputBar from "../../../../base/InputBar";
import WarningMessages from "../../../../base/main/activeblock/WarningMessages";
import useUIStore from "../../../../store/uistore";
import Legend from "../../../../base/main/activeblock/Legend";
import { checkConnectionURL } from "../../../../hooks/urls";
import useDBStore from "../../../../store/dbStore";
import { usePost } from "../../../../hooks/usePost";

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
  const connectionDetails = useDBStore(state => state.connectionDetails);
  const { post, data: result, loading: posting, error: postError } = usePost(checkConnectionURL);

  const handlePost = async () => {
    const postData = connectionDetails.find(conn => conn.db_type === db_type)
    console.log(connectionDetails)
    if (!postData) return console.warn("No matching connection found for", db_type);
    try {
      const status = "success" // await post(postData);
      console.log('Post successful:', status);
    } catch (err) {
      console.error('Post failed:', err.message);
    }
  };


  return (
    <div
      style={{ borderColor: themePalette[activeTheme].borderPrimary }}
      className={`relative border rounded-lg shadow-md w-[90%] h-[60%] flex flex-col justify-center items-center gap-1 py-3 ${!db_type && "opacity-70 pointer-events-none"}`}>
      <Legend title={title} />
      <div className={`w-full h-fit flex justify-around items-center gap-4 px-[2%]`}>
        <FirstColumn db_type={db_type} />
        <SecondColumn db_type={db_type} />
        <WarningMessages />
      </div>
      <div className="flex justify-center items-center gap-4">
        <BaseButton 
        onClick={() => handlePost()} 
        text={posting ? "saving...": "save details"}
        styles="bg-green-50" />
        <BaseButton text="test connection" styles="bg-sky-50" />
      </div>
    </div>
  );
};

export default ConnectionDetailsBlock;

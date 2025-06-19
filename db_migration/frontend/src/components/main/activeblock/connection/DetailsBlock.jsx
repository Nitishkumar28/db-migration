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

const DetailsBlock = ({ db_type, title }) => {
  const { post, data: result, loading: posting, error: postError } = usePost(checkConnectionURL);
  const {connectionDetails} = useDBStore();
  const activeTheme = useUIStore((state) => state.theme);
    const activeConnection = useDBStore(state => {
    if(db_type === "source") {
      return state.selectedSource
    } else if (db_type === "target") {
      return state.selectedTarget
    }
  })
  const activeConnectionDetails = useDBStore(state => {
    if(db_type === "source") {
      return state.selectSourceDetails
    } else if (db_type === "target") {
      return state.selectTargetDetails
    }
  })
    const setConnectionDetails = useDBStore((state) => {
    if(db_type === "source") {
      return state.setSelectedSourceDetails
    } else if (db_type === "target") {
      return state.setSelectedTargetDetails
    }
  });

    const updateConnectionDetails = useDBStore((state) => {
    if(db_type === "source") {
      return state.updateSourceDetails
    } else if (db_type === "target") {
      return state.updateTargetDetails
    }
  });
  
  const handleReset = () => {
    const current = connectionDetails.find(conn => conn.db_type === activeConnection.toLowerCase());
    setConnectionDetails(current || {});
  }


  const handlePost = async () => {
    console.log(activeConnectionDetails)
    if (!activeConnectionDetails) return console.warn("No matching connection found for", db_type);
    try {
      const status = "success" // await post(postData);
      updateConnectionDetails("status", status)
      console.log('Post successful:', status);
    } catch (err) {
      const status = "failed"
      console.error('Post failed:', err.message);
      updateConnectionDetails("status", status)
    }
  };

  return (
    <div
      style={{ borderColor: themePalette[activeTheme].borderPrimary }}
      className={`relative border rounded-lg shadow-md w-[90%] h-[60%] flex flex-col justify-center items-center gap-1 py-3`}>
      <Legend title={title} />
      <div className={`w-full h-fit flex justify-around items-center gap-4 px-[2%]`}>
        <FirstColumn db_type={db_type} />
        <SecondColumn db_type={db_type} />
        <WarningMessages />
      </div>
      <div className="flex justify-center items-center gap-4">
        <BaseButton onClick={() => handlePost()} text={posting ? "checking...": "check connection"} styles="bg-sky-50" />
        <span onClick={() => handleReset()} className="underline underline-offset-2 text-sky-800 font-extralight cursor-pointer capitalize">reset details</span>
      </div>
    </div>
  );
};

export default DetailsBlock;

/*



*/
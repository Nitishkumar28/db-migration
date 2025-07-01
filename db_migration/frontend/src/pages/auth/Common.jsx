import { Link } from "react-router-dom";
import { BaseButton } from "../../base/Base";

export const BasePage = ({ children, ...props }) => {
  return (
    <div className="flex items-center justify-center w-full h-screen bg-blue-0">
      <div className="w-[40%] h-full flex justify-center items-center border-r bg-gradient-to-br from-sky-100 to-sky-200 text-white">
        <div className="space-y-2 text-center animate-slide-in text-sky-700">
          <h1 className="text-4xl font-bold leading-7 tracking-wide">
            Fast & Flexible Migration Tool
          </h1>
          <p className="text-base opacity-90"></p>
          <p className="text-xs opacity-80">
            (Supports PostgreSQL, Oracle, and MySQL)
          </p>
        </div>
      </div>

      <div className="w-[60%] h-full flex justify-center items-center p-8 bg-sky-50">
        <form
          {...props}
          className="w-[60%] min-h-[45%] h-fit p-8 flex flex-col justify-center items-center space-y-4 border border-sky-400 rounded-lg shadow-lg"
        >
          {children}
        </form>
      </div>
    </div>
  );
};

export const AuthHeader = ({ text }) => (
  <h2 className="mb-2 text-2xl font-semibold text-sky-700">{text}</h2>
);

export const InputDiv = ({
  label,
  form,
  field,
  setForm,
  errors,
  type = "text",
}) => {
  return (
    <div className="w-full">
      <label className="block mb-1 text-sm text-sky-700">{label}</label>
      <input
        type={type}
        className="w-full px-3 py-1.5 border border-gray-400 rounded outline-none focus:border-sky-400 focus:ring-blue-300"
        value={form[field] || ""}
        onChange={(e) => setForm({ ...form, [field]: e.target.value })}
      />
      {errors && <p className="mt-1 text-xs text-red-500">{errors}</p>}
    </div>
  );
};

export const StatusMessage = ({ type, message }) => (
  <p
    className={`text-sm text-center ${
      type === "success" ? "text-green-600" : "text-red-600"
    }`}
  >
    {message}
  </p>
);

const NewUserOption = () => {
    return (
        <span className="text-xs text-gray-500">
          New user?{" "}
          <Link
          to="/register"
            className="underline text-sky-600 underline-offset-1 hover:text-sky-700"
          >
            Register
          </Link>
        </span>
    )
}

const AlreadyRegisteredOption = () => {
    return (
        <span className="text-xs text-gray-500">
          Already registered?{" "}
          <Link
          to="/login"
            className="underline text-sky-600 underline-offset-1 hover:text-sky-700"
          >
            Login
          </Link>
        </span>
    )
}

export const AuthFooter = ({ success, type }) => {
  return (
    <div className="flex flex-col items-center justify-center w-full space-y-3">
      <div className={`flex ${type === "register" ? "flex-col-reverse gap-2" : "gap-6"} items-center justify-center w-full`}>
        {type === "login" ? <NewUserOption /> : <AlreadyRegisteredOption />}
        <BaseButton
          type="submit"
          text={type === "login" ? "Login" : "Register"}
          className="px-5 py-2 text-white transition rounded-md bg-sky-600 hover:bg-sky-700"
        />
        {type === "login" && <BaseButton
          type="button"
          text="Forgot Password?"
          className="p-0 text-xs transition text-sky-600 hover:underline underline-offset-2"
        />}
      </div>

      {success && <StatusMessage type="success" message={success} />}
    </div>
  );
};

// export const AuthFooter = ({ success }) => {
//   return (
//     <div className="flex flex-col items-center justify-center w-full space-y-3">
//       <div className="flex items-center justify-between w-full gap-4">
//                 <button
//           type="button"
//           className="text-xs transition text-sky-600 hover:underline underline-offset-2"
//         >
//           New user?
//         </button>
//         <div className="flex-1">
//           <BaseButton
//             type="submit"
//             text="Login"
//             className="w-full px-4 py-2 text-white transition rounded-md bg-sky-600 hover:bg-sky-700"
//           />
//         </div>
//         <button
//           type="button"
//           className="text-xs transition text-sky-600 hover:underline underline-offset-2"
//         >
//           Forgot Password?
//         </button>
//       </div>

//       {success && <StatusMessage type="success" message={success} />}
//     </div>
//   );
// };

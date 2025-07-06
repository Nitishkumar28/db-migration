import { useState } from "react";
import { BaseButton } from "../../base/Base";
import { AuthFooter, AuthHeader, BasePage, InputDiv, StatusMessage } from "./Common";
import { useNavigate } from "react-router-dom";
import { loginAPI } from "../../hooks/urls";
import { usePost } from "../../hooks/usePost";
import useUserStore from "../../store/userStore";

const LoginForm = () => {
  const navigator = useNavigate();
  const { setUserDetails } = useUserStore();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState("");

  const validate = () => {
    const newErrors = {};
    if (!form.email.includes("@")) newErrors.email = "Invalid email";
    if (form.password.length < 6)
      newErrors.password = "Password must be at least 6 characters";
    return newErrors;
  };

  // const handleSubmit = (e) => {
  //   e.preventDefault();
  //   setSuccess("");
  //   const validationErrors = validate();
  //   if (Object.keys(validationErrors).length > 0) {
  //     setErrors(validationErrors);
  //   } else {
  //     setErrors({});
  //     console.log("LOGIN:", form);
  //     setSuccess("Logged in successfully!");
  //     navigator("/home/connections");
  //   }
  // };

const { post, data, loading, error } = usePost(loginAPI());

const handleSubmit = async (e) => {
  e.preventDefault();
  setSuccess("");
  const validationErrors = validate();

  if (Object.keys(validationErrors).length > 0) {
    setErrors(validationErrors);
    return;
  }

  setErrors({});

  try {
    const payload = {
      email: form.email,
      password: form.password
    };

    const result = await post(payload);
    console.log("Server response:", result);

    if (result && result.success) {
      localStorage.setItem("is_logged", "true");
      setUserDetails(result);
      setSuccess("loggedin successfully!");
      navigator("/home/connections");
    } else {
      setErrors({ form: result?.message || "login failed" });
    }
  } catch (err) {
    console.error("Register error:", err);
    setErrors({ form: "Something went wrong. Please try again." });
  }
};

  return (
    <BasePage onSubmit={handleSubmit}>
      {errors && <span className="font-light text-red-500 capitalize">{errors.form}</span>}
      <AuthHeader text="Welcome Back!" />
      <InputDiv
        label="Email"
        form={form}
        field="email"
        setForm={setForm}
        errors={errors.email}
      />
      <InputDiv
        label="Password"
        form={form}
        field="password"
        setForm={setForm}
        errors={errors.password}
        type="password"
      />
      <AuthFooter success={success} type="login" />
    </BasePage>
  );
};

export default LoginForm;

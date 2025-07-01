import { useState } from "react";
import { BaseButton } from "../../base/Base";
import { AuthFooter, AuthHeader, BasePage, InputDiv, StatusMessage } from "./Common";
import { useNavigate } from "react-router-dom";

const LoginForm = () => {
  const navigator = useNavigate();
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

  const handleSubmit = (e) => {
    e.preventDefault();
    setSuccess("");
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
    } else {
      setErrors({});
      console.log("LOGIN:", form);
      setSuccess("Logged in successfully!");
      navigator("/home/connections");
    }
  };

  return (
    <BasePage onSubmit={handleSubmit}>
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

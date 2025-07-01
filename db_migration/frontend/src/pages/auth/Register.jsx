import { useState } from "react";
import { BaseButton } from "../../base/Base";
import { AuthFooter, AuthHeader, BasePage, InputDiv, StatusMessage } from "./Common";
import { useNavigate } from "react-router-dom";

const RegisterForm = () => {
  const navigator = useNavigate();
  const [form, setForm] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState("");

  const validate = () => {
    const newErrors = {};
    if (!form.fullName.trim()) newErrors.fullName = "Full name is required";
    if (!form.email.includes("@")) newErrors.email = "Invalid email";
    if (form.password.length < 6)
      newErrors.password = "Password must be at least 6 characters";
    if (form.password !== form.confirmPassword)
      newErrors.confirmPassword = "Passwords do not match";
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
      console.log("REGISTER:", form);
      setSuccess("Registered successfully!");
      navigator("/home/connections");
    }
  };

  return (
    <BasePage onSubmit={handleSubmit}>
      <AuthHeader text="Create Your Account" />
      <InputDiv
        label="Full Name"
        form={form}
        field="fullName"
        setForm={setForm}
        errors={errors.fullName}
      />
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
      <InputDiv
        label="Re-enter Password"
        form={form}
        field="confirmPassword"
        setForm={setForm}
        errors={errors.confirmPassword}
        type="password"
      />
    <AuthFooter success={success} type="register" />
      {/* <BaseButton
        type="submit"
        text="Register"
        className="rounded-lg px-3 py-2 border border-sky-500 hover:opacity-80 text-[#03729A]"
      />
      {success && <StatusMessage type="success" message={success} />} */}
    </BasePage>
  );
};

export default RegisterForm;

import { useState } from "react";
import { BaseButton } from "../../base/Base";
import { AuthFooter, AuthHeader, BasePage, InputDiv, StatusMessage } from "./Common";
import { useNavigate } from "react-router-dom";
import { registerAPI } from "../../hooks/urls";
import useUserStore from "../../store/userStore";
import { usePost } from "../../hooks/usePost";

const RegisterForm = () => {
  const navigator = useNavigate();
  const { setUserDetails } = useUserStore();
  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState("");

  const validate = () => {
    const newErrors = {};
    if (!form.firstName.trim()) newErrors.firstName = "Firstname is required";
    if (!form.lastName.trim()) newErrors.lastName = "Lastname is required";
    if (!form.email.includes("@")) newErrors.email = "Invalid email";
    if (form.password.length < 6)
      newErrors.password = "Password must be at least 6 characters";
    if (form.password !== form.confirmPassword)
      newErrors.confirmPassword = "Passwords do not match";
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
  //     console.log("REGISTER:", form);
  //     setSuccess("Registered successfully!");
  //     navigator("/home/connections");
  //   }
  // };

const { post, data, loading, error } = usePost(registerAPI());

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
      first_name: form.firstName,
      last_name: form.lastName,
      email: form.email,
      password: form.password,
      confirm_password: form.confirmPassword,
    };

    const result = await post(payload);
    console.log("Server response:", result);

    if (result && result.success) {
      localStorage.setItem("is_logged", "true");
      setUserDetails(result);
      setSuccess("Registered successfully!");
      navigator("/home/connections");
    } else {
      setErrors({ form: result?.message || "Registration failed" });
    }
  } catch (err) {
    console.error("Register error:", err);
    setErrors({ form: "Something went wrong. Please try again." });
  }
};


  return (
    <BasePage onSubmit={handleSubmit}>
      {errors && <span className="font-light text-red-500 capitalize">{errors.form}</span>}
      <AuthHeader text="Create Your Account" />
      <InputDiv
        label="Firstname"
        form={form}
        field="firstName"
        setForm={setForm}
        errors={errors.firstName}
      />
      <InputDiv
        label="Lastname"
        form={form}
        field="lastName"
        setForm={setForm}
        errors={errors.lastName}
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
    </BasePage>
  );
};

export default RegisterForm;

import MainBody from "../components/main/MainBody";
import MainHeaderSection from "../components/main/MainHeaderSection";
import Navbar from "../components/Navbar";

const Home = () => {
  return (
    <div
    style={{backgroundColor: "#F1FAEE", color: "#457B9D", borderColor: "#1D3557"}}
    className="w-full h-screen flex flex-col items-center justify-start gap-4">
      <Navbar />
      <MainBody />
    </div>
  );
};

export default Home;

import MainHeaderSection from "../components/MainHeaderSection";
import Navbar from "../components/Navbar";

const Home = () => {

    return (
        <div className="w-full h-screen flex flex-col items-center justify-start gap-4">
            <Navbar />
            <MainHeaderSection />
            <div className="w-full h-screen flex flex-col items-center justify-start gap-2 px-[1%] pb-[1%]">
                <div className="flex w-full h-full justify-start items-center px-2 gap-2 border border-gray-400">
                    <div className="w-[60%] h-full border-0 text-center">
                        Action Block
                    </div>
                    <div className="w-[40%] h-full border-l border-l-gray-400 text-center">
                        Output Block
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Home;
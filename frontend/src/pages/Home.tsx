import AuthModal from "../components/AuthModal";

function Home() {
    return (
        <div className="relative min-h-screen flex items-center justify-center overflow-hidden bg-[#F4EEE2]">
            <h1 className="text-[20vw] font-bold text-[#8F9E8B] select-none">ANITRACK</h1>
            <AuthModal />
        </div>
    );
};

export default Home; 
import AuthModal from "../components/AuthModal";

function Home() {
    return (
        <div className="relative min-h-screen flex items-center justify-center overflow-hidden bg-white">
            <h1 className="text-[20vw] font-bold text-gray-200 select-none">ANITRACK</h1>
            <AuthModal />
        </div>
    );
};

export default Home; 
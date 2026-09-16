import { useState } from "react";
import RegisterForm from "./RegisterForm";
import LoginForm from "./LoginForm";
import { useNavigate } from "react-router-dom";

function AuthModal() {
    const [view, setView] = useState<'choice' | 'register' | 'login'>('choice');
    const navigate = useNavigate()

    function handleAuthSuccess(data: {access_token: string}) {
        localStorage.setItem('token', data.access_token);
        navigate('/dashboard');
    };

    return (
        <div className="fixed inset-0 bg-stone/25 flex items-center justify-center">
            <div className="bg-[#F4EEE2] rounded-lg p-8 w-96 shadow-xl">
                {view === 'choice' && (
                    <div className="flex flex-col gap-4">
                        <button onClick={() => setView('register')}>Register</button>
                        <button onClick={() => setView('login')}>Login</button>

                    </div>
                )}
                {view === 'register' && <RegisterForm onSuccess={handleAuthSuccess}/>}
                {view === 'login' && <LoginForm onSuccess={handleAuthSuccess}/>}


            </div>
        </div>
    )
};

export default AuthModal;
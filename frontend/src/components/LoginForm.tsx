import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { apiFetch } from "../lib/api";

function LoginForm({onSuccess}: {onSuccess: () => void}) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const mutation = useMutation({
        mutationFn: (data: {email: string; password: string;}) =>
            apiFetch('/auth/login', {
                method: 'POST',
                body: JSON.stringify(data),
            }),
            onSuccess: onSuccess
    })

    function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
        e.preventDefault();
        mutation.mutate({email, password})
    }

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
            />
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            <button>Submit</button>
        </form>
    )
};

export default LoginForm;
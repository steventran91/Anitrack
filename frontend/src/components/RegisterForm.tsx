import {useState} from 'react';
import {useMutation} from '@tanstack/react-query';
import { apiFetch } from '../lib/api';

function RegisterForm({onSuccess}: {onSuccess: () => void}) {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const mutation = useMutation({
        mutationFn: (data: {first_name: string; last_name: string; email: string; password: string;}) =>
            apiFetch('/auth/register', {
                method: 'POST',
                body: JSON.stringify(data),
            }),
        onSuccess: onSuccess
    });

    function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
        e.preventDefault();
        mutation.mutate({first_name: firstName, last_name: lastName, email, password})
    }

    return (
        <form onSubmit={handleSubmit}>
            <input 
                type="text"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                placeholder="First Name"
            />
            <input 
                type="text"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                placeholder="Last Name"
            />
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

export default RegisterForm;
import { useQuery } from '@tanstack/react-query';
import { apiFetch } from '../lib/api';

function Dashboard() {
    const {data, isLoading, isError} = useQuery({
        queryKey: ['dashboard'],
        queryFn: () => apiFetch('/dashboard'),
    })

    if (isLoading) {
        return <div>Loading...</div>
    }
    if (isError) {
        return <div>Something went wrong.</div>
    }

    return (
        <div>
            <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
    )
}

export default Dashboard;


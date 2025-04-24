import axios from 'axios';

const http = axios.create({
    baseUR: import.meta.env.VITE_REQUEST_URL,
    headers: {
        'Content-type': 'application/json',
    }
})

export default http;
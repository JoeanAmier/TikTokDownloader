import './main.css';
import { RouterProvider } from 'react-router-dom';
import httpRouter from './router.tsx';
import ReactDOM from 'react-dom/client';

const rootElement = document.getElementById('root');
if (!rootElement) {
    throw new Error('Failed to find the root element');
}
ReactDOM.createRoot(rootElement).render(
    <RouterProvider router={httpRouter} />
);
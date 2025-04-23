import { createBrowserRouter } from 'react-router-dom';
import MainLayout from '../ui/layouts/MainLayout';

const routes = [
  {
    path: '/',
    element: <MainLayout></MainLayout>,
    loader: () => '메인페이지',
  },
];

const router = createBrowserRouter(routes);

export { router, routes };

import { createBrowerRouter } from 'react-router-dom';

const routes = [
  {
    path: '/',
    element: <MainPage></MainPage>,
    loader: () => '메인페이지',
  },
];

const router = createBrowerRouter(routes);

export { router, routes };

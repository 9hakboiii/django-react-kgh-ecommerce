import { createBrowserRouter } from 'react-router-dom'
import MainLayout from '../ui/layouts/MainLayout'
import Products from '@/ui/components/fruits/products'
import Login from '@/ui/components/login/Login'
import Cart from '@/ui/components/fruits/Cart'

const routes = [
  {
    path: '/',
    element: <MainLayout></MainLayout>,
    loader: () => '메인페이지',
    children: [
      {
        path: '',
        element: <Products></Products>,
        loader: () => '상품들',
      },
      {
        // dev_5_fruit
        path: 'login',
        element: <Login></Login>,
        loader: () => '상품들',
      },
      {
        // dev_7_fruit
        path: 'cart',
        element: <Cart></Cart>,
        loader: () => '카트',
      },
    ],
  },
]

const router = createBrowserRouter(routes)

export { router, routes }

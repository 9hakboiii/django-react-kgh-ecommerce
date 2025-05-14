import { createBrowserRouter } from 'react-router-dom'
import MainLayout from '../ui/layouts/MainLayout'
import Products from '@/ui/components/fruits/products'
import Login from '@/ui/components/login/Login'
import Cart from '@/ui/components/fruits/Cart'
import Hero from '@/ui/components/Hero'
import CheckOut from '@/ui/components/fruits/CheckOut'
import { Shop } from '@/ui/components/fruits/Shop'

const routes = [
  {
    path: '/',
    element: <MainLayout></MainLayout>,
    loader: () => '메인페이지',
    children: [
      {
        path: '',
        element: (
          <div>
            <Hero />
            <Products></Products>
          </div>
        ),
        loader: () => '상품들',
      },
      {
        // dev_5_fruit
        path: 'login',
        element: (
          <div>
            <Hero />
            <Login></Login>
          </div>
        ),
        loader: () => '상품들',
      },
      {
        // dev_7_fruit
        path: 'cart',
        element: <Cart></Cart>,
        loader: () => '카트',
      },
      {
        // dev_8_fruit
        path: 'checkout',
        element: <CheckOut></CheckOut>,
        loader: () => '결제',
      },
      {
        // dev_10_fruit
        path: 'shop',
        element: <Shop></Shop>,
        loader: () => '샵',
      },
    ],
  },
]

const router = createBrowserRouter(routes)

export { router, routes }

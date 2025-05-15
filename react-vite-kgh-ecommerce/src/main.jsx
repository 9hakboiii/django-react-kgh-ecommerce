import { createRoot } from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'
import { router } from './router/Router.jsx'
import { AuthProvider } from './contexts/AuthContext.jsx'
import { CartProvider } from './contexts/CartContext.jsx'
import { ShopProvider } from './contexts/ShopContext.jsx'

// dev_1_fruit
createRoot(document.getElementById('root')).render(
  // dev_5_fruit
  // dev_10_fruit
  <AuthProvider>
    <ShopProvider>
      <CartProvider>
        <RouterProvider router={router} />,
      </CartProvider>
    </ShopProvider>
  </AuthProvider>,
)

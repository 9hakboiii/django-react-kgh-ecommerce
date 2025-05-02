import { createRoot } from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import { router } from './router/Router.jsx';
import { AuthProvider } from './contexts/AuthContext.jsx';

// dev_1_fruit
createRoot(document.getElementById('root')).render(
  // dev_5_fruit
  <AuthProvider>
    <RouterProvider router={router} />,
  </AuthProvider>,
);

import { createContext, useContext, useState } from 'react';
import { loginUser } from '@/ui/api/AuthApi';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const login = async (username, password) => {
    try {
      const response = await loginUser(username, password);
    } catch (error) {
      console.error('로그인 실패', error);
      throw error;
    }
  };
};

import { createContext, useContext, useState } from 'react';
import { loginUser } from '@/ui/api/AuthApi';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(localStorage.getItem('access'));

  const login = async (username, password) => {
    try {
      const response = await loginUser(username, password);
      const { access, refresh } = response.data;

      // 저장 영역은 크게 4가지로 나뉜다.
      // 1. local storage : 브라우저를 닫아도 데이터가 남아있음. (영구적) > 현업에선 local storage를 많이 사용함.
      //    - local storage는 보안에 취약하기 때문에 민감한 데이터는 저장하지 않는 것이 좋음.
      //    - local storage는 도메인 단위로 저장되기 때문에, 같은 도메인에서만 접근 가능함.
      // 2. session storage : 브라우저를 닫으면 데이터가 사라짐. (임시적)
      // 3. cookie : 서버와 클라이언트가 공유하는 데이터. (영구적)
      // 4. memory : 메모리에 저장되는 데이터. (임시적)
      localStorage.setItem('access', access);
      localStorage.setItem('refresh', refresh);
      setAccessToken(access); // 메모리에 access toeken을 저장함

      // 로그인이 된 후 로그인 정보를 받아서 어디서든 로그인 정보를 공유할 수 있게 함
      await getUser();
    } catch (error) {
      console.error('로그인 실패', error);
      throw error;
    }
  };

  const getUser = async () => {
    try {
      const response = await getCurrentUser();
      setUser(response.data);
      console.log(response.data);
    } catch (error) {
      console.errer('사용자 정보 받아오기 실패', error);
      logout();
    }
  };

  // 로그아웃시 로컬에 저장된 access token과 refresh token을 삭제함
  const logout = () => {
    setUser(null);
    setAccessToken(null);
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
  };

  // 자식에게 전달할 값
  const value = {
    logout,
    login,
    accessToken,
    user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

import axios from 'axios';

const accessToken = localStorage.getItem('access');

//dev_5_Fruit
const http = axios.create({
  baseURL: import.meta.env.VITE_REQUEST_URL,
  headers: {
    Authorization: accessToken ? `Bearer ${accessToken}` : undefined,
  },
});

/*
우선 로그인 시에 동작하는 flow를 정리하자면,
1. 새로고침 시에도 로그인 상태가 유지되어야 한다.
2. access token이 만료되면 refresh token을 통해서 재발행 받아야 한다.
3. refresh token이 만료되었다면 로그아웃 되어야 한다.
4. 로그아웃 시에는 access token과 refresh token이 삭제되어야 한다.
5. 로그인 시에는 access token과 refresh token이 저장되어야 한다.
6. 로그인 상태를 확인할 수 있는 함수가 필요하다.
위의 flow를 구현하기 위해서는 axios의 interceptor를 사용하면 된다.
axios의 interceptor를 사용하면 요청이나 응답을 가로채서 처리할 수 있다.
아래는 axios의 interceptor를 사용한 코드이다.
*/

//요청 인터셉터 – 요청마다 access token 넣기
http.interceptors.request.use(
  (config) => {
    const access = localStorage.getItem('access');
    if (access) {
      config.headers['Authorization'] = `Bearer ${access}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// access 토큰 만료 및 재시도하지 않은 경우
//🧩 1. error.response?.status === 401
//설명: axios 요청이 실패했을 때 서버가 401 Unauthorized 상태 코드를 응답했는지 확인하는 조건
//이건 일반적으로 access token이 만료되었거나, 인증 정보가 누락되었을 때 발생
//토큰이 만료된 경우
//토큰이 없거나 잘못된 경우
//🧩 2. !originalRequest._retry
//설명: axios는 실패한 요청 객체(originalRequest)를 그대로 다시 보내서 재시도 할 수 있음.
//근데 이걸 한 번만 재시도하게 하기 위해 _retry라는 커스텀 플래그.
//!originalRequest._retry는 → originalRequest._retry가 아직 true가 아니라는 뜻.
// 즉, 이 요청은 아직 재시도하지 않았다는 의미.
//만약 _retry가 true면 → 이미 refresh 해서 다시 보낸 요청이라는 뜻이므로 무한 루프를 막기 위해 다시 안 보냄.
//결론
//"서버가 401을 반환했고, 이 요청은 아직 재시도되지 않았다면, 토큰을 갱신하고 다시 요청해라!"

// 응답 인터셉터 – access token 만료 시 자동으로 refresh 요청
http.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refresh = localStorage.getItem('refresh');
        const res = await axios.post('http://127.0.0.1:8000/api/auth/jwt/refresh/', {
          refresh: refresh,
        });

        const newAccess = res.data.access;
        localStorage.setItem('access', newAccess);

        // Authorization 헤더 업데이트 후 원래 요청 다시 시도
        originalRequest.headers['Authorization'] = `Bearer ${newAccess}`;
        return http(originalRequest);
      } catch (refreshError) {
        console.error('🔒 토큰 갱신 실패', refreshError);
        // 실패하면 로그인 상태 초기화 로직 추가 가능
      }
    }

    return Promise.reject(error);
  },
);

export default http;

import { useEffect, useState } from 'react'
import '/src/assets/login/css/login.css'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'

// dev_5_fruit
const Login = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const { login } = useAuth() // AuthContext에서 auth 객체를 가져옵니다.

  const handleLogin = async (event) => {
    event.preventDefault()

    try {
      // 동기 통신
      await login(username, password)
      alert('✅ 로그인 성공')
      // 로그인 성공 후 루트로 이동
      navigate('/') // windows.location.href = '/';
    } catch (error) {
      alert('로그인 실패' + error.message)
    }
  }

  //dev_9_1_Fruit
  useEffect(() => {
    // Kakao SDK 초기화
    if (window.Kakao && !window.Kakao.isInitialized()) {
      window.Kakao.init(import.meta.env.VITE_KAKAO_JAVASCRIPT_KEY)
    }
  }, [])

  const handleKakaoLogin = () => {
    if (!window.Kakao) {
      console.log('카카오 모듈이 없습니다 ...')
      return
    }
    //카카오 인증
    window.Kakao.Auth.login({
      scope: 'profile_nickname, account_email, gender', // 원하는 scope
      success: async function (authObj) {
        const kakaoAccessToken = authObj.access_token

        console.log('Kakao Access Token:', kakaoAccessToken)
      },
    })
  }

  return (
    <div className="form-bg">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-4 col-md-offset-4">
            <div className="form-container">
              {/* dev_9_1_Fruit */}
              <div className="form-icon" onClick={handleKakaoLogin}>
                <i className="fa fa-user" />
              </div>
              <h3 className="title">Login</h3>
              <form className="form-horizontal">
                <div className="form-group">
                  <label>username</label>
                  <input
                    className="form-control"
                    type="text"
                    placeholder="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                  />
                </div>
                <div className="form-group">
                  <label>password</label>
                  <input
                    className="form-control"
                    type="password"
                    placeholder="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>
                <button type="button" className="btn btn-default" onClick={handleLogin}>
                  Login
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login

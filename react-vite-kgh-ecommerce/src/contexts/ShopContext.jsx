import { getProductsPaging } from '@/api/ProductApi'
import { createContext, useContext, useState, useEffect } from 'react'

const ShopContext = createContext()

// 외부에서 context를 사용할 수 있도록 만듦
export const useShop = () => useContext(ShopContext)

export const ShopProvider = ({ children }) => {
  const [currentPage, setCurrentPage] = useState(1)
  const [products, setProducts] = useState([])
  const [search, setSearch] = useState('')
  const [ordering, setOrdering] = useState('')

  // 상품 목록 호출
  const fetchProducts = async () => {
    try {
      const response = await getProductsPaging({
        page: currentPage,
        search, // ES6 이후부터 key:value의 이름이 같으면, key만 입력해도 됨
        ordering,
      })
      console.log(response.data)
      setProducts(response.data.results)
    } catch (error) {
      console.error('상품 목록을 불러오는 중 오류 발생:', error)
    }
  }

  // 조건이 변경될때 마다 API 다시 호출
  useEffect(() => {
    fetchProducts()
  }, [currentPage, search, ordering])

  const value = {
    search,
    setSearch,
    currentPage,
    setCurrentPage,
    products,
    setProducts,
    setOrdering,
  }

  return <ShopContext.Provider value={value}>{children}</ShopContext.Provider>
}

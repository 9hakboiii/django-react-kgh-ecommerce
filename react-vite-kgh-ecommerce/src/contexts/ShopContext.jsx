import { getProducts, getProductsPaging } from '@/api/ProductApi'
import { createContext, useContext, useEffect, useState } from 'react'

//dev_10_Fruit
const ShopContext = createContext()

export const useShop = () => useContext(ShopContext)

export const ShopProvider = ({ children }) => {
  const [currentPage, setCurrentPage] = useState(1)
  const [products, setProducts] = useState([])
  const [search, setSearch] = useState('')
  const [ordering, setOdering] = useState('')

  const [category, setCategory] = useState('')

  // {
  //   "count": 21,
  //   "next": "http://127.0.0.1:8000/api/product-list/?ordering=-price&page=2",
  //   "previous": null,
  //   "results": [
  //       {
  //           "id": 8,
  //           "category": {
  //               "id": 4,
  //               "name": "도서"
  //           },
  //           "name": "역사",
  //           "price": "199.94",
  //           "description": "역사는(은) 도서 카테고리에 속하는 상품입니다.",
  //           "image": "http://127.0.0.1:8000/media/upload/product/%EC%97%AD%EC%82%AC_rpRPjCl.jpg",
  //           "is_sale": false,
  //           "sale_price": null
  //       },

  //상품 목록 호출
  const fetchProducsts = async () => {
    try {
      const resonse = await getProductsPaging({
        page: currentPage,
        search,
        ordering,
        category,
      })
      console.log(resonse.data)
      setProducts(resonse.data.results)
    } catch (error) {
      console.error('상품 목록을 불러오는 중 오류 발생:', error)
    }
  }

  //조건이 변경될때 마다 API 다시 호출
  useEffect(() => {
    fetchProducsts()
  }, [currentPage, search, ordering, category])

  const value = {
    search,
    setSearch,
    currentPage,
    setCurrentPage,
    products,
    setProducts,
    ordering,
    setOdering,
    category,
    setCategory,
  }

  return <ShopContext.Provider value={value}>{children}</ShopContext.Provider>
}

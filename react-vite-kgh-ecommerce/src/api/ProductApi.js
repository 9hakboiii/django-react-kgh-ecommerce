import http from './HttpCommon'

//http://127.0.0.1:8000/api/categories/
export const getProducts = () => {
  return http.get('/api/products/')
}

export const getProductsPaging = ({ page = 1, search = '' }) => {
  const params = { page, search }

  // api/product-list/?page=1&search='paraps'
  return http.get('/api/product-list/', { params })
}

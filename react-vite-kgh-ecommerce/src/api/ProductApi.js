import http from './HttpCommon'

//http://127.0.0.1:8000/api/categories/
export const getProducts = () => {
  return http.get('/api/products/')
}

export const getProductsPaging = ({ page = 1, search = '', page_size = 12, ordering = '' }) => {
  const params = { page, search, page_size, ordering }

  // api/product-list/?page=1&search='paraps'&ordering=-id
  return http.get('/api/product-list/', { params })
}

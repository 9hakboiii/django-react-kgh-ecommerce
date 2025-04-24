import http from './HttpCommon';

//http://127.0.0.1:8000/api/categories/
export const getCategories = () => {
  return http.get('/api/categories/');
};
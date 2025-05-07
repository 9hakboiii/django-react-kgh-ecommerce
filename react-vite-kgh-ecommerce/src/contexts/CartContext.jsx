import React, { createContext, useContext, useEffect, useState } from 'react'
import { useAuth } from './AuthContext'

const CartContext = createContext()

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState({})
  const { user } = useAuth()

  // 비회원일 때 localStorage 저장
  useEffect(() => {
    if (!user) {
      localStorage.setItem('cart', JSON.stringify(cartItems))
      console.log('🛒 savedCart:', localStorage.getItem('cart'))
    }
  }, [cartItems, user])

  const getTotalItems = () => {
    // 방법 1: for문을 사용하여 장바구니에 담긴 상품의 총 개수를 계산
    // keys, values, entries, assign, hasOwnPropert
    // let total = 0;
    // const items = Object.values(cartItems); // 상품 객체들을 배열로 가져옴

    // for (let i = 0; i < items.length; i++) {
    //   total += items[i].quantity; // 각 상품의 수량을 누적
    // }

    // 방법 2
    // Object.values(cartItems)로 cartItems 객체의 값만 추출하여 배열로 변환 (js에서 Object.values() 메서드 사용)
    // reduce() 메서드를 사용하여 배열의 각 요소를 누적하여 총 개수를 계산
    return Object.values(cartItems).reduce((acc, item) => acc + item.quantity, 0)
  }

  // 장바구니 추가
  const addToCart = async (product, quantity = 1) => {
    const productId = product.id
    const price = product.price

    if (user) {
      try {
      } catch (err) {
        console.error('서버 장바구니 추가 실패', err)
      }
    } else {
      setCartItems((prev) => {
        const existing = prev[productId]
        return {
          ...prev,
          [productId]: {
            price,
            quantity: existing ? existing.quantity + quantity : quantity,
          },
        }
      })
    }
  }

  return (
    <CartContext.Provider
      value={{
        cartItems,
        addToCart,
        getTotalItems,
      }}
    >
      {children}
    </CartContext.Provider>
  )
}

export const useCart = () => useContext(CartContext)

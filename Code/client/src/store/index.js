// store/index.js

import { createStore } from 'vuex';
import { authenticate, register } from '@/api';
import { isValidJwt } from '@/utils';
import jwt from 'jsonwebtoken-promisified';
import { reactive } from 'vue';


const state = {
  user: {},
  jwt: '',
  categoryCatalog: {},
  productCatalog: {},
  smProductCatalog: reactive([]),
  cartProducts: reactive([]),
  cartProductsFiltered: reactive([]),
  totalQuantity: reactive(0),
};

const actions = {
  login(context, userData) {
    console.log("Calling setUserData");
    context.commit('setUserData', { userData });
    console.log("Calling authenticate");
    return authenticate(userData)
      .then((response) => {
        console.log("calling setJwtToken")
        context.commit('setJwtToken', { jwt: response.data });
        return response;
      })
      .catch((error) => {
        console.log('Error Authenticating: ', error);
        throw error;
      });
  },
  register(context, userData) {
    context.commit('setUserData', { userData });
    return register(userData)
      .then(() => context.dispatch('login', { userData }))
      .catch((error) => {
        console.log('Error Registering: ', error);
      });
  },

  logout({ commit }) {
    
    commit('setUserData', { userData: {} });
    commit('setRole', '');
    commit('setUserId', '');
    
    localStorage.clear();
    
  },

  async fetchCategoryCatalog({ commit }) { 
    try {
      //Fetching all categories
      const response1 = await fetch('http://localhost:7000/api/category');
      const catalogData = await response1.json();
      commit('setCategoryCatalog', catalogData);
    } catch (error) {
      console.error('Error fetching category catalog:', error);
    }
  },
  async fetchProductCatalog({ commit }) {
    try {
      const response1 = await fetch('http://localhost:7000/api/catalog');
      const catalogData = await response1.json();
      commit('setProductCatalog', catalogData);
    } catch (error) {
      console.error('Error fetching product catalog:', error);
    }
  },
  async fetchStoreManagerProductCatalog({ commit }) {
    try {
      const token = localStorage.getItem('gurukrupaAppToken');
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      };
        const response = await fetch(`http://localhost:7000/api/storemanager/${localStorage.getItem('managerId')}/products`, {
        method: 'GET',
        headers: headers,
      });
      
      if (response.ok) {
        const catalogData = await response.json();
        commit('setStoreManagerProductCatalog', catalogData);
      } else {
        console.error('Error fetching product catalog. Status:', response.status);
      }
    } catch (error) {
      console.error('Error fetching product catalog:', error);
    }
  },
  async fetchStoreManagerCategoryCatalog({ commit }) {
    try {
      const token = localStorage.getItem('gurukrupaAppToken');
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      };
      const response = await fetch(`http://localhost:7000/api/storemanager/${localStorage.getItem('managerId')}/categories`, {
        method: 'GET',
        headers: headers,
      });

      if (response.ok) {
        const catalogData = await response.json();
        commit('setStoreManagerCategoryCatalog', catalogData);
      } else {
        console.error('Error fetching category catalog. Status:', response.status);
      }
    } catch (error) {
      console.error('Error fetching category catalog:', error);
    }
  },
  
  async filterProducts({ commit, dispatch, state }, filterParams) {
    console.log('filterParams', filterParams);
    const { categoryId, filterString,minPrice,maxPrice } = filterParams;
    console.log('filterString', filterString);
    if (!state.productCatalog || Object.keys(state.productCatalog).length === 0) {
      console.error('Product catalog not loaded');
      await dispatch('fetchProductCatalog');
      console.log('After fetchProductCatalog', Object.keys(state.productCatalog).length);
    } else {
      console.log('state productCatalog', state.productCatalog);
    }

   /* if (!filterString) {
      console.log("!filterString")
      return state.productCatalog;
    }*/

    const filteredProducts = {};

 
    for (const [category, products] of Object.entries(state.productCatalog)) {
      console.log('filtering state.productCatalog:', state.productCatalog);
      console.log(minPrice);
      console.log(maxPrice);
      const filteredCategoryProducts = products.filter(
        (product) =>
          (filterString === "" || product.name.toLowerCase().startsWith(filterString.toLowerCase())) &&
          (categoryId === 0 || product.categoryid === categoryId) &&
          (minPrice === 0 || parseFloat(product.discounted_price) >= minPrice)  &&
          (maxPrice === 0 || parseFloat(product.discounted_price) <= maxPrice)
      );

      // Add the category to the filteredProducts only if there are matching products
      if (filteredCategoryProducts.length > 0) {
        console.log('filtering filteredCategoryProducts.length', filteredCategoryProducts.length);
        filteredProducts[category] = filteredCategoryProducts;
      }
    }
    
    console.log('filteredProducts', filteredProducts);
    // Commit the mutation to set filtered products in the state
    commit('setFilteredProducts', filteredProducts);
  },
};

const mutations = {
  setUserData(state, payload) {
    state.user.userData = payload.userData;
  },
  setRole(state, role) {
    state.user.role = role;
    if (role === 'ADMIN') {
      localStorage.setItem('isAdmin', true);
      localStorage.setItem('isStoreManager', true);
      localStorage.setItem('isUser', true);
    } else if (role === 'STORE_MANAGER') {
      localStorage.setItem('isAdmin', false);
      localStorage.setItem('isStoreManager', true);
      localStorage.setItem('isUser', true);
    } else {
      localStorage.setItem('isAdmin', false);
      localStorage.setItem('isStoreManager', false);
      localStorage.setItem('isUser', true);
    }
  },
  setUserId(state, userId){ 
    state.user.userId = userId;
  },
  async setJwtToken(state, payload) {
    try {
      console.log("About to decode in setJwtToken", payload.jwt.token)
      
      const decodedToken = await jwt.verify(payload.jwt.token, 'Gurukrupa');
      console.log("Decoded Token", decodedToken);
      console.log("role", decodedToken.role);
      console.log("userid", decodedToken.sub);
      localStorage.setItem('userrole', decodedToken.role);
      
      localStorage.setItem('userId', decodedToken.sub);
      this.commit('setUserId', decodedToken.sub);
      localStorage.setItem('gurukrupaAppToken', payload.jwt.token);
      state.jwt = payload.jwt;

      localStorage.setItem('managerId', payload.jwt.user_info.manager_id);
      this.commit('setRole', payload.jwt.user_info.role );

    } catch (error) {
      console.error('Error decoding JWT token:', error);
      throw error; // Rethrow the error to be caught by the calling code if needed
    }
  },
  setProductCatalog(state, catalog) {
    state.productCatalog = catalog;
  },
  setStoreManagerProductCatalog(state, catalog) {
    state.smProductCatalog = catalog;
  },
  setStoreManagerCategoryCatalog(state, catalog) {
    state.smCategoryCatalog = catalog;
  },
  setCategoryCatalog(state, catalog) { 
    state.categoryCatalog = catalog;
  },
  // Add a new mutation to set filtered products
  setFilteredProducts(state, filteredProducts) {
    const flattenedProducts = Object.values(filteredProducts).flat();
    state.cartProductsFiltered = flattenedProducts;
  },
  /*filterCartProducts(state) { 
    const cartItems = localStorage.getItem('cartItems');
    state.cartProductsFiltered = cartItems ? JSON.parse(cartItems) : [];
    
    state.cartProductsFiltered.push({ ...product, quantity: 1 });
  },*/
  // Add a new mutation to load cart items from localStorage
  loadCartFromLocalStorage(state) {
    const cartItems = localStorage.getItem('cartItems');
    state.cartProducts = cartItems ? JSON.parse(cartItems) : [];
    this.commit('computeTotalQuantity');
  },

  changeItemQuantity(state, params) {
    const product = params.product;
    const type = params.type;

    const cartItems = localStorage.getItem('cartItems');
    state.cartProducts = cartItems ? JSON.parse(cartItems) : [];

    const index = state.cartProducts.findIndex((item) => item.id === product.id);

    if (index !== -1) {
      // Create a new object to avoid mutating the original product directly
      const updatedProduct = { ...state.cartProducts[index] };

      // Update the quantity based on the 'type'
      updatedProduct.quantity += type === 'add' ? 1 : -1;

      // Remove the item if the quantity is 0 after decrementing
      if (type === 'remove' && updatedProduct.quantity === 0) {
        state.cartProducts.splice(index, 1); // Remove the item from the array
      } else {
      // Update the product in the array
        state.cartProducts[index] = updatedProduct;
      }
      // Update localStorage
      localStorage.setItem('cartItems', JSON.stringify(state.cartProducts));
    }
    this.commit('computeTotalQuantity');
  },

  removeItemFromCart(state, product) {
    //const product=param.product
    const cartItems = localStorage.getItem('cartItems');
    state.cartProducts = cartItems ? JSON.parse(cartItems) : [];
    const index = state.cartProducts.findIndex((item) => item.id === product.id);
    console.log('remove index', index)
    state.cartProducts.splice(index, 1);
    localStorage.setItem('cartItems', JSON.stringify(state.cartProducts));
    this.commit('computeTotalQuantity');
  },

  // Update the existing mutation to also save cart items to localStorage
  addToCart(state, product) {
    const checkProduct = state.cartProducts.find((productCar) => product.id === productCar.id);

    if (checkProduct) {
      checkProduct.quantity++;
    } else {
      state.cartProducts.push({ ...product, quantity: 1 });
    }
    localStorage.setItem('cartItems', JSON.stringify(state.cartProducts));
    this.commit('computeTotalQuantity');
  },
  computeTotalQuantity(state) {
    // Ensure that state.cartProducts is initialized as reactive
    
    // Calculate the total quantity of items in the cart
    state.totalQuantity = state.cartProducts.reduce((total, product) => total + product.quantity, 0);
    console.log('Computed totalQuantity',state.totalQuantity)
  }
};

 const getters = {
  isAuthenticated(state) {
    return isValidJwt(state.jwt.token);
  },
  getProductCatalog: (state) => state.productCatalog,
  getStoreManagerProductCatalog: (state) => state.smProductCatalog,
  getStoreManagerCategoryCatalog: (state) => state.smCategoryCatalog,
  getCategoryCatalog: (state) => state.categoryCatalog,
  getTotalQuantity: (state) =>state.totalQuantity,
};

export default createStore({
  state,
  actions,
  mutations,
  getters,
});
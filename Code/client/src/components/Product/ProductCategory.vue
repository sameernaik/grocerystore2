//ProductCategory.vue
<template>
  <div class="container mt-4">
      <div v-if="buyAgainProductsListLoaded && buyAgainProductsList && buyAgainProductsList.length > 0">
        <h2 style="color: #E91E63;margin-bottom:16px;">Buy Again</h2>
        <div class="row">
        <!-- Iterate through each product in the productCatalog list -->
        <div class="col-md-3" v-for="product in buyAgainProductsList" :key="product.id">
          <!-- Display the ProductCategoryItem component for each product -->
          <ProductCategoryItem
            :key="product.id"
            :productName="product.name"
            :productPrice="product.price"
            :productDesc="product.description"
            :productImg="product.imagename"
            :productDiscount="product.discount"
            :available="product.available"
            :stock_quantity="product.stock_quantity"
            @add-to-cart="() => onAddToCart(product)"
          />
        </div>
        </div>
      </div>
      
      <!--{{ {{ console.log(productCatalog) }}-->
      <div v-for="(products, category) in productCatalog" :key="category">
        <h2 style="color: #E91E63;margin-bottom:16px;">{{ getCategoryName(category) }}</h2>
        
         <!--{{ console.log("(productCatalog[category])",productCatalog[category]) }}-->
         <div class="row">
          <div class="col-md-3" v-for="product in products" :key="product.id">
          <!--{{ console.log("product.imagename",product.imagename) }}-->
            <ProductCategoryItem
          :key="product.id"
          :productName="product.name"
          :productPrice="product.price"
          :productDesc="product.description"
          :productImg="product.imagename"
          :productDiscount="product.discount"
          :available="product.available"
          :stock_quantity="product.stock_quantity"
          @add-to-cart="() =>onAddToCart(product)"
        />
        
            
          </div>
          </div>
        
      </div>
    </div>
  
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import ProductCategoryItem from './ProductCategoryItem.vue';
import axios from 'axios';
//import products from '@/store/app';
//const products1 = products.value;
const store = useStore();
const productCatalog = ref([]);
const categoryCatalog = ref([]);
//Add one more productCatalog for storing filtering results.
const productCatalogLoaded = ref(false);
const buyAgainProductsList = ref([]);
//Add one more productCatalog for storing filtering results.
const buyAgainProductsListLoaded = ref(false);

// Function to handle adding products to the cart
const onAddToCart = (product) => {
  console.log('Parent onAddToCart',product);
  store.commit('addToCart', { ...product });
 };

onMounted(async () => {
  // Fetch the product catalog when the component is mounted
  await store.dispatch('fetchProductCatalog');
  productCatalog.value = store.getters.getProductCatalog;
  store.commit('loadCartFromLocalStorage');
  //console.log('onMounted',productCatalog.value )
  await store.dispatch('fetchCategoryCatalog');
  categoryCatalog.value = store.getters.getCategoryCatalog;
  productCatalogLoaded.value = true;
  fetchBuyAgain();
});
const getCategoryName = (categoryid) => {
  
  for (const category of categoryCatalog.value) {
    
    if (category.id === parseInt(categoryid,10)) {
      return category.name;
    }
  }
  // Return a default value or handle the case when no match is found
  return "Unknown Category";
};
const fetchBuyAgain=(async () => {
  const jwtToken = localStorage.getItem('gurukrupaAppToken');
  if (jwtToken)
  {
    try {


      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${jwtToken}`,
      };

      const response = await axios.get(`http://localhost:7000/api/buy-again`, { headers });
      buyAgainProductsList.value = response.data;
    } catch (error) {
      console.error('Error fetching buy again data:', error);
    }

    console.log('buyAgain ', buyAgainProductsList.value);
    buyAgainProductsListLoaded.value = true;
  }
});
</script>

<style>
h1 {
  text-align: center;
  margin-bottom: 35px;
}

.main-container {
  align-items: center;
  display: flex;
  flex-direction: column;
}


</style>
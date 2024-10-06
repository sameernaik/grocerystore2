<template>
  <div>
    <h5 style="margin-top: 50px; text-align: center; color: #E91E63;">{{ heading }}</h5>

    <div class="container mt-5 mb-5">
      <div class="d-flex justify-content-center row">
        <div v-if="products.length === 0" class="col-md-12">
            <h3 style="text-align: center; color: #E91E63;">No search results found. Try modifying search query </h3>
        </div>
        <div v-else class="col-md-10" v-for="product in products" :key="product.id">
          <div class="row p-2 bg-white border rounded mt-2">
            <div class="col-md-3 mt-1">
              <router-link :to="'/product-detail/' + product.id">
                <img
                  id="productImage"
                  :src="getImageSource(product)"
                  @error="setDefaultImage"
                  alt="Image not available"
                  class="card-img-top"
                />
              </router-link>
            </div>

            <div class="col-md-6 mt-1">
              <h5>{{ product.name }}</h5>
              <div class="d-flex flex-row"></div>
              <div class="mt-1 mb-1 spec-1">
                <span>{{ product.sell_quantity }}&nbsp;{{ product.sell_unit }}</span
                ><span class="dot"></span>
                <span><br /><br />{{ product.description }}</span
                ><span class="dot"></span><span><br /></span>
              </div>
              <div v-if="product.manufacturingdate !== null" class="mt-3 mb-2 spec-2">
                <span>Mfg Date: {{ product.manufacturingdate }}</span>
              </div>
              <p class="text-justify text-truncate para mb-0">Exp Date: {{ product.expirydate }}<br /><br /></p>
            </div>

            <div class="align-items-center align-content-center col-md-3 border-left mt-1">
              <div class="d-flex flex-row align-items-center">
                <p
                  class="mr-1"
                  style="font-size: 25px; font-weight: bold ;"
                >
                  Rs {{ parseFloat(product.discounted_price).toFixed(2) }}
                </p>
                <span
                  class="strike-text"
                  style="margin-left: 10px; color: red; text-decoration: line-through"
                >
                  Rs {{ product.price }}
                </span>
              </div>

              <div class="d-flex flex-column mt-4">
                <!-- <router-link
                  v-if="product.available === 1 && product.stock_quantity > 0"
                  :to="'/product-detail/' + product.id"
                  style="margin-top: 50px;"
                  class="btn btn-block btn-primary"
                  @click="addToCart(product)"
                >
                  Add to Cart
                </router-link>-->

                <a
                  v-if="product.available === 1 && product.stock_quantity > 0"
                  @click="addToCart(product)"
                  style="background-color: #E91E63;margin-bottom:10px;"
                  class="btn btn-block btn-primary"
                  >
                  Add to Cart
                </a>

                <h6 v-else style="text-align: left; margin-top: 1px; color: #E91E63">
                  CURRENTLY UNAVAILABLE
                </h6>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';

import { useToast } from "vue-toastification";
const toast = useToast();
const customOptions = {
  position: 'top-right',
  timeout: 2000,
  closeOnClick: true,
  pauseOnHover: true,
  
};

const store = useStore();

const heading = ref(''); // Set the actual data
const products = ref([]); // Set the actual data

const setDefaultImage = (event) => {
  event.target.src = '@/assets/img/unavailable_image_product.jpg';
};

const getImageSource = (product) => {
  if (product && product.imagename) {
    try {
      return require(`@/assets/img/${product.imagename}.jpg`);
    } catch (error) {
      console.error(`Error loading image for product ${product.id}: ${error.message}`);
    }
  }
  return require('@/assets/img/unavailable_image_product.jpg');
};
const addToCart = (product) => {
 // emit("add-to-cart", product)
  console.log('Product added to cart:',  { ...product });
  store.commit('addToCart', { ...product });
  toast.info(product.name + ' added to cart', customOptions);
};
onMounted(() => {
    console.log('SearchResultPanel  onMounted called ');
    products.value = [...store.state.cartProductsFiltered];
    console.log('SearchResultPanel  onMounted complete ',products.value );
    
});
</script>

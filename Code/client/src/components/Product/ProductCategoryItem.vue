<!--ProductCategoryItem-->
<template>
  <div class="card">
    <div class="card-badge">
      <div class="card-badge-container">
        <span v-if="card.productDiscount>0" class="badge badge-primary">{{ card.productDiscount }}% OFF</span>
      </div>
      <img :src="getImageSource()" class="card-img-top" alt="Product Image" style="width: 210px; height: 210px; align: center;" @error="handleImageError">
    </div>
    <div class="card-body" style="background-color: #fce2ed;">
      <h5 class="card-title">{{ card.productName }}</h5>
      <p class="card-text">{{ card.productDesc }}</p>
      <p class="card-text" v-if="card.productPrice !== null"><strong>Price:</strong> Rs {{ card.productPrice.toFixed(2) }}</p>
      <p class="card-text" v-if="card.productPrice !== null && card.productDiscount > 0" ><strong>Discounted Price:</strong> Rs {{ (card.productPrice*(1- card.productDiscount/100)).toFixed(2) }}</p>
      <button v-if="card.available === 1 && card.stock_quantity > 0" style="background-color: #E91E63;" class="btn btn-primary" @click="addToCart">Add to Cart</button>
      <h6 v-else style="text-align: left; margin-top: 1px; color: #E91E63">
      CURRENTLY UNAVAILABLE
      </h6>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import { useToast } from "vue-toastification";
const toast = useToast();
const customOptions = {
  position: 'top-right',
  timeout: 1000,
  closeOnClick: true,
  pauseOnHover: true,
  // Add any other custom options you need
};
const emit = defineEmits(["add-to-cart"])

const card = defineProps({
  productName: String,
  productPrice: Number,
  productDesc: String,
  productImg: String,
  available: Number,
  productDiscount:Number,
  stock_quantity: Number,

});


const addToCart = () => {
  emit("add-to-cart", card)
  console.log('Product added to cart:', { ...card });
  toast.info(card.productName+' added to cart', customOptions );
};

const getImageSource = () => {
  if (card && card.productImg) {
    try {
      return require(`@/assets/img/${card.productImg}.jpg`);
    } catch (error) { 
      console.error(`Error loading image for product`);
    }
  }
  return require('@/assets/img/unavailable_image_product.jpg');
};
const handleImageError = (product) => {
  console.error(`Error loading image for product`);
  product.imageSource = require('@/assets/img/unavailable_image_product.jpg');
};

</script>

<style scoped>
.card {
  width: 16rem;
  
  margin-bottom: 100px;
}

.badge-primary {
  background: #E91E63 !important;
}

.badge {
  padding: 0.7em 0.7em;
}
</style>
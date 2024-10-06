<!-- CartList.vue -->
<template>
  <div id="page-content" class="page-content">
    <div class="banner">
      <div class="container jumbotron-bg text-center rounded-0">
        <h1 style="color: #E91E63;" class="pt-5">Your Cart</h1>
        <p style="color: #E91E63;" class="lead">We’re dedicated in bringing you the best</p>
      </div>
    </div>

    <section id="cart" @add-to-cart="handleAddToCart">
      <form id="cart-form" class="form" action="" method="post">
        <div class="container">
          <div class="row">
            <div class="col-md-12">
              <div class="table-responsive"> 
                <table class="table">
                  <thead>
                    <tr>
                      <th width="10%"></th>
                      <th>Products</th>
                      <th>Price</th>
                      <th>Discounted Price</th>
                      <th width="15%">Quantity</th>
                      <th>Subtotal</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="product in cartItemProducts" :key="product.id">
                      <td>
                        {{ product.productImg }}
                        <a :id="product.id" :href="'/product-detail/' + product.id">
                          <img
                            :src="getImageSource(product)"
                            @error="setDefaultImage(product)"
                            width="108"
                          />
                        </a>
                      </td>
                      <td>
                        <a :id="product.id" :href="'/product-detail/' + product.id">
                          {{ product.name }}<br />
                          <small>{{ product.sell_quantity }} {{ product.sell_unit }}</small>
                        </a>
                      </td>
                      <td>{{ product.price }}</td>
                      <td>{{ (parseFloat(product.discounted_price)).toFixed(2) }}</td>
                      <td>
                        <button type="button" class="btn btn-danger btn-sm mb-1" style="font-size: 16px;margin-right: 10px" @click="changeItemQuantity(product, 'remove')">
                        <i class="fa fa-minus-circle"></i>
                        </button>
                          <!-- <a :id="product.id" :href="'/product-detail/' + product.id">
                          {{ product.quantity }}
                        </a>-->
                        {{ product.quantity }}
                        <button type="button" class="btn btn-success btn-sm mb-1" style="font-size: 16px;margin-left: 10px" @click="changeItemQuantity(product, 'add')">
                        <i class="fa fa-plus-circle"></i>
                        </button>
                      </td>
                      
                      <td>{{ (parseFloat(product.quantity * (product.price - (product.price * product.discount / 100)))).toFixed(2) }}</td>
                      <td>
                        <button type="button" class="bi bi-trash" style="color: red;border:none;font-size: 21px;" @click="removeItem(product)">
                        
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="col">
              <a href="/shop" class="btn btn-default">Continue Shopping</a>
            </div>
            <div class="col text-right">
              <div v-if="applyPromoCode === 1" class="input-group w-50 float-right">
                <input class="form-control" placeholder="Welcome01 Coupon Code" type="text" />
                <div class="input-group-append">
                  <button class="btn btn-default" type="button">Apply</button>
                </div>
              </div>
              <div class="clearfix"></div>
             <h6 class="mt-3">Total: Rs <span style="font-size: 21px;margin-left: 10px">{{ computedTotal }}</span></h6>
              
             <!--<input type="submit" name="submit" class="mt-3 btn btn-primary btn-lg" value="Proceed to Checkout" />-->
              <a style="background-color: #E91E63;" class="mt-3 btn btn-primary btn-lg" @click="checkout">Proceed to Checkout</a>
          
            </div>
          </div>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
import axios from 'axios';
import { computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();
const cartItemProducts = computed(() => [...store.state.cartProducts]);

const getImageSource = (product) => {
  if (product && product.imagename) {
    try {
      return require(`@/assets/img/${product.imagename}.jpg`);
    } catch (error) {
      console.error(`Error loading image for product`);
    }
  }
  return require('@/assets/img/unavailable_image_product.jpg');
};


const setDefaultImage = (product) => {
  product.imagename = 'unavailable_image_product';
};

const checkout = async () => {
  try {
    const jwtToken = localStorage.getItem('gurukrupaAppToken');
    const userId = localStorage.getItem('userId');
    const headers = {
      'Content-Type': 'application/json',
      // Add the Authorization header with the JWT token
      'Authorization': `Bearer ${jwtToken}`,
    };
    // Step 1: Create Cart
    const cartResponse = await axios.post('http://localhost:7000/api/cart', {
      user_id: userId, 
      total: parseFloat(computedTotal.value),
    }, { headers });

    const cartId = cartResponse.data.cart_id;
    localStorage.setItem('sessionId', cartId);
    console.log('Payload to cart-items is');
    console.log({
      session_id: cartId,
      cart_items: cartItemProducts.value.map(product => ({
        product_id: product.id,
        quantity: product.quantity,
        price: product.price,
        discount: product.discount,
      })),
    });
    // Step 2: Create Cart Items
    const cartItemsResponse = await Promise.all(
      cartItemProducts.value.map(async (product) => {
        return axios.post('http://localhost:7000/api/cart-items', {
          session_id: cartId,
          product_id: product.id,
          quantity: product.quantity,
          price: product.price,
          discount: product.discount,
        }, {headers});
      })
    );

    
    
    console.log('Checkout successful:', cartResponse.data, cartItemsResponse.data);

    
    router.push('/checkout');
  } catch (error) {
    console.error('Checkout failed:', error);
    // Handle errors, display messages, etc.
  }
};

const removeItem = (product) => {
  store.commit('removeItemFromCart', product);
};

const changeItemQuantity = (product, type) => {
  console.log('Clicked button ',type)
  store.commit('changeItemQuantity', { product, type });
};

onMounted(() => {
  console.log('loading cart from local storage');
  store.commit('loadCartFromLocalStorage');
  cartItemProducts.value = [...store.state.cartProducts];
  console.log(cartItemProducts.value);
});

const computedTotal = computed(() => {
  return cartItemProducts.value.reduce((total, product) => {
    // Calculate the subtotal for each product and add it to the total
    const subtotal = product.quantity * (product.price - (product.price * product.discount / 100));
    return total + subtotal;
  }, 0).toFixed(2); // Fix the total to 2 decimal places
});
</script>



<style scoped>
.space {
   /* Adjust the value as needed */
}
</style>

<template>
  <div id="page-content" class="page-content">
    <div class="banner">
      <div class="container jumbotron-bg text-center rounded-0">
        <h1 class="pt-5" style="color: #E91E63;">Checkout</h1>
        <p class="lead" style="color: #E91E63;">We’re dedicated in bringing you the best</p>
      </div>
    </div>

    <section id="checkout">
      <form id="checkout-form" class="form" action="" method="POST">
        <div class="container">
          <div class="row">
            <div class="col-xs-12 col-sm-6">
              <h5 class="mb-3">YOUR ORDER</h5>
              <div class="table-responsive">
                <table class="table">
                  <thead>
                    <tr>
                      <th>Products</th>
                      <th class="text-right">Subtotal</th>
                    </tr>
                  </thead>
                  <tbody>
                    <template v-for="product in cartItemProducts" :key="product.id">
                      <tr >
                        <td class="text-center">
                        <a :id="product.id" :href="'/product-detail/' + product.id">
                          <img
                            :src="getImageSource(product)"
                            @error="setDefaultImage(product)"
                            width="51"
                          />{{ product.name }} ({{ product.sell_quantity }} {{ product.sell_unit }}) x {{ product.quantity }}
                        </a>
                          
                        </td>
                        <td class="text-right">
                          <br>Rs {{ (parseFloat((product.quantity * product.discounted_price))).toFixed(2) }}
                        </td>
                      </tr>
                    </template>
                  </tbody>
                  <tfoot>
                    <tr>
                      <td>
                        <strong>Cart Subtotal</strong>
                      </td>
                      <td class="text-right">
                        Rs {{ (parseFloat(subtotal)).toFixed(2) }}
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <strong>Delivery Charges</strong>
                      </td>
                      <td class="text-right">
                      Rs 20.00
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <strong>ORDER TOTAL</strong>
                      </td>
                      <td class="text-right">
                        <input type="hidden" name="order-total" :value="computedTotal" />
                        <strong>{{ computedTotal }}</strong>
                      </td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>

            <div class="col-xs-12 col-sm-6">
              <div class="holder">
                <h5 class="mb-3">{{ DeliveryAddressDict.length > 0 ? 'SELECT A DELIVERY ADDRESS' : 'ENTER DELIVERY ADDRESS' }}</h5>
                <h6 class="mb-3" v-if="DeliveryAddressDict.length > 0">Your address</h6>
                <template v-for="deliveryAddressId in DeliveryAddressDict" :key="deliveryAddressId">
                <input
                  type="radio"
                  :id="deliveryAddressId"
                  :name="'delivery-address'"
                  :value="deliveryAddressId"
                  :checked="deliveryAddressId === DefaultAddressId"
                />
                {{ DeliveryAddressDict[deliveryAddressId] }}
                <br /><br />
              </template>
                <div class="form-group">
                  <a href="/newDeliveryAddressModal" class="btn btn-default">New Delivery Address</a>
                </div>
                <br /><br /><br />

                <h5 class="mb-3">PAYMENT METHODS</h5>
                <div class="form-check-inline">
                  <label class="form-check-label">
                    <input
                      class="form-check-input"
                      type="radio"
                      name="payment-mode"
                      id="payment-mode"
                      value="1"
                      checked
                    />
                    Cash On Delivery
                  </label>
                </div>
                <div class="form-check-inline">
                  <label class="form-check-label">
                    <input class="form-check-input" type="radio" name="payment-mode" id="payment-mode" value="2" />
                    UPI
                  </label>
                </div>
                <div class="form-check-inline">
                  <label class="form-check-label">
                    <input class="form-check-input" type="radio" name="payment-mode" id="payment-mode" value="3" />
                    Net Banking
                  </label>
                </div>
              </div>

              <br />
              <p class="text-left mt-3">
                <input checked="" type="checkbox" /> I’ve read &amp; accept the <a href="#">terms &amp; conditions</a>
              </p>
              <a  href="/cart" class="mt-3 btn btn-primary btn-lg" style="margin-right:10px;background-color: #E91E63;">Back To Cart</a>
              
              <a style="background-color: #E91E63;" class="mt-3 btn btn-primary btn-lg" @click="confirmOrder">Place Your Order</a>
            </div>
          </div>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import axios from 'axios';

const store = useStore();
const router = useRouter();

const cartItemProducts = computed(() => [...store.state.cartProducts]);
const DeliveryAddressDict = ref({});
const DefaultAddressId = ref(1);

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

const confirmOrder = async () => {
  try {
    // Create a new Purchase Order
    const userId = localStorage.getItem('userId');
    const sessionId= localStorage.getItem('sessionId');
    const orderResponse = await axios.post('http://localhost:7000/api/orders', {
      user_id: userId,
      shipping_charges: 20,
      total: parseFloat(computedTotal.value),
      session_id: sessionId,
      status:"SUCCESS",
    });
    const orderId = orderResponse.data.id;
    // Create Purchase Order Items
    const orderItemsResponse = await Promise.all(
      cartItemProducts.value.map(async (product) => {
        return axios.post('http://localhost:7000/api/purchase-order-item', {
          order_id: orderId,
          product_id: product.id,
          quantity: product.quantity,
          price: product.price,
          discount: product.discount,
        });
      })
    );

    // Optionally, you can handle the responses or redirect to a confirmation page
    console.log('Order placed successfully:', orderResponse.data);
    console.log('Order items created:', orderItemsResponse.map((res) => res.data));

    if (localStorage.getItem('cartItems')) {
        localStorage.removeItem('cartItems');
    }
    if (localStorage.getItem('sessionId')) { 
      localStorage.removeItem('sessionId');
    }
    store.state.totalQuantity=0

    // Redirect to the confirmation page
    router.push({ name: 'order-confirmation', params: { orderId: orderId } });
    
  } catch (error) {
    console.error('Error confirming order:', error);
    // Handle error as needed
  }
};

onMounted(() => {
  store.commit('loadCartFromLocalStorage');
  cartItemProducts.value = [...store.state.cartProducts];
});

const subtotal = computed(() => {
  return cartItemProducts.value.reduce((total, product) => {
    const productSubtotal = product.quantity * (product.price - (product.price * product.discount / 100));
    return total + productSubtotal;
  }, 0);
});

const computedTotal = computed(() => {
  const deliveryCharges = 20.0;
  const totalWithDelivery = (subtotal.value + deliveryCharges).toFixed(2);
  return totalWithDelivery;
});


</script>



<style scoped>
/* Your component styles go here */
</style>

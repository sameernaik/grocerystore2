<template>
  <div id="page-content"
       class="page-content">
    <div class="banner">
      <div class="container jumbotron-bg text-center rounded-0">
        <h1 :style="{ color: '#E91E63' }">
          {{ orderStatus === 'SUCCESS' ? 'Order Placed, thank you!' : 'Order Not Placed' }}
        </h1>
        <p :style="{ color: '#E91E63' }">
          {{
            orderStatus === 'SUCCESS'
            ? 'We’re dedicated in bringing you the best'
            : 'Order could not be placed at this time because the payment failed. Try using other Payment Method.'
          }}
        </p>
      </div>
    </div>

    <section id="checkout">
      <div class="container">
        <div class="row">
          <div class="col-xs-12 col-sm-12"
               v-if="orderStatus === 'SUCCESS'">
            <p class="mb-3">Confirmation will be sent to your email for your order</p>
          </div>
        </div>

        <p v-if="orderStatus === 'SUCCESS'">
          We will be sending a shipping confirmation email when the item is successfully shipped!
        </p>
        <h6 v-if="orderStatus === 'SUCCESS'"
            class="font-weight-bold mb-0">Thanks for shopping with us!</h6>
        <span v-if="orderStatus === 'SUCCESS'">Gurukrupa Grocery Team</span>
        <br />

        <router-link style="background-color: #E91E63;"
                     to="/shop"
                     class="mt-3 btn btn-primary btn-lg">
          Continue Shopping
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const orderStatus = ref('SUCCESS');
</script>

<style scoped>
</style>

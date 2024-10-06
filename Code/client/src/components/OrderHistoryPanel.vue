<template>
  <div>
    <div class="banner">
      <div class="container jumbotron-bg text-center rounded-0">
        <h1 class="pt-5" style="color: #E91E63;">
          Your Orders
        </h1>
        <p class="lead" style="color: #E91E63;">
          We’re dedicated in bringing you the best
        </p>
        <div class="d-flex justify-content-end">
          <button @click="downloadHistoricalOrders" class="btn btn-primary " style="background-color: #E91E63;margin-left:21px;margin-bottom:21px">
                      <span>Download Order History</span>
          </button>
        </div>
      </div>
    </div>

    <section id="cart">
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th width="5%">No</th>
                    <th>Order Id</th>
                    <th>Date</th>
                    <th>Total</th>
                    <th>Status</th>
                    <th>Details</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(order, index) in pastOrders" :key="order.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ order.id }}</td>
                    <td>{{ order.created_at }}</td>
                    <td>Rs {{ order.total }}</td>
                    <td>{{ order.status.toString() }}</td>
                    <!--<td>
                      <button class="btn btn-primary" style="background-color: #E91E63;margin-left:21px;margin-bottom:21px">
                      Details
                      </button>
                      `/product/${product.id}/edit`
                    </td>-->
                    <td>
                      <router-link :to="`/past-order/${order.id}`" class="nav-link" style="color: #E91E63" aria-current="page">
                       <b> <i class="fas fa-info-circle fa-2x"></i></b>
                      </router-link>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref,onMounted } from 'vue';

const userId = localStorage.getItem('userId');
const pastOrders = ref([]);

const fetchData = async () => {
  try {
    const response = await axios.get(`http://localhost:7000/api/user-orders/${userId}`);
    pastOrders.value = response.data;
  } catch (error) {
    console.error('Error fetching user orders:', error);
    // You can handle the error here if needed
  }
};
const downloadHistoricalOrders = async () => {
  try {
    const ordersHtml = generateOrdersHtml();

    const blob = new Blob([ordersHtml], { type: 'text/html' });
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = 'order_history_details.html';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error('Error generating/downloading file:', error);
  }
};

const generateOrdersHtml = () => {
  const tableRows = pastOrders.value.map((order, index) => `
    <tr>
      <td style="padding: 7px;">${index + 1}</td>
      <td style="padding: 7px;">${order.id}</td>
      <td style="padding: 7px;">${order.created_at}</td>
      <td style="padding: 7px;">Rs ${order.total}</td>
      <td style="padding: 7px;">${order.status.toString()}</td>
    </tr>
  `).join('');

  return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Order History Details</title>
      <style>
        table {
          border-collapse: collapse;
          width: 100%;
        }

        th, td {
          border: 1px solid #dddddd;
          text-align: left;
          padding: 8px;
        }

        th {
          background-color: #f2f2f2;
        }
      </style>
    </head>
    <body>
      <h1>Your Order History</h1>
      <table>
        <thead>
          <tr>
            <th>No</th>
            <th>Order Id</th>
            <th>Date</th>
            <th>Total</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          ${tableRows}
        </tbody>
      </table>
    </body>
    </html>
  `;
};


onMounted(fetchData);
</script>

<style scoped>
/* Your component styles go here */
</style>

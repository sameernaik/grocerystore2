<template>
    <div v-if="orderInfo !== null && orderInfo !== undefined"
         class="modal-container bordered">
        <div id="orderDetailsModal">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title" style="color: #E91E63">Order Details</h3>
                    </div>
                    <div >
                        <h6 style="text-align: left;"> Order Id: <b>{{ orderInfo.order_id }}</b></h6>
                        <h6 style="text-align: left;"> Customer Name: <b>{{ orderInfo.username }}</b></h6>
                        <h6 style="text-align: left;"> Total: <b> Rs {{ orderInfo.total }}</b></h6>
                        <h6 style="text-align: left;"> Order Date: <b> {{ orderInfo.created_at_str }}</b></h6>
                        <h6 style="text-align: left;"> Status: <b>{{ orderInfo.status }}</b></h6>
                        <br>
                        <div class="table-responsive" style="text-align: left;">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th><h5>Products</h5></th>
                                        <th class="text-right"><h5>Subtotal</h5></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="product in orderProductsInfo"
                                        :key="product.id">
                                        <td>
                                            <h6><b>{{ product.name }}</b> ({{ product.sell_quantity }} {{ product.sell_unit
                                            }}) x {{ product.quantity }}</h6>
                                        </td>
                                        <td class="text-right">
                                            <h5> Rs {{ product.quantity * (product.price - (product.price * product.discount
                                                / 100)) }}</h5>
                                        </td>
                                    </tr>
                                </tbody>
                                <tfooter>
                                    <tr>
                                        <td>
                                            <strong>Cart Subtotal</strong>
                                        </td>
                                        <td class="text-right">
                                            Rs {{ orderInfo.total - 20 }}
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
                                            <h6><strong>ORDER TOTAL</strong></h6>
                                        </td>
                                        <td class="text-right">
                                            
                                                Rs {{ orderInfo.total }}
                                           
                                        </td>
                                    </tr>
                                </tfooter>
                            </table>
                        </div>
                    </div>
                    <router-link to="/past-order"
                                 class="btn btn-success"
                                 style="background-color: #E91E63;display: block; margin-left: 45%; margin-right: 45%; margin-bottom: 5%; margin-top: 5%; width: 12%">
                        OK
                    </router-link>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
import { defineProps, onMounted,ref } from 'vue';
import axios from 'axios';



const props = defineProps({
    orderId: {
        type: Number,
        required: true,
    },
});
const orderInfo = ref(null);
const orderInfoError = ref(null);
const orderProductsInfo = ref(null);
const orderProductsInfoError = ref(null);

onMounted(async () => {
    console.log('Details for orderId: ', props.orderId);
    await getOrderInfo();
    await getOrderProductsInfo();
    console.log(orderInfo.value, orderInfoError.value, orderProductsInfo.value, orderProductsInfoError.value);
});

async function getOrderInfo() {
    try {
        const response = await axios.get(`http://localhost:7000/api/order-info/${props.orderId}`);
        orderInfo.value = response.data.order_info;
        orderInfoError.value = null;
    } catch (error) {
        console.error('Error fetching order info:', error);
        orderInfo.value = null;
        orderInfoError.value = 'Error fetching order info';
    }
}

async function getOrderProductsInfo() {
    try {
        const response = await axios.get(`http://localhost:7000/api/order-products-info/${props.orderId}`);
        orderProductsInfo.value = response.data;
        orderProductsInfoError.value = null;
    } catch (error) {
        console.error('Error fetching order products info:', error);
        orderProductsInfo.value = null;
        orderProductsInfoError.value = 'Error fetching order products info';
    }
}

</script>

<style scoped>
 .bordered {
        border: 2px solid #000; /* 2px solid black border */
        padding: 10px; /* Optional: Add padding for better visual appearance */
    }
</style>


<template>
    <div>
        <div class="row">
            <div class="col-xs-12 col-sm-6">
                <h3 class="mb-3"
                    style="margin-top:50px;margin-left:100px;color: #E91E63;">
                    Top 10 Selling Products (Last Week)
                </h3>
                <img alt="Detail Zoom thumbs image"
                     :src="getImgUrl(topTenProductQuantityImageName)"
                     @error="setDefaultImage"
                     style="width: 100%" />
            </div>
            <div class="col-xs-12 col-sm-6">
                <h3 style="margin-top:50px;margin-left:100px;color: #E91E63;">
                    Top Categorywise Products (Last Week)
                </h3>
                <img alt="Detail Zoom thumbs image"
                     :src="getImgUrl(topNCategorywiseProductImageName)"
                     @error="setDefaultImage"
                     style="width: 100%" />
            </div>
            <div class="col-xs-12 col-sm-6">
                <h3 style="margin-top:50px;margin-top:100px;margin-left:100px;color: #E91E63;">
                    Weekday wise Orders
                </h3>
                <img alt="Detail Zoom thumbs image"
                     :src="getImgUrl(dayOfWeekWiseOrdersImageName)"
                     @error="setDefaultImage"
                     style="width: 100%" />
            </div>
            <div class="col-xs-12 col-sm-6">
                <h3 style="margin-top:50px;margin-top:100px;margin-left:100px;color: #E91E63;">
                    Payment Mode Trend
                </h3>
                <img alt="Detail Zoom thumbs image"
                     :src="getImgUrl(paymentModeTrendImageName)"
                     @error="setDefaultImage"
                     style="width: 100%" />
            </div>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';

const topTenProductQuantityImageName = ref('top_10_product_quantity.png');
const topNCategorywiseProductImageName = ref('top_10_categorywise_product.png');
const dayOfWeekWiseOrdersImageName = ref('dayOfWeekWiseOrders.png');
const paymentModeTrendImageName = ref('paymentModeTrend.png');

const getImgUrl = (filename) => {
    // Assuming you have a method to generate the image URL
    return `http://127.0.0.1:7000/graph/${filename}`;
};

const setDefaultImage = (event) => {
  
    event.target.src = 'http://example.com/static/img/unavailable_image.jpg';
};

const generateGraphs = async () => {
    try {
        await axios.get('http://127.0.0.1:7000/api/generate-graphs');
        console.log('Graphs generated successfully');
        
    } catch (error) {
        console.error('Error generating graphs:', error);
        // Handle error, e.g., display an error message
    }
};

onMounted(() => {
    // Invoke the generateGraphs method on component mounting
    generateGraphs();
});
</script>

<style scoped>

</style>

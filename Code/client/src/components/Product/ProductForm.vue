<template>
<div class="modal-container" style="max-width: 700px; margin: 0 auto;">
    <div id="addProductModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <form id="product-add-form"
                      class="form"
                      action=""
                      method="POST">
                    <input type="hidden"
                           name="_method"
                           value="POST">
                    <div class="modal-header">
                    <h3 class="modal-title" style="color: #E91E63;">{{ mode === 'add' ? 'Add Product' : 'Edit Product' }}</h3>
                    </div>
        
                    <div class="modal-body">
                        <div class="form-group" style="padding: 10px; display: flex; align-items: center;">
                        <label for="product-name">Product&nbsp;Name:</label>
                            <input
                                v-model="productData.name"
                                type="text"
                                class="form-control"
                                name="product-name"
                                id="product-name"
                                required
                            />
                        </div>
                        <div class="form-group">
        <label for="product-description">Description:</label>
        <textarea v-model="productData.description" class="form-control" name="product-description" id="product-description"></textarea>
    </div>

    <div class="form-group">
        <label for="product-imagename">Image Name:</label>
        <input v-model="productData.imagename" type="text" class="form-control" name="product-imagename" id="product-imagename" required>
    </div>

    <div class="form-group">
        <label for="product-stock-quantity">Stock&nbsp;Quantity:</label>
        <input v-model="productData.stock_quantity" type="text" class="form-control" name="product-stock-quantity" id="product-stock-quantity" required>
    </div>
     <div class="form-group">
        <label for="product-stock-unit">Stock Unit:</label>
        <input 
            v-model="productData.stock_unit"
            type="text"
            class="form-control"
            name="product-stock-unit"
            id="product-stock-unit"
            required
        />
    </div>

    <div class="form-group">
        <label for="product-sell-quantity">Sell Quantity:</label>
        <input 
            v-model="productData.sell_quantity"
            type="text"
            class="form-control"
            name="product-sell-quantity"
            id="product-sell-quantity"
            required
        />
    </div>

    <div class="form-group">
        <label for="product-sell-unit">Sell Unit:</label>
        <input 
            v-model="productData.sell_unit"
            type="text"
            class="form-control"
            name="product-sell-unit"
            id="product-sell-unit"
            required
        />
    </div>
        <div class="form-group">
        <label for="product-price">Per Unit Price</label>
        <input 
            v-model="productData.price"
            type="text"
            class="form-control"
            name="product-price"
            id="product-price"
            required
        />
    </div>

    <div class="form-group">
        <label for="product-discount">Discount %</label>
        <input 
            v-model="productData.discount"
            type="text"
            class="form-control"
            name="product-discount"
            id="product-discount"
        />
    </div>

    <div class="form-group">
        <label for="product-manufacturingdate">Manufacturing Date&nbsp;(YYYY-MM-DD)</label>
        <input 
            v-model="productData.manufacturingdate"
            type="text"
            class="form-control"
            name="product-manufacturingdate"
            id="product-manufacturingdate"
        />
    </div>

    <div class="form-group">
        <label for="product-expirydate">Expiry Date (YYYY-MM-DD)</label>
        <input 
            v-model="productData.expirydate"
            type="text"
            class="form-control"
            name="product-expirydate"
            id="product-expirydate"
        />
    </div>

    <div class="form-group">
        <label for="product-categoryid">Category</label>
        <select 
            v-model="productData.categoryid"
            name="product-categoryid"
            id="product-categoryid"
            class="form-control"
            required
        >
          <!-- <option value="" disabled selected>Select Category</option>
            <option value="1">1</option>-->
            <option v-for="category in categoryCatalog" :key="category.id" :value="category.id">
                                            {{ category.name }}
                                        </option>
        </select>
    </div>

    <div class="form-group">
        <label for="product-available">Availability</label>
        <select 
            v-model="productData.available"
            name="product-available"
            id="product-available"
            class="form-control"
            required
        >
            <option value="1">Available</option>
            <option value="0">Unavailable</option>
        </select>
    </div>
    </div>
                    <div class="modal-footer">
                        <router-link to="/product" style="padding: 5px 21px; border: solid" class="btn btn-default">Cancel</router-link>
                        <input
                            @click.prevent="submitForm"
                            style="padding: 5px 21px; margin-left: 10px; border: solid;background-color: #E91E63;"
                            type="submit"
                            class="btn btn-success"
                            :value="mode === 'add' ? 'Add' : 'Edit'"/>
                    </div>
                    
                </form>
            </div>
        </div>
    </div>
</div>
</template>
<script setup>
import axios from 'axios';
import { ref, onMounted, defineProps } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
const store = useStore();
const router = useRouter();
const categoryCatalogLoaded = ref(false);
const categoryCatalog = ref([]);
const productData = ref({
    available:1,
});
// Define props, data, and lifecycle hooks directly without using 'const'
const props = defineProps({
    mode: {
        type: String,
        required: true,
    },
    productId: {
        type: Number,
        // productId is required when mode is 'edit'
        required: (mode) => mode === 'edit',
    },
});

// Use the onMounted hook to fetch data when the component is mounted
onMounted(async () => {
    console.log('Product Form mode', props.mode);
    await store.dispatch('fetchStoreManagerCategoryCatalog');
    categoryCatalog.value = store.getters.getStoreManagerCategoryCatalog;
    categoryCatalogLoaded.value = true;

    if (props.mode === 'edit') {
        console.log('Editing Product Id ', props.productId);
        try {
            const response = await axios.get(`http://localhost:7000/api/product/${props.productId}`);
            // Assuming the response.data is an object containing product details
            productData.value = response.data;
            console.log(productData)
        } catch (error) {
            console.error('Error fetching product data:', error);
            // Handle error as needed
        }
    }

});
const submitForm = async () => {
    if (!validateInputFields())
    { 
        return;
    }
    const jwtToken = localStorage.getItem('gurukrupaAppToken');
    const headers = {
        'Content-Type': 'application/json',
        // Add the Authorization header with the JWT token
        'Authorization': `Bearer ${jwtToken}`,
    };
    try {
        if (props.mode === 'add') {
            // Use POST endpoint for adding
            await axios.post('http://localhost:7000/api/products', productData.value, { headers });
        } else if (props.mode === 'edit') {
            // Use PUT endpoint for editing
            await axios.put(`http://localhost:7000/api/product/${props.productId}`, productData.value, { headers });
        }
        router.push('/product');
    } catch (error) {
        console.error('Error submitting form:', error);
        // Handle error as needed
    }
};
const validateInputFields = () => {
    // Check for required fields
    if (!productData.value.name) {
        console.error('Product Name is required');
        return false;
    }
    if (!productData.value.imagename) {
        // Display an error message or handle the validation error as needed
        console.error('Image Name is required');
        return false;
    }
    if (!productData.value.stock_quantity) {
        console.error('Stock Quantity is required');
        return false;
    }

    if (!productData.value.stock_unit) {
        console.error('Stock Unit is required');
        return false;
    }

    if (!productData.value.sell_quantity) {
        console.error('Sell Quantity is required');
        return false;
    }

    if (!productData.value.sell_unit) {
        console.error('Sell Unit is required');
        return false;
    }

    if (!productData.value.price) {
        console.error('Per Unit Price is required');
        return false;
    }
    if (!productData.value.discount) {
        console.error('Discount is required');
        return false;
    }

    if (!productData.value.categoryid) {
        console.error('Category is required');
        return false;
    }

    // Add validations for other required fields

    // If all validations pass, return true
    return true;
};

</script>
<style>
.form-group {
    margin-bottom: 1px;
    padding: 10px; 
    display: flex; 
    align-items: center;
}

label {
    display: inline-block;
    width: 150px; /* Adjust the width as needed */
    text-align: left;
    margin-right: 15px;
    color: #E91E63;
}

</style>





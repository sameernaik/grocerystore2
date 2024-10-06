<template>
  <div class="container">
    <div class="table-responsive">
      <div class="table-wrapper">
        <div class="table-title">
          <div class="row">
            <div class="col-xs-6">
              <h2 style="color: #E91E63;margin-top:21px;margin-bottom:21px"><b>Product</b> Management</h2>
            </div>
            <div v-if="!isAdmin" class="col-xs-6">
              <router-link to="/product/add" class="btn btn-primary" style="background-color: #E91E63;margin-bottom:21px">
                <i class="bi bi-plus"></i>
                <span>Add New Product</span>
              </router-link>
              <button @click="triggerJob" class="btn btn-primary" style="background-color: #E91E63;margin-left:21px;margin-bottom:21px">
                  <span>Trigger Report Job</span>
              </button>
              <button @click="checkStatus" class="btn btn-primary" style="background-color: #E91E63;margin-left:21px;margin-bottom:21px" :disabled="jobId === null">
                  <span>Check Report Job</span>
              </button>
            </div>
          </div>
        </div>
        <div class="table-responsive">
          <div class="table-wrapper">
        <div v-if="productsLoaded">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>Id</th>
                <th style="text-align:left;">Name</th>
                <th style="text-align:left;">Description</th>
                <th>Image</th>
                <th>Stock Qty</th>
                <th>Sell&nbsp;Qty</th>
                <th>Price</th>
                <th>Discount&nbsp;%</th>
                <th>Category</th>
                <th>Available</th>
                <th v-if="!isAdmin">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in products" :key="product.id">
                <td>{{ product.id }}</td>
                <td style="text-align:left; font-size: medium;">{{ product.name }}</td>
                <td style="text-align:left;">{{ product.description }}</td>
                <td>
                  <img
                    :src="getImageSource(product)"
                    width="60"
                    @error="handleImageError"
                  />
                </td>
                <td>{{ product.stock_quantity }}&nbsp;{{ product.stock_unit }}</td>
                <td>{{ product.sell_quantity }}&nbsp;{{ product.sell_unit }}</td>
                <td>{{ product.price }}</td>
                <td>{{ product.discount }}</td>
                <td>{{ getCategoryName(product.categoryid) }}</td>
                <!--<td>{{ categories[product.categoryid] }}</td>-->
                <td>{{ product.available ? 'Available' : 'Unavailable' }}</td>
                <td v-if="!isAdmin">
                  <div style="display: flex; align-items: center;">
                      <router-link
                        :to="`/product/${product.id}/edit`"
                        class="bi bi-pencil edit"
                        style="color: #E91E63;border:none;font-size: 21px;margin-right:11px"
                      >
                      </router-link>
                      <button
                        class="bi bi-trash delete"
                        style="color: #E91E63;border:none;font-size: 21px;"
                        @click="showDeleteConfirmation(product.id)"
                      >
                    </button>
                  </div>   
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, getCurrentInstance } from 'vue';
import store from '@/store'; 
import axios from 'axios';
import { useToast } from "vue-toastification";
const toast = useToast();
const customOptions = {
  position: 'top-right',
  timeout: 5000,
  closeOnClick: true,
  pauseOnHover: true,
  // Add any other custom options you need
};

const products = ref([]);
//Add one more productCatalog for storing filtering results.
const productsLoaded = ref(false);
const isAdmin = computed(() => localStorage.getItem('isAdmin') === 'true' || false);
const categoryCatalog = ref([]);
const jobId = ref(null);  // Define jobId as a ref


const { emit } = getCurrentInstance();

onMounted(async () => {
  // Fetch the product catalog when the component is mounted
  await store.dispatch('fetchStoreManagerProductCatalog');
  products.value = store.getters.getStoreManagerProductCatalog;
  console.log('Product Management', products.value)
  await store.dispatch('fetchCategoryCatalog');
  categoryCatalog.value = store.getters.getCategoryCatalog;
  productsLoaded.value = true;
})
const getCategoryName = (categoryid) => {
  for (const category of categoryCatalog.value) {
    if (category.id === categoryid) {
      return category.name;
    }
  }
  // Return a default value or handle the case when no match is found
  return "Unknown Category";
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
const handleImageError = (product) => {
  console.error(`Error loading image for product ${product.id}`);
  product.imageSource = require('@/assets/img/unavailable_image_product.jpg');
};

const showDeleteConfirmation = async (productId) => {
  // Display a confirmation dialog
  const userConfirmed = window.confirm('Are you sure you want to delete this product?');

  if (userConfirmed) {
    try {
      const jwtToken = localStorage.getItem('gurukrupaAppToken');

      const headers = {
        'Content-Type': 'application/json',
        // Add the Authorization header with the JWT token
        'Authorization': `Bearer ${jwtToken}`,
      };

      // Use DELETE endpoint for deleting
      await axios.delete(`http://localhost:7000/api/product/${productId}`, { headers });

      // Optionally, you can refresh the product list or perform other actions after successful deletion
      // For example, you can emit an event to inform the parent component to refresh the product list
      emit('productDeleted', productId);

      console.log('Product deleted successfully!');
    } catch (error) {
      console.error('Error deleting product:', error);
      // Handle error as needed
    }
  }
};
const triggerJob = async () => {
  try {
    const jwtToken = localStorage.getItem('gurukrupaAppToken');

    const headers = {
      // Add the Authorization header with the JWT token
      'Authorization': `Bearer ${jwtToken}`,
    };
    const response = await axios.get(`http://localhost:7000/product/export_products_csv`, { headers });
    jobId.value = response.data.job_id;
    console.log('CSV Download Job Id :', jobId.value);
    toast.info('Submitted request for product report generation.\n Job id ' + jobId.value, customOptions);
  } catch (error) {
    console.error('Error triggering job:', error);
  }
};

const checkStatus = async () => {
  try {
    if (!jobId.value) {
      console.error('Job ID is not defined');
      return;
    }
    const response = await axios.get(`http://localhost:7000/product/export_status/${jobId.value}`, {
      responseType: 'blob',
    });

    const contentTypeHeader = response.headers['content-type'];
    if (contentTypeHeader && contentTypeHeader.toLowerCase().includes('text/csv'))  {
      const blob = new Blob([response.data], { type: 'text/csv' });
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = 'product_details.csv';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } else
    {
      console.log('response.headers[content - type]', response.headers['content-type'])
      console.log('Task is not complete:', response.data);
      toast.info('Please wait... Report is being generated for job id '+ jobId.value , customOptions);
    }
  } catch (error) {
    console.error('Error checking status/downloading file:', error);
  }
};
</script>

<style>

</style>
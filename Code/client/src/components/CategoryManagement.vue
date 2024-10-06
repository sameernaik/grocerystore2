<template>
  <div class="container" style="max-width:1000px">
    <div class="table-responsive">
      <div class="table-wrapper">
        <div class="table-title">
          <div class="row">
            <div class="col-xs-6">
              <h2 style="color: #E91E63;margin-top:21px;margin-bottom:21px"><b>Category</b> Management</h2>
            </div>
            <div class="col-xs-6">
              <router-link  to="/category/add" class="btn btn-primary" style="background-color: #E91E63;margin-bottom:10px;">
                <i class="bi bi-plus"></i>
                <span v-if="isAdmin">Add New Category</span>
                <span v-if="!isAdmin">Request New Category</span>
              </router-link>
            </div>
          </div>
        </div>
         <div class="table-responsive">
            <div class="table-wrapper">
          <div v-if="categoriesLoaded">
        <table class="table table-striped table-hover">
          <thead>
            <tr>
              <th>Id</th>
              <th>Name</th>
              <th v-if="isAdmin">Assigned To</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <template v-if="categories.length > 0">
              <tr v-for="category in categories" :key="category.id">
                <td>{{ category.id }}</td>
                <td>{{ category.name }}</td>
                <td v-if="isAdmin">{{ storeManagers[category.owner] }}</td>
                <td style="min-width: 200px;">
                  <!-- Add Product link -->
                  <!-- <router-link :to="`/product/add?category=${category.id}`" class="add">
                    <i class="material-icons" data-toggle="tooltip" title="Add Product">&#xE147;</i>
                    <span>Add Product</span>
                  </router-link> -->

                  <!-- Edit Category link -->
                  <router-link :to="`/category/${category.id}/edit`" class="bi bi-pencil edit" style="color: #E91E63;border:none;font-size: 16px;margin-right: 20px;">
                    <i v-if="!isAdmin" class="" data-toggle="tooltip" title="Edit">Request Edit</i>
                  </router-link>

                  <!-- Delete Category link -->
                  <button
                          class="bi bi-trash delete"
                          style="color: #E91E63;border:none;font-size: 16px;"
                          @click="showDeleteConfirmation(category.id)"
                        >
                  <u><i v-if="!isAdmin" class="" data-toggle="tooltip" title="Delete">Request Delete</i></u>
                  </button>
                  <!--<router-link :to="`/category/${category.id}/delete`" class="bi bi-trash delete" style="color: #E91E63;border:none;font-size: 16px;">
                    <i v-if="!isAdmin" class="" data-toggle="tooltip" title="Delete">Request Delete</i>
                  </router-link>-->
                </td>
              </tr>
            </template>
            <template v-else>
              <tr>
                <td colspan="4">No categories available</td>
              </tr>
            </template>
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

const categories = ref([]);
//Add one more productCatalog for storing filtering results.
const categoriesLoaded = ref(false);
const isAdmin = computed(() => localStorage.getItem('isAdmin') === 'true' || false);
const { emit } = getCurrentInstance();
const storeManagers = ref({})

onMounted(async () => {
  // Fetch the category catalog when the component is mounted
  await store.dispatch('fetchStoreManagerCategoryCatalog');
  categories.value = store.getters.getStoreManagerCategoryCatalog;
  try {
    const response = await axios.get(`http://localhost:7000/api/managers`);
    // Assuming the response.data is an object containing product details
    const managerData = response.data;
    storeManagers.value = managerData.reduce((acc, obj) => {
      acc[obj.id] = obj.name;
      return acc;
    }, {});
    console.log('storeManagers', storeManagers.value)
  } catch (error) {
    console.error('Error fetching manager data:', error);
    // Handle error as needed
  }




  console.log('Categories Management', categories.value);
  categoriesLoaded.value = true;
})

const showDeleteConfirmation = async (categoryId) => {
  // Display a confirmation dialog
  const adminMessage = "Are you sure you want to delete the category ?";
  const storeManagerMessage = "Are you sure you want to request deletion of category ?";
  const message = isAdmin.value ? adminMessage :storeManagerMessage;
  const userConfirmed = window.confirm(message);

  if (userConfirmed) {
    try {
      const jwtToken = localStorage.getItem('gurukrupaAppToken');

      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${jwtToken}`,
      };

      await axios.delete(`http://localhost:7000/api/category/${categoryId}`, { headers });

      if (isAdmin.value) {
        emit('categoryDeleted', categoryId);
      }
      if (!isAdmin.value) {
        toast.info('Thank you ! Delete category request has been submitted for Admin Approval', customOptions);
      }
      console.log('Category Deleted successfully!');
    } catch (error) {
      console.error('Error deleting category:', error);
      
    }
  }
};

</script>

<style>
/* Add your styles here if needed */
</style>

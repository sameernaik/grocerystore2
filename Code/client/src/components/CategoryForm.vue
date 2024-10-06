<template>
  <div class="modal-container" style="max-width: 500px; margin: 0 auto;">
    <div id="addCategoryModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <form @submit.prevent="submitForm" id="category-modal-add" class="form">
            <div class="modal-header">
              <h3 v-if="isAdmin" class="modal-title" style="color: #E91E63;">{{ mode === 'add' ? 'Add Category' : 'Edit Category' }}</h3>
              <h3 v-if="!isAdmin" class="modal-title" style="color: #E91E63;">{{ mode === 'add' ? 'Request Add Category' : 'Request Edit Category' }}</h3>
            </div>
            <div class="modal-body">
              <div class="form-group">
                <h5><label for="category-name">Name</label></h5>
                <input v-model="categoryData.name" type="text" class="form-control" id="category-name" required />
              </div>
              <div v-if="isAdmin" class="form-group">
              <h5><label for="category-owner">Assign To</label></h5>
                    <select 
                        v-model="categoryData.owner"
                        name="category-owner"
                        id="category-owner"
                        class="form-control"
                        required
                     >
                        <!--<option selected value="2">storeManager2</option>
                        <option value="1">storeManager1</option>-->
                        <option v-for="manager in managerData" :key="manager.id" :value="manager.id">
                                              {{ manager.name }}
                                          </option>
                    </select>
              </div>
              <div id="" class="text-center">
                <h5 style="padding: 3px; color: red">{{ flashMessage }}</h5>
              </div>
            </div>
            <div class="modal-footer">
              <router-link to="/category" style="padding: 5px 21px; border: solid" class="btn btn-default">Cancel</router-link>
              <input
                  @click.prevent="submitForm"
                  style="padding: 5px 21px; margin-left: 10px; border: solid;background-color: #E91E63;"
                  type="submit"
                  class="btn btn-success"
                  :value="submitButtonValue"/>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref,onMounted,computed,defineProps } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from "vue-toastification";
const toast = useToast();
const customOptions = {
  position: 'top-right',
  timeout: 5000,
  closeOnClick: true,
  pauseOnHover: true,
  // Add any other custom options you need
};

const props = defineProps({
  mode: {
    type: String,
    required: true,
  },
  categoryId: {
    type: Number,
    // categoryId is required only when mode is 'edit'
    required: (mode) => mode === 'edit',
  },
});

const isAdmin = computed(() => localStorage.getItem('isAdmin') === 'true' || false);
const router = useRouter();
const categoryData = ref({});
const managerData = ref([]);
const flashMessage = ref('');

onMounted(async () => {
  console.log('Received props:', props);
   try {
    const response = await axios.get(`http://localhost:7000/api/managers`);
    // Assuming the response.data is an object containing product details
    managerData.value = response.data;
    console.log(managerData.value)
  } catch (error) {
    console.error('Error fetching manager data:', error);
    // Handle error as needed
  }
   if (props.mode === 'edit') {
    console.log('CategoryForm.onMounted Editing Category Id ', props.categoryId);
    try {
      const response = await axios.get(`http://localhost:7000/api/category/${props.categoryId}`);
      // Assuming the response.data is an object containing product details
      categoryData.value = response.data;
      console.log(categoryData.value)
    } catch (error) {
      console.error('Error fetching product data:', error);
      // Handle error as needed
    }
   }
});
const submitForm = async () => {
  if (!validateInputFields()) {
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
      if (!isAdmin.value) { 
        const managerId = localStorage.getItem('managerId');
        categoryData.value.owner = managerId;
      }
      await axios.post('http://localhost:7000/api/category', categoryData.value, { headers });
      if (!isAdmin.value) {
        toast.info('Thank you ! Add category request has been submitted for Admin Approval', customOptions);
      }
    } else if (props.mode === 'edit') {
      // Use PUT endpoint for editing
      await axios.put(`http://localhost:7000/api/category/${props.categoryId}`, categoryData.value, { headers });
      if (!isAdmin.value) {
        toast.info('Thank you ! Edit category request has been submitted for Admin Approval', customOptions);
      }
    }
    router.push('/category');
  } catch (error) {
    console.error('Error submitting form:', error);
    // Handle error as needed
  }
};
const validateInputFields = () => {
  // Check for required fields
  if (!categoryData.value.name) {
    console.error('Category Name is required');
    return false;
  }
  return true;
};
const submitButtonValue = computed(() => {
  if (props.mode === 'add' && isAdmin.value) {
    return 'Add';
  } else if (props.mode === 'edit' && isAdmin.value) {
    return 'Edit';
  } else if (props.mode === 'add' && !isAdmin.value) {
    return 'Request Add';
  } else if (props.mode === 'edit' && !isAdmin.value) {
    return 'Request Edit';
  }
  // Default value if none of the conditions match
  return 'Submit';
});
</script>


<style>
/* Add your styles here if needed */
</style>

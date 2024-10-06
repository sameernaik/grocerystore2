<template>
  <div class="container" style="max-width:1500px">
    <div class="table-responsive">
      <div class="table-wrapper">
        <div class="table-title">
          <div class="row">
            <div class="col-xs-6">
              <h2 style="color: #E91E63;margin-top:21px;margin-bottom:21px"><b>Approvals</b> Management</h2>
            </div>
           </div>
        </div>
         <div class="table-responsive">
            <div class="table-wrapper">
          <div v-if="approvalsLoaded">
        <table class="table table-striped table-hover">
          <thead>
            <tr>
              <th>Id</th>
              <th>Message</th>
              
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <template v-if="approvals.length > 0">
              <tr v-for="approval in approvals" :key="approval.id">
                <td>{{ approval.id }}</td>
                <td>{{ approval.message }}</td>
               
                <td style="min-width: 200px;">
                  <!-- Approve Link -->
                  <button
    @click="handleApproval(approval.id,'APPROVED')"
    class="btn btn-primary"
    style="background-color: #E91E63;margin-bottom:5px;margin-right:10px"
  >
  <span class="bi bi-check-circle-fill ms-2" style="font-size: 16px;">&nbsp;&nbsp;Approve</span>
  </button>

                  <!-- Reject Link -->
                  <button
                          
                          class="btn btn-primary"
                          style="background-color: #E91E63;margin-bottom:5px;"
                          @click="handleApproval(approval.id, 'REJECTED')"
                        >
                  <span class="bi bi-x-circle-fill ms-2" style="font-size: 16px;">&nbsp;&nbsp;Reject</span>
                  </button>
                </td>
              </tr>
            </template>
            <template v-else>
              <tr>
                <td colspan="4">No approvals available</td>
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

import axios from 'axios';

const approvals = ref([]);
//Add one more productCatalog for storing filtering results.
const approvalsLoaded = ref(false);
const isAdmin = computed(() => localStorage.getItem('isAdmin') === 'true' || false);
const { emit } = getCurrentInstance();


onMounted(async () => {

  try {
    const jwtToken = localStorage.getItem('gurukrupaAppToken');

    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${jwtToken}`,
    };

    const response = await axios.get(`http://localhost:7000/api/approvals`, {headers});
    approvals.value = response.data;
  } catch (error) {
    console.error('Error fetching manager data:', error);
  }

  console.log('approvals Management', approvals.value);
  approvalsLoaded.value = true;
})


const handleApproval = async (approvalId, status) => {
  try {
    const jwtToken = localStorage.getItem('gurukrupaAppToken');

    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${jwtToken}`,
    };

    const requestBody = { status };
    await axios.put(`http://localhost:7000/api/approvals/${approvalId}`, requestBody, { headers });

    if (isAdmin.value) {
      emit('approvalUpdated', approvalId);
    }

    console.log(`${status} successfully!`, approvalId);
  } catch (error) {
    console.error(`Error ${status.toLowerCase()}ing:`, error);
  }
};


</script>

<style>
/* Add your styles here if needed */
</style>

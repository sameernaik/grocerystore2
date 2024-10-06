<template>
  <div id="login" class="text-center">
    <div class="page-header">
      <img src="@/assets/img/logo-png.png" :width="300" class="mx-auto d-block" style="margin-bottom:51px" alt="Logo">
    </div>

    <div class="container">
      <div class="row justify-content-center align-items-center">
        <div class="col-md-7">
          <div class="col-md-7" style="margin-left:160px">
            <form @submit.prevent="authenticate">
              <h3 class="text-success">Login User {{ loginType }}</h3>
              <div class="form-group">
                <label for="username" class="text-success">Username:</label><br>
                <input type="email" placeholder="Email" v-model="username" name="username" id="username" class="form-control" required>
              </div>
              <div class="form-group">
                <label for="password" class="text-success">Password:</label><br>
                <input type="password" placeholder="Password" v-model="password" name="password" id="password" class="form-control" required minlength="7">
              </div>
              <div class="form-group" style="display: flex; justify-content: center;">
                <input type="submit" name="submit" class="btn btn-success btn-md" value="Submit" style="">
              </div>

              <div class="control">
                
                <a class="button is-large is-success" @click="register">Register here</a>
              </div>
            </form>
            <div v-if="formErrors.length > 0" class="alert alert-danger">
          <ul>
            <li v-for="(error, index) in formErrors" :key="index">
              {{ error }}</li></ul>
        </div>	
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { useToast } from "vue-toastification";
const toast = useToast();
export default {
  data () {
    return {
      username: '',
      password: '',
      errorMsg: '',
      formErrors: [],
    }
  },
  methods: {
    authenticate () {
      this.error = null;
      this.formErrors = [];
      this.$store.dispatch('login', { username: this.username, password: this.password })
        .then((response) => {
          if(response){
          const { data, status } = response;
          console.log("status",status)
          
          if (status === 200) {
            const accessToken = data; 
            console.log("accessToken", accessToken);
            toast.success('Authenticated !', { duration: 1000 });
            this.$router.push('/shop');
          } else {
            console.error('Unexpected HTTP status code:', status);
            this.$router.push('/login');
            toast.error('Unexpected HTTP status code:'+status, { duration: 1000 });
          }}
          else{
            console.error('Response is undefined',response)
          }
          }).catch((error) => {
            console.error('Error', error);
            const errorMessage = error.response.data.error;
            console.error('Login error:', errorMessage);
            this.formErrors = [];
            this.formErrors.push(errorMessage);
        });
    },
    register () {
      this.$router.push('/register/BUYER')
    },
    
  }
}
</script>



<style scoped>
.loginRow {
  width: 100vw;
  height: 95vh;
}
.form-wrapper {
  width: 90%;
}
</style>


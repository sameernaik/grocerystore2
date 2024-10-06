<template>
	<header>
		<!-- <img src="{{url_for('static', filename='/img/bg-header-all.jpg')}}">-->
		<div class="page-header">
			<div class="container align-items-center  justify-content-center" >
            <img src="@/assets/img/logo-png.png" :width="300">
        </div>
		</div>
	</header>
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/all.css">
<div class="container">
<hr>
    
	<div class="card bg-light">
    <article class="card-body mx-auto" style="min-width: 300px; min-height: 300px">
	
	<h2 class="card-title mt-2 text-center text-success">Create {{ registrationType }} Account</h2>
	<!--<p class="text-center">Get started with your free account</p>-->
	<form @submit.prevent="handleSubmit">
	<!-- Add the 'required' attribute to the input fields -->
	<input v-model="formData.firstname" class="form-control" placeholder="First name" type="text">
	<div class="spacer"></div>
	<input v-model="formData.lastname" class="form-control" placeholder="Last name" type="text">
	<div class="spacer"></div>
	<input v-model="formData.username" class="form-control" placeholder="Email" type="email" required minlength="1">
	<div class="spacer"></div>
	<input v-model="formData.password" class="form-control" placeholder="Create password" type="password" required minlength="7">
	<div class="spacer"></div>
	<input v-model="formData.repeatpassword" class="form-control" placeholder="Repeat password" type="password" required minlength="7">
	<div class="spacer"></div>
    <div class="form-group">
        <button type="submit" class="btn btn-success btn-md"> Create Account  </button>
    </div> <!-- form-group// -->

	<div v-if="formErrors.length > 0" class="alert alert-danger">
		<ul>
			<li v-for="(error,index) in formErrors" :key="index">
				{{ error }}</li></ul>
	</div>	
</form>

</article>
</div> <!-- card.// -->

</div>

</template>
<script>
import axios from 'axios';

export default {
	created() {
		this.registrationType = this.$route.params.registrationType;
	},
	methods: {
		async handleSubmit() {
			try {
				
				if (!this.validateForm()) {
					return;
				}

				const { repeatpassword, ...dataToSend } = this.formData;
				repeatpassword.length
				const response = await axios.post('http://localhost:7000/api/register', {
					...dataToSend,
					role: this.registrationType.toLowerCase() === 'buyer' ? 'BUYER' : 'STORE_MANAGER',
				});
				console.log('Registration successful:', response.data);
				this.$router.push('/login');
			} catch (error) {
				console.error('Error during registration:', error);
				if (error.response && error.response.status === 400) {
					const errorMessage = error.response.data.error;
					console.error('Registration error:', errorMessage);
					this.formErrors = [];
					this.formErrors.push(errorMessage);
					// Example using a hypothetical notification library
					// this.notifyUserError(errorMessage);
				}
			}
		},
		validateForm() {
			this.formErrors = [];
			console.log('Registration Type is ',this.registrationType);
			console.log('form data', this.formData);
			
			if (!this.formData.password.trim()) {
				this.formErrors.push('Password is required.');
			}

			
			if (!this.formData.repeatpassword.trim()) {
				this.formErrors.push('Repeat Password is required.');
			} else if (this.formData.password.trim() !== this.formData.repeatpassword.trim()) {
				this.formErrors.push('Password and Repeat Password must match.');
			}

			return this.formErrors.length === 0;
		},
	},
	data() {
		return {
			registrationType: this.registrationType ,
			formData: {
				firstname: '',
				lastname: '',
				username: '',
				password: '',
				repeatpassword: '',
			},
			formErrors: [],
		};
	},
};
</script>
<style>
.spacer {
  height: 10px;
}
</style>
import { createApp } from 'vue'
import App from './App.vue'

import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';

import router from './routes';
import store from './store';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

const app = createApp(App);

const options = {
    position: 'top-right',
    timeout: 2100,
    closeOnClick: true,
    pauseOnHover: true,
};
app.use(Toast, options);



app.use(router);
app.use(store);



app.mount('#app')
// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import LoginPage from '@/views/LoginPage.vue';
import RegistrationForm from '@/components/RegistrationForm.vue';
import ShopPage from '@/views/ShopPage.vue';
import ProductManagementPage from '@/views/ProductManagementPage.vue';
import ProductForm from '@/components/Product/ProductForm.vue';
import CategoryManagementPage from '@/views/CategoryManagementPage.vue';
import ApprovalsManagementPage from '@/views/ApprovalsManagementPage.vue';
import CategoryForm from '@/components/CategoryForm.vue';
import AdvancedSearchPage from '@/views/AdvancedSearchPage.vue';
import CartPage from '@/views/CartPage.vue';
import CheckoutPage from '@/views/CheckoutPage.vue';
import OrderConfirmationPage from '@/views/OrderConfirmationPage.vue';
import SearchResultPage from '@/views/SearchResultPage.vue';
import OrderPage from '@/views/OrderPage.vue';
import SummaryPage from '@/views/SummaryPage.vue';
import OrderHistoryDetailsPanel from '@/components/OrderHistoryDetailsPanel.vue';

const routes = [
    {
        path: '/',
        name: 'shopPage',
        component: ShopPage,
    },
    {
        path: '/shop',
        name: 'shop',
        component: ShopPage,
    },
    {
        path: "/login",
        name: "Login",
        component: LoginPage,
    },
    {
        path: "/register/:registrationType",
        name: "register",
        component: RegistrationForm,
    },
    {
        path: '/category',
        name: 'category',
        component: CategoryManagementPage,
    },
    {
        path: '/category/add',
        name: 'category-add',
        component: CategoryForm,
        props: { mode: 'add' },
    },
    {
        path: '/category/:id/edit',
        name: 'category-edit',
        component: CategoryForm,
        props: route => ({ mode: 'edit', categoryId: parseInt(route.params.id) }),
    },
   
    {
        path: '/product',
        name: 'product',
        component: ProductManagementPage,
    },
    {
        path: '/product/add',
        name: 'product-add',
        component: ProductForm,
        props: { mode: 'add'},
    },
    {
        path: '/product/:id/edit',
        name: 'product-edit',
        component: ProductForm,
        props: route => ({ mode: 'edit', productId: parseInt(route.params.id) }),
    },
    {
        path: '/past-order/:id',
        name: 'past-order-detail',
        component: OrderHistoryDetailsPanel,
        props: route => ({ orderId: parseInt(route.params.id) }),
    },
    {
        path: '/home',
        name: 'home',
        component: HomePage,
    },
    
    {
        path: '/advanced-search',
        name: 'advancedSearch',
        component: AdvancedSearchPage,
    },
    {
        path: '/cart',
        name: 'cart',
        component: CartPage,
    },
    {
        path: '/checkout',
        name: 'checkout',
        component: CheckoutPage,
    },
    {
        path: '/past-order',
        name: 'past-order',
        component: OrderPage,
    },
    {
        path: '/order-confirmation/:orderId',
        name: 'order-confirmation',
        component: OrderConfirmationPage,
    },
    {
        path: '/search-result',
        name: 'search-result',
        component: SearchResultPage,
    },
    {
        path: '/admin',
        name: 'admin',
        component: ApprovalsManagementPage,
    },
    {
        path: '/summary',
        name: 'summary',
        component: SummaryPage,
    },
    {
        path: '/messages',
        name: 'messages',
        component: ProductManagementPage,
    },
    
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
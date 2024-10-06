<template>
<div class="modal-container" style="width:900px;height:200px">
   <form id="advanced-search-form"
          
          action="/advanced-search"
          method="post">
    <div class="row justify-content-center">

        <div class="col-md-10">
            <div class="card p-3  py-4">

                <h5 style="color:#E91E63;font-weight: bold;">Advanced Search</h5>

                <div class="row g-3 mt-2">

                    <div class="col-md-3">
                        <div v-if="categoryCatalogLoaded">
                            <div class="form-group">
                                <!--<select name="category-id"
                                        id="category-id"
                                        class="form-control"
                                        style="background-color:white;color:#E91E63"
                                        required>
                                    <option value="0" selected>Any Category</option>
                                   {% for category in categoryCatalog %}
                                    <option value="{{ category.id }}">{{ category.name }}</option>
                                    {% endfor %} 
                                </select>-->
                                <select v-model="selectedCategory" @change="handleChange" style="background-color:white;color:#E91E63" >
                                    <option value="0" selected>Any Category</option>
                                    <option v-for="category in categoryCatalog" :key="category.id" :value="category.id">
                                        {{ category.name }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-6">

                        <input 
                               type="text"
                               v-model="searchProductNameInput"
                               name="search-input"
                               class="form-control"
                               placeholder="Search Product Name">

                    </div>

                    <div class="col-md-3">
                       <a @click="search" class="btn btn-secondary" style="padding-right: 30%; padding-left: 30%; color: white; background-color: #E91E63">
                        Search
                        </a>


                    </div>

                </div>


                <div class="mt-3">
                        <div>

                            <div class="card card-body">
                                <div class="col-md-6">
                                <label class="form-label">
                                    <p><b>Price range</b></p>
                                </label>
                                <div class="form-group" style="display: flex;align-items: center; ">
                                    <label for="min-price" style="margin-right:10px">Min&nbsp;Price</label>
                                    <input type="text"
                                        v-model="searchProductMinPriceInput"
                                        @input="handleInput"
                                        class="form-control"
                                        name="min-price"
                                        id="min-price"
                                        placeholder="Min Price"
                                        style="margin-bottom:10px">
                                        <span v-if="!isValid" style="color: red;">Please enter a valid numeric value</span>
                                </div>
                                <div class="form-group" style="display: flex; align-items: center;">
                                    <label for="max-price" style="margin-right:10px">Max&nbsp;Price</label>
                                    <input type="text"
                                        v-model="searchProductMaxPriceInput"
                                        class="form-control"
                                        name="max-price"
                                        id="max-price"
                                        placeholder="Max Price"
                                        
                                        style="margin-top:10px">
                                </div>
                            </div>
                        </div>
                       <!--  <br>
                            <div class="card card-body">
                                    <div class="col-md-12">
                                        <label for="customRange3"
                                            class="form-label">
                                            <p><b>Manufacturing Date</b></p>
                                        </label>
                                        
                                        <div class="row" style="margin-bottom:7px">
                                            <div class="form-group col-md-3">
                                                <label class="form-label">
                                                    <p>From Date</p>
                                                </label>
                                            </div>
                                            <div class="form-group col-md-2">
                                              <select name="from-day"
                                                        id="from-day"
                                                        class="form-control"
                                                        required>
                                                    <option value='0'
                                                            disabled
                                                            selected>Day</option>
                                                    {% for day_of_month in range (1, 32) %}
                                                    <option value={{
                                                            day_of_month
                                                            }}>{{ day_of_month }}</option>
                                                    {% endfor %}
                                                </select>
                                            </div>
                                            <div class="form-group col-md-2">
                                                <select name="from-month"
                                                        id="from-month"
                                                        class="form-control"
                                                        required>
                                                    <option value="0"
                                                            disabled
                                                            selected>Month</option>
                                                    {% for month in range (1, 13) %}
                                                    <option value={{
                                                                month
                                                            }}>{{ month }}</option>
                                                    {% endfor %}
                                                </select>
                                            </div>
                                            <div class="form-group col-md-3">
                                               <select name="from-year"
                                                        id="from-year"
                                                        class="form-control"
                                                        required>
                                                    <option value="0"
                                                            disabled
                                                            selected>Year</option>
                                                    {% for year in range (2020, 2024) %}
                                                    <option value={{
                                                            year
                                                            }}>{{ year }}</option>
                                                    {% endfor %}
                                                </select>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="form-group col-md-3">
                                                <label class="form-label">
                                                    <p>To Date</p>
                                                </label>
                                            </div>
                                            <div class="form-group col-md-2">
                                                <select name="to-day"
                                                        id="to-day"
                                                        class="form-control"
                                                        required>
                                                    <option value="0"
                                                            disabled
                                                            selected>Day</option>
                                                    {% for day_of_month in range (1, 32) %}
                                                    <option value={{
                                                            day_of_month
                                                            }}>{{ day_of_month }}</option>
                                                    {% endfor %}
                                                </select>
                                            </div>
                                            <div class="form-group col-md-2">
                                                <select name="to-month"
                                                        id="to-month"
                                                        class="form-control"
                                                        required>
                                                    <option value="0"
                                                            disabled
                                                            selected>Month</option>
                                                    {% for month in range (1, 13) %}
                                                    <option value={{
                                                            month
                                                            }}>{{ month }}</option>
                                                    {% endfor %}
                                                </select>
                                            </div>
                                            <div class="form-group col-md-3">
                                                <select name="to-year"
                                                        id="to-year"
                                                        class="form-control"
                                                        required>
                                                    <option value="0"
                                                            disabled
                                                            selected>Year</option>
                                                    {% for year in range (2020, 2026) %}
                                                    <option value={{
                                                            year
                                                            }}>{{ year }}</option>
                                                    {% endfor %}
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                            </div>
                        <br>-->
                            <!--
                            <div class="card card-body">
                                <div class="col-md-12">
                                    <label for="customRange3"
                                           class="form-label">
                                        <p><b>Expiry Date</b></p>
                                    </label>
                            
                                    <div class="row"
                                         style="margin-bottom:7px">
                                        <div class="form-group col-md-3">
                                            <label class="form-label">
                                                <p>From Date</p>
                                            </label>
                                        </div>
                                        <div class="form-group col-md-2">
                                            <select name="from-day-expiry"
                                                    id="from-day-expiry"
                                                    class="form-control"
                                                    required>
                                                <option value='0'
                                                        disabled
                                                        selected>Day</option>
                                                {% for day_of_month in range (1, 32) %}
                                                <option value={{
                                                        day_of_month
                                                        }}>{{ day_of_month }}</option>
                                                {% endfor %}
                                            </select>
                                        </div>
                                        <div class="form-group col-md-2">
                                            <select name="from-month-expiry"
                                                    id="from-month-expiry"
                                                    class="form-control"
                                                    required>
                                                <option value="0"
                                                        disabled
                                                        selected>Month</option>
                                                {% for month in range (1, 13) %}
                                                <option value={{
                                                        month
                                                        }}>{{ month }}</option>
                                                {% endfor %}
                                            </select>
                                        </div>
                                        <div class="form-group col-md-3">
                                             <select name="from-year-expiry"
                                                    id="from-year-expiry"
                                                    class="form-control"
                                                    required>
                                                <option value="0"
                                                        disabled
                                                        selected>Year</option>
                                                {% for year in range (2020, 2026) %}
                                                <option value={{
                                                        year
                                                        }}>{{ year }}</option>
                                                {% endfor %}
                                            </select>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="form-group col-md-3">
                                            <label class="form-label">
                                                <p>To Date</p>
                                            </label>
                                        </div>
                                        <div class="form-group col-md-2">
                                            <select name="to-day-expiry"
                                                    id="to-day-expiry"
                                                    class="form-control"
                                                    required>
                                                <option value="0"
                                                        disabled
                                                        selected>Day</option>
                                                {% for day_of_month in range (1, 32) %}
                                                <option value={{
                                                        day_of_month
                                                        }}>{{ day_of_month }}</option>
                                                {% endfor %}
                                            </select>
                                        </div>
                                        <div class="form-group col-md-2">
                                             <select name="to-month-expiry"
                                                    id="to-month-expiry"
                                                    class="form-control"
                                                    required>
                                                <option value="0"
                                                        disabled
                                                        selected>Month</option>
                                                {% for month in range (1, 13) %}
                                                <option value={{
                                                        month
                                                        }}>{{ month }}</option>
                                                {% endfor %}
                                            </select>
                                        </div>
                                        <div class="form-group col-md-3">
                                             <select name="to-year-expiry"
                                                    id="to-year-expiry"
                                                    class="form-control"
                                                    required>
                                                <option value="0"
                                                        disabled
                                                        selected>Year</option>
                                                {% for year in range (2020, 2026) %}
                                                <option value={{
                                                        year
                                                        }}>{{ year }}</option>
                                                {% endfor %}
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>-->
                            
                        </div>
                    </div>
              
             </div>

        </div>

    </div>
    </form>
</div>
</template>
<script setup>
import { ref,onMounted,computed } from 'vue';
import {useStore} from 'vuex';
import { useRouter } from 'vue-router';
const store = useStore();
const router = useRouter();
const searchProductNameInput = ref('');
const searchProductMinPriceInput = ref(0);
const searchProductMaxPriceInput = ref(10000);
const categoryCatalogLoaded = ref(false);
const categoryCatalog = ref([]);
const selectedCategory = ref(0); 
const isValid = computed(() => /^\d+$/.test(searchProductMinPriceInput.value)); 
const search = async () => {
     const filterParams = {
        categoryId: selectedCategory.value,
        filterString: searchProductNameInput.value,
        minPrice: searchProductMinPriceInput.value,
        maxPrice: searchProductMaxPriceInput.value
    };
    console.log("Searching ", searchProductNameInput.value)
    
    await store.dispatch('filterProducts', filterParams);
    router.push('/search-result');
};
onMounted(async () => {
    // Fetch the product catalog when the component is mounted
  await store.dispatch('fetchCategoryCatalog');
  await store.dispatch('fetchProductCatalog');
  categoryCatalog.value = store.getters.getCategoryCatalog;
  //store.commit('loadCartFromLocalStorage');
  //console.log('onMounted',productCatalog.value )
  categoryCatalogLoaded.value = true;
});
const handleChange = () => {
  console.log('Category Changed',selectedCategory.value);
};
const handleInput = () => {
  if (!isValid.value) {
    // Optionally, you can clear the input or provide user feedback here
  }
};
</script>
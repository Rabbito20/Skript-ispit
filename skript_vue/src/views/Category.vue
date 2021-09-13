<template>
    <div class="page-category">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h2 class="is-size-2 has-text-centered">{{ category.name }}</h2>
            </div>

            <div class="columns is-multiline">
            <div class="column is-12">
                <h2 class="is-size-2 has-text-centered">Latest products</h2>
            </div>

            <!-- <div class="column is-3"
            v-for="product in category.products"
            v-bind:key="product.id"
            >
                <div class="box">
                <figure class="image mb-4">
                    <img :src="product.get_thumbnail">
                </figure>

                <h3 class="is-size-4">{{ product.name }}</h3>
                <p class="is-size-6 has-text-grey">{{ product.price }} EUR</p>

                <router-link v-bind:to="product.get_absolute_url" class="button is-dark mt-4">View details</router-link>
                </div>
            </div> -->

            <ProductBox
            v-for="product in category.products"
            v-bind:key="product.id"
            v-bind:product="product"/>
        

            </div>
        </div>
    </div>
</template>

<script>

import axios from 'axios'
import { toast } from 'bulma-toast'

import ProductBox from '@/components/ProductBox'

export default {
    name: 'Category',
    data() {
        return {
            category: {
                products: []
            }
        }
    },
    components: {
        ProductBox
    },
    mounted() {
        this.getCategory()
    },
    watch: {
        // Ovo u slucaju kad menjamo rute za Winter i Summer prati i refreshuje sadrzaj po potrebi
        // U suprotnom pri promeni kategorije moramo da refreshujemo stranicu manuelno
        $route(to, from) {
            if (to.name === 'Category') {
                this.getCategory()
            }
        }
    },
    methods: {
        async getCategory() {
            const categorySlug = this.$route.params.category_slug

            this.$store.commit('setIsLoading', true)

            axios
                .get(`/api/v1/products/${categorySlug}/`)
                .then(response => {
                    this.category = response.data

                    document.title = this.category.name + ' | Ziccak'
                })
                .catch(error => {
                    console.log(error)

                    toast ({
                        message: 'Something went wrong. Please try again.',
                        type: 'is-danger',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'bottom-right',
                    })
                })

            this.$store.commit('setIsLoading', false)

        }
    }
}
</script>
<template>
    <div class="footer">
        <a href="http://www.beian.gov.cn" target="_blank" v-if="beian">
            <img class="beian" :src="beian_url" />
            {{ beian }}
        </a>
        <a href="http://beian.miit.gov.cn" target="_blank" v-if="icp">{{ icp }}</a>
        Copyright &copy; {{ year }} All rights reserved.
        Powered by
        <a
            href="https://github.com/staugur/picbed"
            target="_blank"
            ref="nofollow"
        >picbed</a>
    </div>
</template>

<script>
export default {
    name: 'Footer',
    data() {
        return {
            beian_url: require('@/assets/img/beian.png')
        }
    },
    computed: {
        year() {
            return new Date().getFullYear()
        },
        icp() {
            return this.$store.state.icp
        },
        beian() {
            return this.$store.state.beian
        }
    }
}
</script>

<style>
.footer {
    text-align: center;
}
.footer a {
    color: #666;
    text-decoration: none;
}
.footer a:hover {
    color: #777;
}
.footer .beian {
    vertical-align: middle;
    margin-top: -4px;
}
</style>
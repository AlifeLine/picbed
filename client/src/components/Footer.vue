<template>
    <div class="footer">
        <a href="http://www.beian.gov.cn" target="_blank" v-if="beian">
            <img class="beian" :src="beian_url" />
            {{ beian }}
        </a>
        <a href="http://www.beian.miit.gov.cn" target="_blank" v-if="icp">{{ icp }}</a>
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
    props: ['icp', 'beian'],
    data() {
        return {
            beian_url: require('@/assets/img/beian.png')
        }
    },
    computed: {
        year() {
            return new Date().getFullYear()
        }
    }
}
</script>

<style>
.footer a {
    color: #666;
}
.footer a:hover {
    color: #777;
}
.footer .beian {
    vertical-align: middle;
    margin-top: -4px;
}
</style>
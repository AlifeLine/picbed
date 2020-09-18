<!--
  * 基于Semantic-UI的基础按钮组件
  *
  * @param {String} type 按钮原生属性，支持submit、reset、button（默认）
  * @param {Boolean} autofocus 按钮原生属性，聚焦，默认false
  * @param {Boolean} disabled 按钮原生属性，禁用，默认false
  * @param {Boolean} loading 加载中（图标）
  * @param {Boolean} isBasic 是否为基础样式，即边框风格，否则全色风格
  * @param {Boolean} isFluid 适应容器
  * @param {Boolean} isCircle 圆形
  * @param {Boolean} isCompact 紧凑
  * @param {Boolean} isAttached 附加（存在float时有效）
  * @param {Boolean} isActive 活动的
  * @param {Boolean} isInverted 翻转（存在color时有效）
  * @param {String} icon 图标的font-class
  * @param {String} float 浮动，支持left、right
  * @param {String} size 按钮尺寸: mini tiny small medium large big huge
  * @param {String} color 按钮颜色:
                        red-红色 orange-橘黄色 yellow-黄色 olive-橄榄色
                        green-绿色 teal-蓝绿色 blue-蓝色 violet-紫罗兰色
                        purple-紫色 pink-粉色 brown-褐色 grey-灰色 black-黑色
-->
<template>
    <button
        class="ui button"
        :type="type"
        :autofocus="autofocus"
        :disabled="disabled || loading"
        :class="[
            {
                basic: isBasic,
                disabled: disabled,
                loading: loading,
                fluid: isFluid,
                circular: isCircle,
                compact: isCompact,
                attached: setAttached,
                active: isActive,
                inverted: setInverted,
                icon: icon
            },
            size, color, float
        ]"
        @click="handleClick"
    >
        <i :class="loadingIcon" v-if="loading"></i>
        <i :class="[ fontClass, icon ]" v-if="icon && !loading"></i>
        <span v-if="$slots.default">
            <slot></slot>
        </span>
    </button>
</template>
<script>
export default {
    name: 'SuiButton',
    data() {
        return {
            fontClass: '',
            loadingIcon: 'icon-loading'
        }
    },
    props: {
        type: {
            type: String,
            default: 'button',
            validator(value) {
                return ['button', 'submit', 'reset'].includes(value)
            }
        },
        autofocus: Boolean,
        disabled: Boolean,
        loading: Boolean,
        isBasic: Boolean,
        isFluid: Boolean,
        isCircle: Boolean,
        isCompact: Boolean,
        isAttached: Boolean,
        isActive: Boolean,
        isInverted: Boolean,
        icon: String,
        float: {
            type: String,
            validator(value) {
                return ['left', 'right'].includes(value)
            }
        },
        size: {
            type: String,
            validator(value) {
                return [
                    'mini',
                    'tiny',
                    'small',
                    'medium',
                    'large',
                    'big',
                    'huge'
                ].includes(value)
            }
        },
        color: {
            type: String,
            validator(value) {
                return [
                    'red',
                    'orange',
                    'yellow',
                    'olive',
                    'green',
                    'teal',
                    'blue',
                    'violet',
                    'purple',
                    'pink',
                    'brown',
                    'grey',
                    'black'
                ].includes(value)
            }
        }
    },
    computed: {
        setAttached() {
            return this.isAttached && this.float
        },
        setInverted() {
            return this.isInverted && this.color
        }
    },
    methods: {
        handleClick(event) {
            if (this.disabled === true) return
            this.$emit('click', event)
        }
    }
}
</script>

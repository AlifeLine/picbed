module.exports = {
    devServer: {
        host: process.env.picbed_host || '127.0.0.1',
        port: 9513,
        proxy: 'http://127.0.0.1:9514'
    }
}

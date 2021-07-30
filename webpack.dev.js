const config = require('./webpack.common.js');
const merge = require('webpack-merge');


module.exports = merge(config, {
  mode: 'development',

  devtool: 'eval-source-map',

  stats: {
    colors: true,
  },

  watch: true,
  watchOptions: {
    aggregateTimeout: 300,
    poll: 1000
  },
});

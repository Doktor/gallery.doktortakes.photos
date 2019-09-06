const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
  mode: 'development',

  context: __dirname,

  entry: {
    editAlbum: path.resolve('src/entry/editAlbum.js'),
  },

  output: {
    path: path.resolve('./static/bundles/'),
    filename: '[name].[hash].js',
  },

  plugins: [
    new BundleTracker({
      filename: './src/webpack-stats.json',
    }),
    new VueLoaderPlugin(),
  ],

  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          compilerOptions: {
            whitespace: 'condense',
          },
        },
      },
    ],
  },

  resolve: {
    alias: {
      vue: 'vue/dist/vue.js',
    },
  },

  watch: true,
  watchOptions: {
    aggregateTimeout: 300,
    poll: 1000
  }
};

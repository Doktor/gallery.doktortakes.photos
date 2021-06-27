const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin');


module.exports = {
  context: __dirname,

  entry: {
    main: path.resolve(__dirname, './src/main.js'),
  },

  output: {
    path: path.resolve(__dirname, './static/'),
    filename: '[name].js',
  },

  plugins: [
    new BundleTracker({
      path: __dirname,
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
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.s[ac]ss$/,
        use: [
          'style-loader',
          'css-loader',
          {
            loader: 'sass-loader',
            options: {
              prependData: `@import "./src/styles/_variables.scss";`,
            },
          },
        ],
      },
      {
        test: /\.js$/,
        exclude: /(node_modules)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',
            ],
            plugins: [
              // reuse injected helper code
              '@babel/plugin-transform-runtime',
              // import()
              '@babel/plugin-syntax-dynamic-import',
            ],
          }
        }
      },
      {
        test: /\.(png)$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'images/',
              publicPath: '/static/images/',
            },
          },
        ],
      },
    ],
  },

  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      vue: 'vue/dist/vue.js',
    },
    extensions: ['.js', '.json', '.vue'],
  },
};

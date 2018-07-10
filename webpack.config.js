// Webpack v4 Config

const path = require('path');
// const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");
const HtmlWebpackPlugin = require('html-webpack-plugin');
// const VueLoaderPlugin = require('vue-loader/lib/plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

const devMode = process.env.NODE_ENV !== 'production';

module.exports = {
    entry: {
        index: './src/script.js'
    },
    output: {
        path: path.resolve(__dirname, 'static'),
        filename: '[name].bundle.js',
    },

    optimization: {
        minimizer: [
            new UglifyJsPlugin({}),
            new OptimizeCSSAssetsPlugin({})
        ]
    },

    plugins: [
        new CleanWebpackPlugin(['static', 'templates']),
        new MiniCssExtractPlugin({}),
        new HtmlWebpackPlugin({
            filename: '../templates/index.html',
            template: './src/index.html',
            minify: devMode ? false : {
                removeComments: true,
                collapseWhitespace: true,
                conservativeCollapse: true
            },
        }),
        new HtmlWebpackPlugin({
            filename: '../templates/login.html',
            template: './src/login.html',
            minify: devMode ? false : {
                removeComments: true,
                collapseWhitespace: true,
                conservativeCollapse: true
            },
            inject: false
        }),
        // new VueLoaderPlugin(),
        // new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/)
    ],

    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    },

    module: {
        rules: [{
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /\.css$/,
                use: [
                    devMode ? 'style-loader' : MiniCssExtractPlugin.loader,
                    "css-loader"
                ]
            },
            // {
            //     test: /\.scss$/,
            //     use: [
            //         devMode ? 'style-loader' : MiniCssExtractPlugin.loader,
            //         "css-loader",
            //         'sass-loader'
            //     ]
            // },
            // {
            //     test: /\.vue$/,
            //     loader: 'vue-loader'
            // },
            {
                test: /\.(png|jpg|jss)$/,
                use: [{
                    loader: 'file-loader',
                    options: {
                        name: '[name].[ext]'
                    }
                }]
            }
        ]
    }
}
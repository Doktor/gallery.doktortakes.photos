import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          whitespace: "condense",
        },
      },
    }),
  ],
  base: "/static/",
  build: {
    outDir: "./static",
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, "src/main.js"),
      },
    },
    target: "esnext",
  },
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
      "vue": "vue/dist/vue.runtime.esm-bundler.js",
    },
    extensions: [".js", ".json", ".vue"],
  },
  css: {
    preprocessorOptions: {
      scss: {
        includePaths: [resolve(__dirname, "src/styles")],
      },
    },
  },
});

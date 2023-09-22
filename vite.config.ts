import vue from "@vitejs/plugin-vue";

import path from "path";

import { defineConfig } from "vite";

export default ({ mode }) => {
  return defineConfig({
    plugins: [vue()],
    root: path.join(__dirname, "frontend"),
    envDir: path.resolve(__dirname),
    server: {
      port: 5000,
      strictPort: true
    },
    build: {
      emptyOutDir: true,
      target: "es2020",
      assetsDir: "static"
    },
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "frontend/src/")
      }
    }
  });
};

const longLine = [
  "something",
  "something else",
  "this should still fit",
  "it's close",
  "ha"
];

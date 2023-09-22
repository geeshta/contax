import { defineConfig } from "vite";

import path from "path";

export default ({ mode }) => {
  return defineConfig({
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

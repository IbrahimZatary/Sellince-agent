import { fileURLToPath } from "node:url";

import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const SOURCE_DIRECTORY = fileURLToPath(new URL("./src", import.meta.url));

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": SOURCE_DIRECTORY,
    },
  },
  test: {
    environment: "jsdom",
    fileParallelism: false,
    include: ["src/**/*.test.jsx"],
    maxWorkers: 1,
    pool: "forks",
    setupFiles: ["./src/test/setup.js"],
  },
});

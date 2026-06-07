import path from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

const root = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  resolve: {
    alias: {
      "/images": path.join(root, "public/images"),
    },
  },
  server: {
    fs: {
      allow: [root, path.join(root, "public")],
    },
  },
});

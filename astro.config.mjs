import { defineConfig } from 'astro/config';

export default defineConfig({
  // Output static HTML files
  output: 'static',

  // Base URL for the site
  site: 'https://modernmoneylab.eu',

  // Build options
  build: {
    // Output directory
    outDir: './dist',
    // Assets directory within output
    assets: 'assets'
  },

  // Development server
  server: {
    port: 3000
  }
});

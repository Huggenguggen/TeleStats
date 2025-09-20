# Use Node.js official image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy rest of the frontend
COPY . .

# Build Nuxt app
RUN npm run build

# Expose port
EXPOSE 3000

# Start Nuxt
CMD ["npm", "run", "preview"]

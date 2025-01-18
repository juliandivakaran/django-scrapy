# Use an official Node.js image as a base
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json /app/

# Install dependencies
RUN npm install

# Copy the rest of the app's source code
COPY . /app/

# Build the React app for production
RUN npm run build

# Expose the port for React (default is 3000)
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]

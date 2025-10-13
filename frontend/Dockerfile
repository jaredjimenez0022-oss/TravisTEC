# Dockerfile para Frontend
FROM node:18-alpine

WORKDIR /app

# Copiar package.json (si existe)
COPY package*.json ./

# Instalar dependencias (si hay package.json)
RUN if [ -f package.json ]; then npm install; fi

# Copiar código fuente
COPY . .

# Exponer puerto
EXPOSE 3000

# Servidor simple para desarrollo
CMD ["npx", "http-server", "src", "-p", "3000", "--cors"]

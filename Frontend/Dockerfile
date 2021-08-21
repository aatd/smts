# stage1 as builder
FROM node:10-alpine as builder

WORKDIR /mythief-ui

ARG ISRPI 

# Copy the package.json and install dependencies
COPY package*.json ./

RUN if [ "$ISRPI" != "TRUE" ] ; then npm install ; fi

# Copy rest of the files
COPY . .

# Build the project
RUN if [ "$ISRPI" != "TRUE" ] ; then npm run build ; fi


FROM nginx:alpine as production-build
COPY ./.nginx/nginx.conf /etc/nginx/nginx.conf

## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

# Copy from the stage 1
COPY --from=builder /mythief-ui/dist /usr/share/nginx/html

EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]
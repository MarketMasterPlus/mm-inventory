```
PUC-Rio
Especialização em Desenvolvimento Fullstack
Disciplina: Desenvolvimento Back-end Avançado

Aluno: Rodrigo Alves Costa
```

## Market Master: Inventory Management Service

The `mm-inventory` service is part of the Market Master project, a suite of microservices designed to manage various aspects of a supermarket e-commerce platform. This service handles product inventory, stock management, and price tracking across different stores.

### Related Market Master Microservices:
- [mm-product](https://github.com/MarketMasterPlus/mm-product) — Product (item registry) Management
- [mm-store](https://github.com/MarketMasterPlus/mm-store) — Store Management
- [mm-address](https://github.com/MarketMasterPlus/mm-address) — Address Management with ViaCEP API integration
- [mm-customer](https://github.com/MarketMasterPlus/mm-customer) — Customer/User Management
- [mm-shopping-cart](https://github.com/MarketMasterPlus/mm-shopping-cart) — Shopping Cart Management
- [mm-pact-broker](https://github.com/MarketMasterPlus/mm-pact-broker) — Pact Broker for Contract tests
- [mm-ui](https://github.com/MarketMasterPlus/mm-ui) — User Interface for Market Master

---

## Quick Start

### Prerequisites
- **Docker** and **Docker Compose** are required to run this service.

### Steps to Run the Service
1. Clone the repository:  
   git clone https://github.com/MarketMasterPlus/mm-inventory

2. Navigate to the project directory:  
   cd mm-inventory

3. Start the services with Docker Compose:  
   docker-compose up -d

4. Access the Inventory Management API at:  
   http://localhost:5705/

---

## Project Description

The `mm-inventory` service is responsible for managing inventory data, including product stock, pricing, and store-specific inventory details. It communicates with the `mm-product` and `mm-store` services to fetch product and store data, respectively.

### Key Features
- **Inventory Management**: Allows users to manage product inventory across different stores.
- **Store-Specific Pricing and Stock**: Tracks pricing and stock levels for products at individual stores.
- **Integration with Product and Store Services**: Communicates with `mm-product` and `mm-store` to retrieve product and store information.

---

## Docker Setup

The `docker-compose.yml` file configures the `mm-inventory` service and a PostgreSQL database for data storage.

### Docker Compose Configuration:

version: '3.8'

services:
  db:
    image: postgres:latest
    container_name: mm-inventory-db
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: marketmaster
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/mm-inventory.sql:/docker-entrypoint-initdb.d/mm-inventory.sql
    ports:
      - 5436:5432
    networks:
      - marketmaster-network

  product_service:
    build: .
    container_name: mm-inventory
    ports:
      - 5705:5705
    depends_on:
      - db
    environment:
      FLASK_APP: app.py
      FLASK_ENV: development
    volumes:
      - .:/app
    networks:
      - marketmaster-network

volumes:
  postgres_data:

networks:
  marketmaster-network:
    external: true

To start the service using Docker, run:

docker-compose up -d

---

## API Endpoints

### Inventory Management:
- **GET /mm-inventory/**  
  Retrieves a list of all product items or allows filtering by attributes such as product name, category, description, and brand.  
  Example:  
  curl http://localhost:5705/mm-inventory/?name=productname

- **POST /mm-inventory/**  
  Allows users to create a new product item record in the inventory.  
  Example:  
  curl -X POST http://localhost:5705/mm-inventory/ -d '{"productid": 1, "storeid": 1, "price": 9.99, "stock": 100}'

- **GET /mm-inventory/{id}**  
  Retrieves detailed information for a product item by its unique identifier.  
  Example:  
  curl http://localhost:5705/mm-inventory/1

- **PUT /mm-inventory/{id}**  
  Updates a product item by its unique identifier.  
  Example:  
  curl -X PUT http://localhost:5705/mm-inventory/1 -d '{"price": 12.99, "stock": 50}'

- **DELETE /mm-inventory/{id}**  
  Deletes a product item by its unique identifier.  
  Example:  
  curl -X DELETE http://localhost:5705/mm-inventory/1

---

## Pact Provider Verification

The `mm-inventory` service uses **Pact** for contract testing to ensure that the interactions between the inventory service and its consumers are valid and verified.

### Pact Setup

Pact is configured in the `mm-inventory/pact` directory, and contract tests are executed using Mocha. The service verifies the contract against the Pact broker.

### Pact Dependencies:

{
  "name": "pact",
  "version": "1.0.0",
  "scripts": {
    "test": "mocha --recursive ./tests/*.spec.js"
  },
  "devDependencies": {
    "@pact-foundation/pact": "^13.1.3",
    "@pact-foundation/pact-node": "^10.18.0",
    "axios": "^1.7.7",
    "chai": "^5.1.1",
    "dotenv": "^16.4.5",
    "mocha": "^10.7.3"
  }
}

### Running Pact Verification

To verify the contracts between the `mm-inventory` service and its consumers, use the following command:

npm test

Pact will retrieve the contract from the Pact broker and verify that the `mm-inventory` service complies with the expected interactions.

---

## Running the Flask Application Locally

If you prefer to run the service without Docker, follow the steps below.

### Step 1: Install Dependencies

Make sure you have Python 3 and `pip` installed. Then, install the required dependencies:

pip install -r requirements.txt

### Step 2: Configure Environment Variables

Create a `.env` file in the root of the project with the following content:

FLASK_APP=app.py  
FLASK_ENV=development  
DATABASE_URL=postgresql://marketmaster:password@localhost:5436/postgres

### Step 3: Run the Application

With the environment variables set, you can run the Flask application:

flask run

By default, the service will be accessible at `http://localhost:5705`.

---

## Additional Information

This microservice is part of the Market Master system, providing inventory management features that are essential for tracking product availability and pricing. It is closely integrated with other services in the system, such as the `mm-product` and `mm-store` services.

For more details about the Market Master project and to explore other microservices, visit the respective repositories:

- [mm-product](https://github.com/MarketMasterPlus/mm-product)
- [mm-store](https://github.com/MarketMasterPlus/mm-store)
- [mm-shopping-cart](https://github.com/MarketMasterPlus/mm-shopping-cart)
- [mm-address](https://github.com/MarketMasterPlus/mm-address)
- [mm-customer](https://github.com/MarketMasterPlus/mm-customer)
- [mm-pact-broker](https://github.com/MarketMasterPlus/mm-pact-broker)
- [mm-ui](https://github.com/MarketMasterPlus/mm-ui)

For any further questions, feel free to open an issue on GitHub or consult the provided documentation within each repository.

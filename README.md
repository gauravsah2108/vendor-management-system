
# Vendor Management System

The Vendor Management System is a Django web application that provides APIs for managing vendor profiles, purchase orders, and performance metrics.

## Installation

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    ```

2. **Navigate to the project directory:**

    ```bash
    cd vendor_management_system
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

## Running the Development Server

Start the development server with the following command:

```bash
python manage.py runserver
```

The server will start running at `http://127.0.0.1:8000/`.

## API Endpoints

### Vendor Profile Management

- **Create a new vendor:** `POST /api/vendors/`
- **List all vendors:** `GET /api/vendors/`
- **Retrieve a specific vendor's details:** `GET /api/vendors/{vendor_id}/`
- **Update a vendor's details:** `PUT /api/vendors/{vendor_id}/`
- **Delete a vendor:** `DELETE /api/vendors/{vendor_id}/`

### Purchase Order Tracking

- **Create a new purchase order:** `POST /api/purchase_orders/`
- **List all purchase orders:** `GET /api/purchase_orders/`
- **Retrieve details of a specific purchase order:** `GET /api/purchase_orders/{po_id}/`
- **Update a purchase order:** `PUT /api/purchase_orders/{po_id}/`
- **Delete a purchase order:** `DELETE /api/purchase_orders/{po_id}/`

### Vendor Performance Metrics

- **Retrieve performance metrics for a specific vendor:** `GET /api/vendors/{vendor_id}/performance/`

### Update Acknowledgment Endpoint

- **Acknowledge a purchase order:** `POST /api/purchase_orders/{po_id}/acknowledge/`

## Usage

1. **Use the provided API endpoints to interact with the Vendor Management System.**
2. **You can use tools like Postman or curl to make HTTP requests to the API endpoints.**
3. **Ensure you have appropriate permissions and authentication tokens to access protected endpoints.**

## Authentication

The API endpoints are secured using token-based authentication. To authenticate, include the token in the Authorization header of your HTTP requests:

```
Authorization: Token <your_token>
```

## Testing

You can run the unit tests to verify the functionality of the API endpoints:

```bash
python manage.py test
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

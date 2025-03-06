# OrderFood

OrderFood is a Django-based web application that allows customers to place food orders and restaurant owners to manage them. This repository focuses on the Admin View (see [Testing](#testing)), providing insights into order statuses and summaries.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Testing](#testing)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- Make and follow orders for customers.
- View and manage food orders for Admin.
- Track order statuses (Pending, Processing, Completed, Canceled).
- Generate visual summaries (bar and pie charts) using Pandas and Matplotlib.
- Filter today's orders separately for quick insights.

## Testing

To test the full functionality:
- Sign up with any account to test the customer view.
- Log in with the admin account 'http://127.0.0.1:8000/menu_admin/' to see the Admin View built by us.

## Installation

### Prerequisites

- Python 3.13+
- Django
- Virtual Environment (venv)
- Git

### Setup Instructions

```sh
# Clone the repository
git clone https://github.com/Sandarg95/SDEV220_FinalProject.git
cd SDEV220_FinalProject

# Switch to the Admin-View branch
git checkout Admin-View

# Create and activate a virtual environment
python -m venv myvenv1
source myvenv1/bin/activate  # On Windows use: myvenv1\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a superuser (for admin access)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

## Usage

1. Log in to the Django admin panel at `http://127.0.0.1:8000/admin/`
2. Log in with the admin account bilt by us to see the Admin View at '[http://127.0.0.1:8000/login/](http://127.0.0.1:8000/menu_admin/)' 
3. Navigate to create and update orders, edit foods, and to view summary on 'menu-admin'.
4. Visit `http://127.0.0.1:8000/summary/` to view order statistics and charts.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to your branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License.

## Contact

For questions or suggestions, reach out to [Daniel Santana](https://github.com/Sandarg95) or [Coleman Matthew Dean Ransford](https://github.com/Heavensdoorlmao) .


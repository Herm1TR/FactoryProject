# Factory Project

## Project Introduction and Background

This project aims to demonstrate how to apply logistics transportation and optimization algorithms within the Django framework. Through this project, you can see how to combine user authentication, data visualization, and complex algorithms to simulate route planning and cost comparison in actual logistics transportation, thereby improving delivery efficiency. This project also showcases how to use Django's powerful ORM and template system to build a clearly structured and easily maintainable application.

## Main Features

* **User Authentication and Registration:** Utilizing Django's built-in authentication system to provide registration, login, and logout functions, protecting sensitive pages of the application.
* **Dashboard Displaying Dock Operational Status:** Providing current load and historical shipping data for each dock, allowing users to get a clear overview of dock operations at a glance.
* **Cost Comparison and Optimized Route Calculation:** Showcasing changes in logistics transportation costs by comparing original shipping routes with routes calculated by optimization algorithms, presented in chart form.
* **Dynamic Display of Robot Delivery Trajectories:** Displaying the movement trajectories of robots during the delivery process in animated form, intuitively presenting logistics operations.

## Technology Stack

* **Backend Framework:** Django
* **Database:** SQLite (used during development, can be adjusted as needed)
* **Frontend:** Using Django template language combined with basic HTML/CSS/JavaScript
* **Other Packages:**
   * python-decouple or django-environ (for managing sensitive information and environment variables)

## Installation and Execution Steps

1. **Create a Virtual Environment:**
   ```bash
   python -m venv env
   ```

2. **Activate the Virtual Environment:**
   * Windows:
   ```bash
   env\Scripts\activate
   ```
   * macOS/Linux:
   ```bash
   source env/bin/activate
   ```

3. **Install Dependencies:** Ensure all dependencies are listed in the `requirements.txt` file, then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables:** Create a `.env` file in the project root directory, and add:
   ```ini
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```
   Note: Add the `.env` file to `.gitignore` to prevent sensitive information from being uploaded to GitHub.

5. **Run Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application:** Open a browser and go to http://127.0.0.1:8000 to view the project.

## Project Structure

* **factory_project/**
   * `settings.py`: Project configuration file, including database settings, application installation, environment variable reading, etc.
   * `urls.py`: Global URL routing configuration.
   * `manage.py`: Django command-line tool.
* **logistics/**
   * `models.py`: Defines data models for docks, robots, delivery records, and warehouses.
   * `views.py`: View functions for each page, responsible for handling requests and returning data.
   * `optimization.py`: Contains functions related to logistics optimization algorithms.
   * Other templates and static files: For frontend page display.
   * **management/commands/**
      * `cleardata.py`: Used to clear data in the system
      * `populatedata.py`: Used to generate simulated delivery data

## Management Commands

The project includes two custom management commands for data management and testing:

### cleardata

```bash
python manage.py cleardata [--logisticsdata] [--dock]
```

This command is used to clear data in the system and has the following parameters:
- `--logisticsdata`: Clear all LogisticsData records
- `--dock`: Clear all Dock data
- At least one parameter must be specified

Examples:
```bash
# Clear all delivery records
python manage.py cleardata --logisticsdata

# Clear all dock data
python manage.py cleardata --dock

# Clear both delivery records and dock data
python manage.py cleardata --logisticsdata --dock
```

### populatedata

```bash
python manage.py populatedata
```

This command is used to generate original simulated delivery data (without considering whether the dock is fully loaded) to demonstrate the differences before and after optimization. Running this command will:

1. Create or update four dock data entries (Dock A, B, C, D)
2. Create or update two robot data entries (Robot001, Robot002)
3. Create or confirm warehouse data (Warehouse, fixed at coordinates origin 0,0)
4. Simulate 10 deliveries, with each delivery carrying up to 5 units of cargo
5. Each delivery starts from the warehouse, randomly selecting docks for delivery without considering whether the dock is already fully loaded
6. After each delivery is completed, the robot returns to the warehouse

This command is very useful for testing system functionality and visualization effects, especially when comparing delivery routes and cost differences before and after optimization.

## Configuration Settings

Sensitive information (such as SECRET_KEY) is no longer hardcoded in the code but is managed using environment variables. One of the following methods is recommended:

* **python-decouple:** In `settings.py`, use:
  ```python
  from decouple import config
  SECRET_KEY = config('SECRET_KEY')
  ```

* **django-environ:** In `settings.py`, use:
  ```python
  import environ
  env = environ.Env(DEBUG=(bool, False))
  environ.Env.read_env()
  SECRET_KEY = env('SECRET_KEY')
  ```

Make sure the `.env` file is not uploaded to GitHub by adding to `.gitignore`:
```
.env
```

## Contribution Guidelines

If you are interested in contributing to this project, please follow these steps:

1. Fork this repository.
2. Create your feature branch (`git checkout -b feature/your-feature-description`).
3. Commit your changes (`git commit -am 'Add feature or fix bug'`).
4. Push to your branch (`git push origin feature/your-feature-description`).
5. Submit a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

# techltd
# Sales Data Analysis REST API
<p> This project provides a REST API to manipulate sales data of a super shop. It also includes an API to generate a PDF report containing useful information about the sales data. </p>

<h6>Technology Stack</h6>
<li>Django</li>
<li>Django Rest Framework</li>
<li>Matplotlib</li>
<li>ReportLab</li>

<h6> Installation and Setup </h6>
<li>Clone the repository</li>
<li> Create a virtual environment using virtualenv env and activate it using source .\env\Scripts\activate </li>
<li>Install the dependencies using pip install -r requirements.txt</li>
<li>Create a PostgreSQL database and update the DATABASES configuration in settings.py accordingly</li>
<li>Run migrations using python manage.py migrate</li>
<li>create super user  python manage.py createsuperuser  then login admin page</li>
<li>Load csv file sales_data.csv</li>
<li>Start the development server using python manage.py runserver </li>


<h3> API Endpoints </h5>
<h6> Authentication Endpoints</h6>
<li> POST /api/auth/register/ - Register a new user</li>
<li>POST /api/auth/login/ - Obtain a new access token</li>
<h6>Sales Data Endpoints</h6>
<li>GET /api/sales/ - List all sales data</li>
<li>POST /api/sales/ - Create a new sales data</li>
<li>GET /api/sales/<int:pk>/ - Retrieve a single sales data by primary key</li>
<li>PUT /api/sales/<int:pk>/ - Update a single sales data by primary key</li>
<li>DELETE /api/sales/<int:pk>/ - Delete a single sales data by primary key</li>
<h6>Report Endpoint</h6>
<li>GET /api/generate_report/ - Generate a PDF report containing useful information about the sales data</li>
  
<h4>Report Information</h4>
<p>The generated PDF report contains the following information:</p>

<li>Total number of orders count per year</li>
<li>Total count of distinct customers</li>
<li>Top 3 customers who have ordered the most with their total amount of transactions</li>
<li>Customer Transactions per Year (from the beginning year to last year)</li>
<li>Most selling items sub-category names</li>
<li>Region basis sales performance pie chart</li>
<li>Sales performance line chart over the years</li>

<h3> Thank you 👍👍, View my code </h3>

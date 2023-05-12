from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from rest_framework import viewsets
from .serializers import SalesSerializer

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import pandas as pd
import matplotlib.pyplot as plt
from django.db.models import Count, Sum, Q
from sales.models import Sales
from rest_framework.views import APIView
import base64
import matplotlib.pyplot as plt


class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer


class SalesReport(APIView):
    
    def get(self, request, *args, **kwargs):
        sales_data = Sales.objects.all().values()
        
        # Convert sales data to pandas DataFrame
        df = pd.DataFrame.from_records(sales_data)
        # Convert 'order_date' column to datetime type
        df['order_date'] = pd.to_datetime(df['order_date'])

        
        # Total number of orders count per year
        orders_count_per_year = df.groupby(df['order_date'].dt.year)['id'].count()
        
        # Total count of distinct customers
        distinct_customers_count = df['customer_id'].nunique()

        df['sales']=df['sales'].astype(float)
        
        # Top 3 customers who have ordered the most with their total amount of transactions
        top_customers = df.groupby(['customer_id', 'customer_name'])['sales'].agg(['sum', 'count']).reset_index()
        top_customers = top_customers.sort_values('sum', ascending=False).head(3)
        
        # Customer Transactions per Year (from the beginning year to last year)
        customer_transactions_per_year = df.groupby([df['order_date'].dt.year, 'customer_id'])['sales'].agg(['count', 'sum']).reset_index()
        customer_transactions_per_year = customer_transactions_per_year.rename(columns={'count': 'transactions_count', 'sum': 'transactions_amount'})
        
        # Convert 'sales' column to numeric type
        df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
        # Add the most selling items sub-category names
        top_subcategory_names = df.groupby('subcategory')['sales'].sum().nlargest(3).index.tolist()


        # Region basis sales performance pie chart
        region_sales = df.groupby('region')['sales'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')

        # Convert the figure to a base64-encoded image
        buffer = BytesIO()
        fig1.savefig(buffer, format='png')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.read()).decode()
        

        # Sales performance line chart over the years
        sales_performance = df.groupby(df['order_date'].dt.year)['sales'].sum()
        fig2, ax2 = plt.subplots()
        ax2.plot(sales_performance.index, sales_performance.values)
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Sales')
        ax2.set_title('Sales Performance over the Years')
        buffer = BytesIO()
        fig2.savefig(buffer, format='png')
        buffer.seek(0)
        sales_performance_line_chart = base64.b64encode(buffer.read()).decode('utf-8')
        
        # Prepare the context
        context = {
            'orders_count_per_year': orders_count_per_year,
            'distinct_customers_count': distinct_customers_count,
            'top_customers': top_customers,
            'customer_transactions_per_year': customer_transactions_per_year,
            'top_subcategory_names': top_subcategory_names,
            'region_sales_pie_chart': f"data:image/png;base64,{image_data}",
            'sales_performance_line_chart': f"data:image/png;base64,{sales_performance_line_chart}",
        }
        
        
        # Create a PDF report
        template = get_template('report_f.html')
        html = template.render(context)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), response)
        if not pdf.err:
            response = HttpResponse(response.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
            return response
        
        return HttpResponse("Error Generating PDF", status=400)

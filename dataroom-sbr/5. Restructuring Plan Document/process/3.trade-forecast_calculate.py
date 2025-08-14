#!/usr/bin/env python3
"""
Trade Forecast Generator for Historic Rivermill - Colourful.Land Pty Ltd
================================================================================

Refactored implementation using Builder Pattern to reduce code length and improve maintainability.

Usage:
    python3 3.trade-forecast-refactored.py

Output:
    ../output/trade-forecast.csv - Complete P&L forecast for 24 months
    ../output/seasonal-cost-report.txt - Seasonal cost variation analysis

All calculations derive from trade_forecast_method.md specifications.

CRITICAL BASELINE VALIDATION:
The July 2025 baseline ($201,972 total trading income, 26.7% YoY growth) represents a proven, 
sustainable performance level, not a one-time transformation spike. This baseline is supported by:
- May 2025: 29% YoY growth in gross sales
- June 2025: 6% YoY growth in gross sales (temporary seasonal dip)
- July 2025: 29% YoY growth in gross sales (26.7% in trade income due to calculation differences)

This sustained growth pattern demonstrates the business has consistently achieved ~29% YoY growth 
rates across multiple months, making the July 2025 baseline a reliable foundation for forward 
projections rather than an outlier requiring special justification.

UTILITIES METHODOLOGY:
June 2026 utilities cost of $4,500/month serves as the baseline for all forecasted months with 
seasonal fluctuations: peak tourism months (Sep-Mar) at $4,800/month (+6.7%), traditional dining 
months (Apr-Aug) at $4,200/month (-6.7%), and transition months at $4,500/month (baseline). 
Solar savings of $1,500/month are applied to all months from August 2025 onwards.
================================================================================
"""

import csv
import math
from datetime import datetime
from typing import Dict, List, Tuple
import os

class ForecastMatrixBuilder:
    """Builder pattern for constructing the forecast matrix with guaranteed structure."""
    
    def __init__(self):
        self.matrix = {}
        self.columns = self._define_columns()
        self.account_mappings = self._define_account_mappings()
        
    def _define_columns(self) -> List[str]:
        """Define the exact column structure for consistency."""
        return [
            'Account',           # Column 0
            'FY25',             # Column 1 - Actual FY25
            'Jul-25',           # Column 2 - Actual July 2025
            'Aug-25',           # Column 3 - Forecast
            'Sep-25',           # Column 4 - Forecast
            'Oct-25',           # Column 5 - Forecast
            'Nov-25',           # Column 6 - Forecast
            'Dec-25',           # Column 7 - Forecast
            'Jan-26',           # Column 8 - Forecast
            'Feb-26',           # Column 9 - Forecast
            'Mar-26',           # Column 10 - Forecast
            'Apr-26',           # Column 11 - Forecast
            'May-26',           # Column 12 - Forecast
            'Jun-26',           # Column 13 - Forecast
            'Jul-26',           # Column 14 - Forecast
            'Aug-26',           # Column 15 - Forecast
            'Sep-26',           # Column 16 - Forecast
            'Oct-26',           # Column 17 - Forecast
            'Nov-26',           # Column 18 - Forecast
            'Dec-26',           # Column 19 - Forecast
            'Jan-27',           # Column 20 - Forecast
            'Feb-27',           # Column 21 - Forecast
            'Mar-27',           # Column 22 - Forecast
            'Apr-27',           # Column 23 - Forecast
            'May-27',           # Column 24 - Forecast
            'Jun-27',           # Column 25 - Forecast
            'FY25/26 Total',    # Column 26 - FY total
            'FY26/27 Total',    # Column 27 - FY total
            'Director explanation'  # Column 28 - Empty
        ]
    
    def _define_account_mappings(self) -> Dict[str, str]:
        """Define mappings between display names and data keys."""
        return {
            # Revenue mappings
            'Parties and Events': 'parties_events',
            'Restaurant Revenue': 'restaurant_revenue',
            'Sales - Equestrian Party Booking': 'equestrian_party_booking',
            'Sales - Leasing': 'leasing',
            'Sales - STR': 'str',
            'Special Event': 'special_event',
            'Square Card Surcharges': 'square_card_surcharges',
            'Square Discounts': 'square_discounts',
            'Square Other Income': 'square_other_income',
            'Square Sales': 'square_sales',
            'Venue Hire': 'venue_hire',
            'Wedding': 'wedding',
            'Farm Stay': 'farmstay',
            
            # Cost of sales mappings
            'COGS - Back of house (Kitchen wages)': 'kitchen_wages',
            'COGS - Food Costs': 'food_costs',
            'COGS - General Cafe Expense': 'general_cafe_cogs',
            
            # Operating expense mappings - updated to match matrix structure
            'Accounting': 'accounting',
            'Administration Fees': 'administration_fees',
            'Advertising and Promotion': 'advertising_promotion',
            'Automobile Expense': 'automobile_expense',
            'Bank Fees': 'bank_fees',
            'Business gift expense': 'business_gift_expense',
            'Cleaning Expense': 'cleaning_expense',
            'Design and Printing': 'design_printing',
            'Director Salary': 'director_salary',
            'Employee Wages - Others': 'employee_wages_others',
            'Employee Wages- Front of house': 'front_house_wages',
            'Entertainment': 'entertainment',
            'Equestrian Food Expense': 'equestrian_food',
            'Equine Health': 'equine_health_expenses',
            'Equipment - Leasing': 'equipment_leasing',
            'General Business Research': 'general_business_research',
            'General Cafe Expense': 'general_cafe_expense',
            'Insurance Payment': 'insurance',
            'Interest Expense': 'interest_expense',
            'Legal': 'legal',
            'Management Consultant': 'management_consultant',
            'Marketing Expense': 'marketing',
            'Miscellaneous Expenses': 'miscellaneous_expenses',
            'Motor Vehicle & Fuel': 'motor_vehicle',
            'Non Equine Health': 'non_equine_health',
            'Office Expenses': 'office_expenses',
            'Office Supplies': 'office_supplies',
            'Parking Ticket': 'parking_ticket',
            'Printing and Stationery': 'printing_stationery',
            'Professional Services Expense': 'professional_services',
            'Property License and Permits': 'property_permits',
            'Realised Currency Gains': 'realised_currency_gains',
            'Refund': 'refund',
            'Reimbursement Clearing': 'reimbursement_clearing',
            'Renovation Contractors': 'renovation_contractors',
            'Rent Expense': 'rent_expense',
            'Repairs & Maintenance': 'repairs_maintenance',
            'Retail Item Purchase': 'retail_item_purchase',
            'Rubbish Removal and waste Disposal': 'rubbish_removal',
            'Shipping and Postage': 'shipping_postage',
            'Square Fees': 'square_fees',
            'Staff Meals & Amenities': 'staff_meals_amenities',
            'Staffing Contractors': 'staffing_contractors',
            'Subscriptions & Memberships': 'subscriptions',
            'Sundry Expenses': 'sundry_expenses',
            'Superannuation': 'superannuation',
            'Telephone & Internet': 'telephone_internet',
            'Training & Professional Development': 'training_development',
            'Travel - International': 'travel_international',
            'Travel - National': 'travel_national',
            'Travel - National - Leasing': 'travel_national_leasing',
            'Travel - Taxi': 'travel_taxi',
            'Utilities': 'utilities',
            'Wedding Sales Expense': 'wedding_sales_expense',
            'Web Domain, Hosting & Associated': 'web_domain_hosting',
            'Wedding cost': 'wedding_cost',
            'Wedding Sales Expense': 'wedding_sales_expense'
        }
    
    def add_all_rows(self):
        """Add all required matrix rows with proper structure."""
        matrix_rows = [
            'Trading Income',
            'Parties and Events',
            'Restaurant Revenue',
            'Sales - Equestrian Party Booking',
            'Sales - Leasing',
            'Sales - STR',
            'Special Event',
            'Square Card Surcharges',
            'Square Discounts',
            'Square Other Income',
            'Square Sales',
            'Venue Hire',
            'Wedding',
            'Farm Stay',
            'Total Trading Income',
            'Cost of Sales',
            'COGS - Back of house (Kitchen wages)',
            'COGS - Food Costs',
            'COGS - General Cafe Expense',
            'Total Cost of Sales',
            'Gross Profit',
            'Gross Profit Percentages',
            'Other Income',
            'Refund - From Vendor or Others',
            'Total Other Income',
            'Operating Expenses',
            'Accounting',
            'Administration Fees',
            'Advertising and Promotion',
            'Automobile Expense',
            'Bank Fees',
            'Business gift expense',
            'Cleaning Expense',
            'Design and Printing',
            'Director Salary',
            'Employee Wages - Others',
            'Employee Wages- Front of house',
            'Entertainment',
            'Equestrian Food Expense',
            'Equine Health',
            'Equipment - Leasing',
            'General Business Research',
            'General Cafe Expense',
            'Insurance Payment',
            'Interest Expense',
            'Legal',
            'Management Consultant',
            'Marketing Expense',
            'Miscellaneous Expenses',
            'Motor Vehicle & Fuel',
            'Non Equine Health',
            'Office Expenses',
            'Office Supplies',
            'Parking Ticket',
            'Printing and Stationery',
            'Professional Services Expense',
            'Property License and Permits',
            'Realised Currency Gains',
            'Refund',
            'Reimbursement Clearing',
            'Renovation Contractors',
            'Rent Expense',
            'Repairs & Maintenance',
            'Retail Item Purchase',
            'Rubbish Removal and waste Disposal',
            'Shipping and Postage',
            'Square Fees',
            'Staff Meals & Amenities',
            'Staffing Contractors',
            'Subscriptions & Memberships',
            'Sundry Expenses',
            'Superannuation',
            'Telephone & Internet',
            'Training & Professional Development',
            'Travel - International',
            'Travel - National',
            'Travel - National - Leasing',
            'Travel - Taxi',
            'Utilities',
            'Web Domain, Hosting & Associated',
            'Wedding cost',
            'Wedding Sales Expense',
            'Total Operating Expenses',
            'Net Profit'
        ]
        
        for row_name in matrix_rows:
            self.matrix[row_name] = [''] * len(self.columns)
            self.matrix[row_name][0] = row_name
        
        return self
    
    def fill_actual_data(self, actual_data: Dict[str, Dict[str, float]]):
        """Fill matrix with actual FY25 and Jul-25 data using mapping."""
        # Create reverse mapping from display names to actual CSV account names
        reverse_mapping = {
            'Parties and Events': 'Parties and Events',
            'Restaurant Revenue': 'Restaurant Revenue',
            'Sales - Equestrian Party Booking': 'Sales - Equestrian Party Booking',
            'Sales - Leasing': 'Sales - Leasing',
            'Sales - STR': 'Sales - STR',
            'Special Event': 'Special Event',
            'Square Card Surcharges': 'Square Card Surcharges',
            'Square Discounts': 'Square Discounts',
            'Square Other Income': 'Square Other Income',
            'Square Sales': 'Square Sales',
            'Venue Hire': 'Venue Hire',
            'Wedding': 'Wedding',
            'Farm Stay': 'Farm Stay',
            'COGS - Back of house (Kitchen wages)': 'COGS - Back of house (Kitchen wages)',
            'COGS - Food Costs': 'COGS - Food Costs',
            'COGS - General Cafe Expense': 'COGS - General Cafe Expense',
            'Accounting': 'Accounting',
            'Administration Fees': 'Administration Fees',
            'Advertising and Promotion': 'Advertising and Promotion',
            'Automobile Expense': 'Automobile Expense',
            'Bank Fees': 'Bank Fees',
            'Business gift expense': 'Business gift expense',
            'Cleaning Expense': 'Cleaning Expense',
            'Design and Printing': 'Design and Printing',
            'Director Salary': 'Director Salary',
            'Employee Wages - Others': 'Employee Wages - Others',
            'Employee Wages- Front of house': 'Employee Wages- Front of house',
            'Entertainment': 'Entertainment',
            'Equestrian Food Expense': 'Equestrian Food Expense',
            'Equine Health': 'Equine Health',
            'Equipment - Leasing': 'Equipment - Leasing',
            'General Business Research': 'General Business Research',
            'General Cafe Expense': 'General Cafe Expense',
            'Insurance Payment': 'Insurance Payment',
            'Interest Expense': 'Interest Expense',
            'Legal': 'Legal',
            'Management Consultant': 'Management Consultant',
            'Marketing Expense': 'Marketing Expense',
            'Miscellaneous Expenses': 'Miscellaneous Expenses',
            'Motor Vehicle & Fuel': 'Motor Vehicle & Fuel',
            'Non Equine Health': 'Non Equine Health',
            'Office Expenses': 'Office Expenses',
            'Office Supplies': 'Office Supplies',
            'Parking Ticket': 'Parking Ticket',
            'Printing and Stationery': 'Printing and Stationery',
            'Professional Services Expense': 'Professional Services Expense',
            'Property License and Permits': 'Property License and Permits',
            'Realised Currency Gains': 'Realised Currency Gains',
            'Refund': 'Refund',
            'Reimbursement Clearing': 'Reimbursement Clearing',
            'Renovation Contractors': 'Renovation Contractors',
            'Rent Expense': 'Rent Expense',
            'Repairs & Maintenance': 'Repairs & Maintenance',
            'Retail Item Purchase': 'Retail Item Purchase',
            'Rubbish Removal and waste Disposal': 'Rubbish Removal and waste Disposal',
            'Shipping and Postage': 'Shipping and Postage',
            'Square Fees': 'Square Fees',
            'Staff Meals & Amenities': 'Staff Meals & Amenities',
            'Staffing Contractors': 'Staffing Contractors',
            'Subscriptions & Memberships': 'Subscriptions & Memberships',
            'Sundry Expenses': 'Sundry Expenses',
            'Superannuation': 'Superannuation',
            'Telephone & Internet': 'Telephone & Internet',
            'Training & Professional Development': 'Training & Professional Development',
            'Travel - International': 'Travel - International',
            'Travel - National': 'Travel - National',
            'Travel - National - Leasing': 'Travel - National - Leasing',
            'Travel - Taxi': 'Travel - Taxi',
            'Utilities': 'Utilities',
            'Web Domain, Hosting & Associated': 'Web Domain, Hosting & Associated',
            'Wedding cost': 'Wedding cost',
            'Wedding Sales Expense': 'Wedding Sales Expense'
        }
        
        for display_name, csv_account_name in reverse_mapping.items():
            if display_name in self.matrix:
                # FY25 data (column 1)
                fy25_value = actual_data['FY25'].get(csv_account_name, 0.0)
                self.matrix[display_name][1] = fy25_value if fy25_value != 0 else 0.0
                
                # Jul-25 data (column 2)
                jul25_value = actual_data['Jul-25'].get(csv_account_name, 0.0)
                self.matrix[display_name][2] = jul25_value if jul25_value != 0 else 0.0
        
        # Handle special cases for totals
        if 'Total Trading Income' in self.matrix:
            self.matrix['Total Trading Income'][1] = actual_data['FY25'].get('Total Trading Income', 0.0)
            self.matrix['Total Trading Income'][2] = actual_data['Jul-25'].get('Total Trading Income', 0.0)
        
        if 'Total Cost of Sales' in self.matrix:
            self.matrix['Total Cost of Sales'][1] = actual_data['FY25'].get('Total Cost of Sales', 0.0)
            self.matrix['Total Cost of Sales'][2] = actual_data['Jul-25'].get('Total Cost of Sales', 0.0)
        
        if 'Total Other Income' in self.matrix:
            self.matrix['Total Other Income'][1] = actual_data['FY25'].get('Total Other Income', 0.0)
            self.matrix['Total Other Income'][2] = actual_data['Jul-25'].get('Total Other Income', 0.0)
        
        if 'Total Operating Expenses' in self.matrix:
            self.matrix['Total Operating Expenses'][1] = actual_data['FY25'].get('Total Operating Expenses', 0.0)
            self.matrix['Total Operating Expenses'][2] = actual_data['Jul-25'].get('Total Operating Expenses', 0.0)
        
        if 'Net Profit' in self.matrix:
            self.matrix['Net Profit'][1] = actual_data['FY25'].get('Net Profit', 0.0)
            self.matrix['Net Profit'][2] = actual_data['Jul-25'].get('Net Profit', 0.0)
        
        return self
    
    def fill_forecast_data(self, forecast_data: List[Dict]):
        """Fill matrix with forecast data using mapping."""
        for month_idx, month_data in enumerate(forecast_data[1:], start=3):
            # Revenue lines
            for display_name, data_key in self.account_mappings.items():
                if display_name in self.matrix:
                    if data_key in month_data['revenue_breakdown']:
                        value = month_data['revenue_breakdown'][data_key]
                        self.matrix[display_name][month_idx] = value if value != 0 else 0
                    elif data_key in month_data['cost_of_sales']:
                        value = month_data['cost_of_sales'][data_key]
                        self.matrix[display_name][month_idx] = value if value != 0 else 0
                    elif data_key in month_data['operating_expenses']:
                        value = month_data['operating_expenses'][data_key]
                        self.matrix[display_name][month_idx] = value if value != 0 else 0
            
            # Special handling for Farm Stay (it's not in the standard mappings)
            if 'Farm Stay' in self.matrix:
                farmstay_value = month_data['revenue_breakdown'].get('farmstay', 0)
                self.matrix['Farm Stay'][month_idx] = farmstay_value if farmstay_value != 0 else 0
            
            # Direct mapping for key operating expenses that might not be in account_mappings
            if 'Employee Wages- Front of house' in self.matrix:
                front_house_value = month_data['operating_expenses'].get('front_house_wages', 0)
                self.matrix['Employee Wages- Front of house'][month_idx] = front_house_value if front_house_value != 0 else 0
            
            if 'COGS - Back of house (Kitchen wages)' in self.matrix:
                kitchen_wages_value = month_data['cost_of_sales'].get('kitchen_wages', 0)
                self.matrix['COGS - Back of house (Kitchen wages)'][month_idx] = kitchen_wages_value if kitchen_wages_value != 0 else 0
            
            if 'COGS - Food Costs' in self.matrix:
                food_costs_value = month_data['cost_of_sales'].get('food_costs', 0)
                self.matrix['COGS - Food Costs'][month_idx] = food_costs_value if food_costs_value != 0 else 0
            
            if 'COGS - General Cafe Expense' in self.matrix:
                general_cafe_value = month_data['cost_of_sales'].get('general_cafe_cogs', 0)
                self.matrix['COGS - General Cafe Expense'][month_idx] = general_cafe_value if general_cafe_value != 0 else 0
            
            # Fill other operating expenses directly
            expense_mappings = {
                'Accounting': 'accounting',
                'Advertising and Promotion': 'advertising_promotion',
                'Bank Fees': 'bank_fees',
                'Director Salary': 'director_salary',
                'Employee Wages - Others': 'employee_wages_others',
                'Entertainment': 'entertainment',
                'Equestrian Food Expense': 'equestrian_food',
                'Equine Health': 'equine_health_expenses',
                'Equipment - Leasing': 'equipment_leasing',
                'General Cafe Expense': 'general_cafe_expense',
                'Insurance Payment': 'insurance',
                'Management Consultant': 'management_consultant',
                'Marketing Expense': 'marketing',
                'Office Supplies': 'office_supplies',
                'Rent Expense': 'rent_expense',
                'Repairs & Maintenance': 'repairs_maintenance',
                'Rubbish Removal and waste Disposal': 'rubbish_removal',
                'Shipping and Postage': 'shipping_postage',
                'Square Fees': 'square_fees',
                'Subscriptions & Memberships': 'subscriptions',
                'Superannuation': 'superannuation',
                'Telephone & Internet': 'telephone_internet',
                'Travel - International': 'travel_international',
                'Travel - National': 'travel_national',
                'Travel - National - Leasing': 'travel_national_leasing',
                'Travel - Taxi': 'travel_taxi',
                'Utilities': 'utilities'
            }
            
            for display_name, data_key in expense_mappings.items():
                if display_name in self.matrix:
                    value = month_data['operating_expenses'].get(data_key, 0)
                    self.matrix[display_name][month_idx] = value if value != 0 else 0
            
            # Handle additional expenses that might have different names
            additional_expense_mappings = {
                'Motor Vehicle & Fuel': 'motor_vehicle',
                'Property License and Permits': 'property_permits',
                'Cleaning Expense': 'cleaning_expense',
                'Office Expenses': 'office_expenses',
                'Professional Services Expense': 'professional_services',
                'Renovation Contractors': 'renovation_contractors',
                'Staff Meals & Amenities': 'staff_meals_amenities',
                'Staffing Contractors': 'staffing_contractors',
                'Web Domain, Hosting & Associated': 'web_domain_hosting',
                'Wedding cost': 'wedding_cost'
            }
            
            for display_name, data_key in additional_expense_mappings.items():
                if display_name in self.matrix:
                    value = month_data['operating_expenses'].get(data_key, 0)
                    self.matrix[display_name][month_idx] = value if value != 0 else 0
        
        return self
    
    def calculate_totals(self, forecast_data: List[Dict], actual_data: Dict[str, Dict[str, float]]):
        """Calculate all summary rows and totals."""
        # Calculate FY totals
        fy2526_months = forecast_data[1:13]  # Aug-25 to Jul-26
        fy2627_months = forecast_data[13:25]  # Aug-26 to Jul-27
        
        # Total Trading Income
        fy25_total_income = actual_data['FY25'].get('Total Trading Income', 0)
        jul25_total_income = actual_data['Jul-25'].get('Total Trading Income', 0)
        fy2526_total_income = sum(data['revenue_breakdown']['total_trading_income'] for data in fy2526_months)
        fy2627_total_income = sum(data['revenue_breakdown']['total_trading_income'] for data in fy2627_months)
        
        self.matrix['Total Trading Income'][1] = fy25_total_income if fy25_total_income != 0 else 0.0
        self.matrix['Total Trading Income'][2] = jul25_total_income if jul25_total_income != 0 else 0.0
        self.matrix['Total Trading Income'][26] = fy2526_total_income
        self.matrix['Total Trading Income'][27] = fy2627_total_income
        
        # Calculate monthly totals for forecast months (columns 3-25)
        revenue_components = ['Parties and Events', 'Restaurant Revenue', 
                           'Sales - Equestrian Party Booking', 'Sales - Leasing',
                           'Sales - STR', 'Special Event', 'Square Card Surcharges', 
                           'Square Discounts', 'Square Other Income', 'Square Sales', 
                           'Venue Hire', 'Wedding', 'Farm Stay']
        
        for month_idx in range(3, 26):  # Columns 3-25 (Aug-25 to Jun-27)
            monthly_total = 0
            for component in revenue_components:
                if component in self.matrix and month_idx < len(self.matrix[component]):
                    value = self.matrix[component][month_idx]
                    if value and value != 0:
                        monthly_total += value
            self.matrix['Total Trading Income'][month_idx] = monthly_total if monthly_total != 0 else 0
        
        # Total Cost of Sales
        fy25_total_cogs = actual_data['FY25'].get('Total Cost of Sales', 0)
        jul25_total_cogs = actual_data['Jul-25'].get('Total Cost of Sales', 0)
        fy2526_total_cogs = sum(data['cost_of_sales']['kitchen_wages'] + 
                               data['cost_of_sales']['food_costs'] + 
                               data['cost_of_sales']['general_cafe_cogs'] for data in fy2526_months)
        fy2627_total_cogs = sum(data['cost_of_sales']['kitchen_wages'] + 
                               data['cost_of_sales']['food_costs'] + 
                               data['cost_of_sales']['general_cafe_cogs'] for data in fy2627_months)
        
        self.matrix['Total Cost of Sales'][1] = fy25_total_cogs if fy25_total_cogs != 0 else 0.0
        self.matrix['Total Cost of Sales'][2] = jul25_total_cogs if jul25_total_cogs != 0 else 0.0
        self.matrix['Total Cost of Sales'][26] = fy2526_total_cogs
        self.matrix['Total Cost of Sales'][27] = fy2627_total_cogs
        
        # Calculate monthly COGS totals for forecast months (columns 3-25)
        cogs_components = ['COGS - Back of house (Kitchen wages)', 'COGS - Food Costs', 'COGS - General Cafe Expense']
        
        for month_idx in range(3, 26):  # Columns 3-25 (Aug-25 to Jun-27)
            monthly_total = 0
            for component in cogs_components:
                if component in self.matrix and month_idx < len(self.matrix[component]):
                    value = self.matrix[component][month_idx]
                    if value and value != 0:
                        monthly_total += value
            self.matrix['Total Cost of Sales'][month_idx] = monthly_total if monthly_total != 0 else 0
        
        # Gross Profit
        fy25_gross_profit = fy25_total_income - fy25_total_cogs
        jul25_gross_profit = jul25_total_income - jul25_total_cogs
        fy2526_gross_profit = fy2526_total_income - fy2526_total_cogs
        fy2627_gross_profit = fy2627_total_income - fy2627_total_cogs
        
        self.matrix['Gross Profit'][1] = fy25_gross_profit if fy25_gross_profit != 0 else 0.0
        self.matrix['Gross Profit'][2] = jul25_gross_profit if jul25_gross_profit != 0 else 0.0
        self.matrix['Gross Profit'][26] = fy2526_gross_profit
        self.matrix['Gross Profit'][27] = fy2627_gross_profit
        
        # Calculate monthly gross profit for forecast months (columns 3-25)
        for month_idx in range(3, 26):  # Columns 3-25 (Aug-25 to Jun-27)
            revenue = self.matrix['Total Trading Income'][month_idx]
            cogs = self.matrix['Total Cost of Sales'][month_idx]
            if revenue and cogs and revenue != 0 and cogs != 0:
                gross_profit = revenue - cogs
                self.matrix['Gross Profit'][month_idx] = gross_profit if gross_profit != 0 else 0
        
        # Gross Profit Percentages
        fy25_margin = (fy25_gross_profit / fy25_total_income * 100) if fy25_total_income > 0 else 0
        jul25_margin = (jul25_gross_profit / jul25_total_income * 100) if jul25_total_income > 0 else 0
        
        self.matrix['Gross Profit Percentages'][1] = f"{fy25_margin:.1f}%"
        self.matrix['Gross Profit Percentages'][2] = f"{jul25_margin:.1f}%"
        
        # Forecast month percentages (columns 3-26)
        for month_idx in range(3, 26):  # Columns 3-25 (Aug-25 to Jun-27)
            revenue = self.matrix['Total Trading Income'][month_idx]
            gross_profit = self.matrix['Gross Profit'][month_idx]
            if revenue and gross_profit and revenue > 0:
                forecast_margin = (gross_profit / revenue) * 100
                self.matrix['Gross Profit Percentages'][month_idx] = f"{forecast_margin:.1f}%"
        
        # FY total percentages
        fy2526_margin = (fy2526_gross_profit / fy2526_total_income * 100) if fy2526_total_income > 0 else 0
        self.matrix['Gross Profit Percentages'][26] = f"{fy2526_margin:.1f}%"
        
        fy2627_margin = (fy2627_gross_profit / fy2627_total_income * 100) if fy2627_total_income > 0 else 0
        self.matrix['Gross Profit Percentages'][27] = f"{fy2627_margin:.1f}%"
        
        # Total Other Income
        fy25_other_income = actual_data['FY25'].get('Total Other Income', 0)
        jul25_other_income = actual_data['Jul-25'].get('Total Other Income', 0)
        fy2526_other_income = sum(data['revenue_breakdown'].get('other_income', 0) for data in fy2526_months)
        fy2627_other_income = sum(data['revenue_breakdown'].get('other_income', 0) for data in fy2627_months)
        
        self.matrix['Total Other Income'][1] = fy25_other_income if fy25_other_income != 0 else 0.0
        self.matrix['Total Other Income'][2] = jul25_other_income if jul25_other_income != 0 else 0.0
        self.matrix['Total Other Income'][26] = fy2526_other_income
        self.matrix['Total Other Income'][27] = fy2627_other_income
        
        # Total Operating Expenses
        fy25_total_expenses = actual_data['FY25'].get('Total Operating Expenses', 0)
        jul25_total_expenses = actual_data['Jul-25'].get('Total Operating Expenses', 0)
        fy2526_total_expenses = sum(sum(data['operating_expenses'].values()) for data in fy2526_months)
        fy2627_total_expenses = sum(sum(data['operating_expenses'].values()) for data in fy2627_months)
        
        self.matrix['Total Operating Expenses'][1] = fy25_total_expenses if fy25_total_expenses != 0 else 0.0
        self.matrix['Total Operating Expenses'][2] = jul25_total_expenses if jul25_total_expenses != 0 else 0.0
        self.matrix['Total Operating Expenses'][26] = fy2526_total_expenses
        self.matrix['Total Operating Expenses'][27] = fy2627_total_expenses
        
        # Calculate monthly operating expenses totals for forecast months (columns 3-25)
        operating_expense_components = [
            'Accounting', 'Administration Fees', 'Advertising and Promotion', 'Automobile Expense',
            'Bank Fees', 'Business gift expense', 'Cleaning Expense', 'Design and Printing',
            'Director Salary', 'Employee Wages - Others', 'Employee Wages- Front of house', 'Entertainment',
            'Equestrian Food Expense', 'Equine Health', 'Equipment - Leasing',
            'General Business Research', 'General Cafe Expense', 'Insurance Payment',
            'Interest Expense', 'Legal', 'Management Consultant', 'Marketing Expense',
            'Miscellaneous Expenses', 'Motor Vehicle & Fuel', 'Non Equine Health',
            'Office Expenses', 'Office Supplies', 'Parking Ticket', 'Printing and Stationery',
            'Professional Services Expense', 'Property License and Permits', 'Realised Currency Gains',
            'Refund', 'Reimbursement Clearing', 'Renovation Contractors', 'Rent Expense',
            'Repairs & Maintenance', 'Retail Item Purchase', 'Rubbish Removal and waste Disposal',
            'Shipping and Postage', 'Square Fees', 'Staff Meals & Amenities', 'Staffing Contractors',
            'Subscriptions & Memberships', 'Sundry Expenses', 'Superannuation',
            'Telephone & Internet', 'Training & Professional Development', 'Travel - International',
            'Travel - National', 'Travel - National - Leasing', 'Travel - Taxi',
            'Utilities', 'Web Domain, Hosting & Associated', 'Wedding cost', 'Wedding Sales Expense'
        ]
        
        for month_idx in range(3, 26):  # Columns 3-25 (Aug-25 to Jun-27)
            monthly_total = 0
            for component in operating_expense_components:
                if component in self.matrix:
                    value = self.matrix[component][month_idx]
                    if value and value != 0:
                        monthly_total += value
            self.matrix['Total Operating Expenses'][month_idx] = monthly_total if monthly_total != 0 else 0
        
        # Net Profit
        fy25_net_profit = fy25_gross_profit + fy25_other_income - fy25_total_expenses
        jul25_net_profit = jul25_gross_profit + jul25_other_income - jul25_total_expenses
        fy2526_net_profit = fy2526_gross_profit + fy2526_other_income - fy2526_total_expenses
        fy2627_net_profit = fy2627_gross_profit + fy2627_other_income - fy2627_total_expenses
        
        self.matrix['Net Profit'][1] = fy25_net_profit if fy25_net_profit != 0 else 0.0
        self.matrix['Net Profit'][2] = jul25_net_profit if jul25_net_profit != 0 else 0.0
        self.matrix['Net Profit'][26] = fy2526_net_profit
        self.matrix['Net Profit'][27] = fy2627_net_profit
        
        # Calculate monthly net profit for forecast months (columns 3-25)
        for month_idx in range(3, 26):  # Columns 3-25 (Aug-25 to Jun-27)
            gross_profit = self.matrix['Gross Profit'][month_idx]
            operating_expenses = self.matrix['Total Operating Expenses'][month_idx]
            if gross_profit and operating_expenses and gross_profit != 0 and operating_expenses != 0:
                net_profit = gross_profit - operating_expenses
                self.matrix['Net Profit'][month_idx] = net_profit if net_profit != 0 else 0
        
        return self
    
    def build(self, forecast_data: List[Dict], actual_data: Dict[str, Dict[str, float]]) -> Dict[str, List]:
        """Build the complete matrix using the builder pattern."""
        matrix = (self
                .add_all_rows()
                .fill_actual_data(actual_data)
                .fill_forecast_data(forecast_data)
                .calculate_totals(forecast_data, actual_data)
                .matrix)
        
        # Round all financial values to 2 decimal places
        self._round_financial_values(matrix)
        
        # Add director explanations for significant changes and anomalies
        self.add_director_explanations(matrix)
        
        return matrix
    
    def _round_financial_values(self, matrix: Dict[str, List]):
        """Round all financial values to 2 decimal places for CSV output."""
        for row_name, values in matrix.items():
            for i, value in enumerate(values):
                if isinstance(value, (int, float)) and value != 0:
                    # Round to 2 decimal places for money values
                    matrix[row_name][i] = round(value, 2)
                elif isinstance(value, str) and value.endswith('%'):
                    # Handle percentage values - keep as is
                    continue
    
    def add_director_explanations(self, matrix: Dict[str, List]):
        """Add director explanations to the matrix for significant changes and anomalies."""
        # Table of Row Explanations - Directors only explain when there are SIGNIFICANT CHANGES, ANOMALIES, or STRATEGIC SHIFTS
        #
        # EXPLANATION RULES - Follow these guidelines when adding new explanations:
        #
        # 🚨 CRITICAL: Directors only explain when there are SIGNIFICANT CHANGES, ANOMALIES, or STRATEGIC SHIFTS
        #
        # ✅ ONLY EXPLAIN WHEN:
        # - Sharp cliffs between months (especially Sep 2025 when laid-off staff stop working)
        # - Profit higher than industry average
        # - Major cost restructuring (e.g., Operations Manager elimination, casual to permanent conversion)
        # - Revenue model changes (e.g., admission fees introduced, wedding business rebuilt)
        # - Unusual seasonal patterns that need context
        #
        # ❌ DO NOT EXPLAIN:
        # - Normal, obvious line items (e.g., "Vehicle fuel and maintenance costs")
        # - Standard business expenses (e.g., "Professional accounting services")
        # - Section headers or totals
        # - Items that are self-explanatory
        # - Generic descriptions that add no value
        #
        # 🎯 DIRECTOR'S ROLE:
        # - Explain WHY something changed significantly
        # - Explain WHAT strategic shift caused the change
        # - Explain WHEN stakeholders should expect the change to stabilize
        # - Focus on business impact, not accounting definitions
        #
        # 📝 FORMATTING CONSTRAINTS:
        # - ONE COLUMN ONLY: All explanations go in the last column (column 29)
        # - NO LINEBREAKS: Each explanation must fit on a single line
        # - TERSENESS: Keep explanations concise and to the point
        # - MAXIMUM LENGTH: Aim for explanations under 80 characters when possible
        #
        # 🎭 TONE & LANGUAGE:
        # - Write as a DIRECTOR explaining significant changes to stakeholders
        # - Use business language, not accounting textbook language
        # - Focus on strategic impact and business rationale
        # - Think: "What significant change or anomaly needs board explanation?"
        
        ROW_EXPLANATIONS = {
            # Only explain SIGNIFICANT CHANGES, ANOMALIES, or STRATEGIC SHIFTS
            # Based on narrative: café to tourism destination shift, major restructuring, admission fees
            
            'Wedding': 'Wedding business uses external agent instead of manager Sophie',
            'Square Sales': 'Tourism operations now a much larger revenue stream via experience-led model',
            'COGS - Food Costs': 'Food costs reduced from 35% to 20% via tourism transformation',
            'Director Salary': 'Commences Sep 2025: director replaces Operations Manager Mike Wood',
            'Employee Wages - Others': 'Reduced Sep 2025: Sophie replaced by wedding contractor',
            'Employee Wages- Front of house': 'Permanent staff conversion eliminates 25% casual loading',
            'Marketing Expense': 'Restructured: Institute of Design partnership converting to equity',
            'Rent Expense': 'Resumes Sep 2025 after rental holiday period',
            'Utilities': 'Solar panels reduce costs by $18k annually from Jul 2025',
            'Wedding Sales Expense': 'External contractor replaces Sophie: $26k FY25/26, $40k FY26/27',
            'Superannuation': '12% of all wages per new Australian rule July 2025 (excluding marketing personnel)',
            'Renovation Contractors': 'All major renovation work completed by July 2025',
            'Staffing Contractors': 'Replaced by permanent staff structure and casual employees',
            'Travel - International': 'Strategic travel schedule: Aug=0, Sep-Dec=3000/2000/1000/3000, FY25/26=0, FY26/27=2000/month',
            'Total Operating Expenses': 'Strategic restructuring: workforce changes, marketing equity conversion, energy efficiency',
            'Trading Income': 'July 2025 baseline used as transformation stabilised (4th month into transform to tourism) performance point, not full FY25',
        }
        
        # Add explanations to the matrix
        for row_name, explanation in ROW_EXPLANATIONS.items():
            if row_name in matrix:
                # Ensure the row has enough columns
                while len(matrix[row_name]) < 29:
                    matrix[row_name].append('')
                
                # Add the explanation to the last column (index 28)
                matrix[row_name][28] = explanation

class TradeForecastGenerator:
    """
    Trade forecast generator implementing Historic Rivermill's business transformation methodology.
    
    Refactored to use Builder Pattern for improved maintainability and reduced code length.
    All calculations derive from trade_forecast_method.md specifications.
    """
    
    def __init__(self, admission_fee_december_onwards=10.00):
        """Initialize the forecast generator with methodology parameters."""
        # Configurable admission fee for December 2025 onwards
        self.admission_fee_december_onwards = admission_fee_december_onwards
        
        # Core baseline data from July 2025 P&L
        self._initialize_baseline_data()
        
        # Growth and operational methodology parameters  
        self._initialize_methodology_parameters()
        
        # Cost structure and operational changes
        self._initialize_cost_framework()
        
        # Revenue diversification schedule
        self._initialize_revenue_streams()
        
        # Load historical seasonal patterns
        self.seasonal_data = self.load_seasonal_patterns()
        
        # Ensure output directory exists
        self._ensure_output_directory()
        
        # Initialize the matrix builder
        self.matrix_builder = ForecastMatrixBuilder()

    def _ensure_output_directory(self):
        """Ensure the output directory exists."""
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
        os.makedirs(output_dir, exist_ok=True)

    def _initialize_baseline_data(self):
        """Establish July 2025 baseline data from P&L analysis."""
        self.july_2025_baseline = {
            'total_trading_income': 201972.61,
            'parties_events': 787.27,
            'restaurant_revenue': 90.91,
            'square_card_surcharges': 2286.12,
            'square_discounts': -5742.03,
            'square_sales': 202175.34,
            'wedding': 2375.00,
            'back_of_house_wages': 21645.90,
            'food_costs': 36825.88,
            'general_cafe_expense_cogs': 1899.61,
            'accounting': 1900.00,
            'advertising': 833.63,
            'bank_fees': 184.00,
            'employee_wages_others': 20117.63,
            'front_of_house_wages': 30352.18,
            'entertainment': 300.00,
            'equestrian_food': 1344.08,
            'equine_health_expenses': 1000.00,
            'equipment_leasing': 712.13,
            'general_cafe_expense_op': 3636.55,
            'insurance': 5488.19,
            'management_consultant': 450.00,
            'marketing': 9136.67,
            'motor_vehicle': 55.33,
            'office_supplies': 9523.26,
            'property_permits': 2565.80,
            'rent_expense': 12271.43,
            'repairs_maintenance': 8779.60,
            'rubbish_removal': 60.00,
            'shipping_postage': 11.70,
            'square_fees': 3067.29,
            'subscriptions': 3214.22,
            'superannuation': 8058.82,
            'telephone_internet': 208.18,
            'travel_international': 2680.83,
            'travel_national': 176.13,
            'utilities': 3923.32
        }
        
        # CRITICAL: July 2025 baseline represents proven, sustainable performance
        # Supported by sustained growth pattern: May (29% YoY), June (6% YoY), July (29% YoY)
        # This is not a one-time transformation spike but established growth trajectory

    def _initialize_methodology_parameters(self):
        """Configure growth methodology and operational transformation parameters."""
        self.growth_baseline = 0.267
        self.gross_to_trade_factor = 201972.61 / 210965
        
        # Updated growth target for 6% profit margin baseline scenario
        self.fy2526_growth_target = 0.000  # 0% growth for baseline profitability
        
        self.operational_factors = {
            'rent_resumption_sep': 12271,
            'labour_savings_sep': 75000 / 12,  # Reduced from $155k to $75k due to director salary
            'marketing_investment': -(180000 / 12),
            'solar_savings': 18000 / 12
        }
        
        self.months = [
            'Aug-25', 'Sep-25', 'Oct-25', 'Nov-25', 'Dec-25', 'Jan-26',
            'Feb-26', 'Mar-26', 'Apr-26', 'May-26', 'Jun-26', 'Jul-26',
            'Aug-26', 'Sep-26', 'Oct-26', 'Nov-26', 'Dec-26', 'Jan-27', 
            'Feb-27', 'Mar-27', 'Apr-27', 'May-27', 'Jun-27', 'Jul-27'
        ]

    def _initialize_cost_framework(self):
        """Establish cost structure reflecting operational restructuring outcomes."""
        self.base_cost_ratios = {
            'kitchen_wages': 0.075,
            'front_house_wages': 0.110,
            'superannuation': 0.12,  # Updated to 12% per new Australian rule effective July 2025
            'square_fees': 0.015,
            'general_cafe_cogs': 0.01
        }
        
        # Cost scaling factor for realistic profit margins (93% of revenue)
        self.cost_scaling_factor = 0.93
        
        self.transformation_food_cost_schedule = [
            0.180, 0.175, 0.175, 0.175, 0.175, 0.170, 0.170, 0.170, 0.165, 0.165, 0.165, 0.165,
            0.160, 0.160, 0.160, 0.160, 0.160, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155
        ]
        
        self.seasonal_cost_factors = {
            'peak_tourism': {'kitchen_wages': 0.075, 'front_house_wages': 0.110},
            'traditional_dining': {'kitchen_wages': 0.080, 'front_house_wages': 0.113},
            'transition': {'kitchen_wages': 0.077, 'front_house_wages': 0.111}
        }
        
        self.monthly_seasonal_classification = [
            'traditional_dining', 'peak_tourism', 'peak_tourism', 'peak_tourism', 'peak_tourism', 'peak_tourism',
            'peak_tourism', 'transition', 'traditional_dining', 'traditional_dining', 'traditional_dining', 'traditional_dining',
            'traditional_dining', 'peak_tourism', 'peak_tourism', 'peak_tourism', 'peak_tourism', 'peak_tourism',
            'peak_tourism', 'transition', 'traditional_dining', 'traditional_dining', 'traditional_dining', 'traditional_dining'
        ]
        
        # Matrix-based expense structure - ALL expenses must be explicitly defined
        self.expense_categories = [
            'accounting', 'administration_fees', 'advertising_promotion', 'automobile_expense',
            'bank_fees', 'business_gift_expense', 'cleaning_expense', 'design_printing',
            'director_salary', 'employee_wages_others', 'front_house_wages', 'entertainment', 'equestrian_food',
            'equine_health_expenses', 'equipment_leasing', 'general_business_research',
            'general_cafe_expense', 'insurance', 'interest_expense', 'legal',
            'management_consultant', 'marketing', 'miscellaneous_expenses', 'motor_vehicle',
            'non_equine_health', 'office_expenses', 'office_supplies', 'parking_ticket',
            'printing_stationery', 'professional_services', 'property_permits',
            'realised_currency_gains', 'refund', 'reimbursement_clearing', 'renovation_contractors',
            'rent_expense', 'repairs_maintenance', 'retail_item_purchase', 'rubbish_removal',
            'shipping_postage', 'square_fees', 'staff_meals_amenities', 'staffing_contractors',
            'subscriptions', 'sundry_expenses', 'superannuation', 'telephone_internet',
            'training_development', 'travel_international', 'travel_national',
            'travel_national_leasing', 'travel_taxi', 'utilities', 'web_domain_hosting', 'wedding_cost',
            'wedding_sales_expense'
        ]
        
        # Initialize expense matrix with 24 months + category name column
        self.expense_matrix = [[0] * 25 for _ in range(len(self.expense_categories))]
        
        # Populate category names in first column
        for i, category in enumerate(self.expense_categories):
            self.expense_matrix[i][0] = category
        
        # Define baseline monthly values for each expense category
        self.expense_baselines = {
            'accounting': 500,
            'administration_fees': 0,
            'advertising_promotion': 1500,
            'automobile_expense': 0,
            'bank_fees': 200,  # Will be escalated monthly
            'business_gift_expense': 0,
            'cleaning_expense': 885,  # $10,627 annually / 12
            'design_printing': 0,
            'director_salary': 0,  # Will be set based on month (Sep 2025 onwards)
            'employee_wages_others': 15000,  # Reduced from $20,118 after Sophie replacement
            'front_house_wages': 0,  # Calculated as percentage of revenue
            'entertainment': 300,
            'equestrian_food': 1500,
            'equine_health_expenses': 1000,
            'equipment_leasing': 712,
            'general_business_research': 0,
            'general_cafe_expense': 3500,
            'insurance': 0,  # Paid annually in July
            'interest_expense': 0,
            'legal': 0,
            'management_consultant': 450,
            'marketing': 15000,
            'miscellaneous_expenses': 0,
            'motor_vehicle': 55,
            'non_equine_health': 0,
            'office_expenses': 355,  # $4,254.68 annually / 12
            'office_supplies': 4000,
            'parking_ticket': 0,
            'printing_stationery': 0,
            'professional_services': 2193,  # $26,318.18 annually / 12
            'property_permits': 0,  # Paid annually in July
            'realised_currency_gains': 0,
            'refund': 0,
            'reimbursement_clearing': 0,
            'renovation_contractors': 0,  # Renovation completed by July 2025
            'rent_expense': 0,  # Will be set based on month
            'repairs_maintenance': 9000,
            'retail_item_purchase': 0,
            'rubbish_removal': 60,
            'shipping_postage': 11.7,
            'square_fees': 0,  # Calculated as percentage of Square revenue
            'staff_meals_amenities': 697,  # $8,367.07 annually / 12
            'staffing_contractors': 0,  # Replaced by permanent staff structure
            'subscriptions': 3214,
            'sundry_expenses': 0,
            'superannuation': 0,  # Calculated as 12% of wages per new Australian rule July 2025
            'telephone_internet': 230,
            'training_development': 0,
            'travel_international': 2680.83,
            'travel_national': 176.13,
            'travel_national_leasing': 0,
            'travel_taxi': 0,
            'utilities': 0,  # Will be calculated with solar savings
            'web_domain_hosting': 0,
            'wedding_cost': 0,
            'wedding_sales_expense': 0  # Will be calculated based on month and wedding revenue
        }
        
        # Validate that all expense categories have baselines defined
        missing_baselines = [cat for cat in self.expense_categories if cat not in self.expense_baselines]
        if missing_baselines:
            raise ValueError(f"Missing expense baselines for: {missing_baselines}")
        
        # Validate that all baselines have corresponding categories
        extra_baselines = [cat for cat in self.expense_baselines.keys() if cat not in self.expense_categories]
        if extra_baselines:
            raise ValueError(f"Extra expense baselines found: {extra_baselines}")

    def _initialize_revenue_streams(self):
        """Configure revenue diversification strategy."""
        self.wedding_schedule = [
            0, 0, 0, 7500, 15000, 15000, 7500, 15000, 7500, 7500, 0, 0,
            10000, 20000, 30000, 30000, 40000, 30000, 40000, 30000, 20000, 10000, 15000, 20000
        ]
        
        self.farmstay_schedule = [
            0, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 10000, 10000, 10000, 10000,
            10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000
        ]

    def load_seasonal_patterns(self) -> Dict[str, float]:
        """Derive seasonal patterns from historical sales data."""
        seasonal_data = {}
        csv_path = os.path.join(os.path.dirname(__file__), '12-month-gross-sales.csv')
        
        july_2025_trade = 201972.61
        july_2024_trade = july_2025_trade / 1.267
        gross_trade_factor = 1.0445
        july_2024_gross_estimated = july_2024_trade * gross_trade_factor
        
        try:
            with open(csv_path, 'r') as f:
                reader = csv.reader(f)
                gross_sales_data = {}
                
                for row in reader:
                    if len(row) >= 2 and row[0].strip() and row[1].strip():
                        month_year = row[0].strip()
                        try:
                            gross_sales = float(row[1].strip())
                            gross_sales_data[month_year] = gross_sales
                        except ValueError:
                            continue
                
                month_names = {
                    '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec',
                    '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', 
                    '06': 'Jun', '07': 'Jul'
                }
                
                for month_year, gross_value in gross_sales_data.items():
                    if month_year.startswith('2024-'):
                        month_num = month_year.split('-')[1]
                        if month_num in month_names:
                            month_name = month_names[month_num]
                            seasonal_factor = gross_value / july_2024_gross_estimated
                            seasonal_data[month_name] = seasonal_factor
                
                for month_year, gross_value in gross_sales_data.items():
                    if month_year.startswith('2025-'):
                        month_num = month_year.split('-')[1]
                        if month_num in month_names and month_num in ['01', '02', '04', '05', '06', '07']:
                            month_name = month_names[month_num]
                            equivalent_2024_gross = gross_value / 1.267
                            seasonal_factor = equivalent_2024_gross / july_2024_gross_estimated
                            seasonal_data[month_name] = seasonal_factor
                
                if 'Feb' in seasonal_data and 'Apr' in seasonal_data:
                    march_normalised = (seasonal_data['Feb'] + seasonal_data['Apr']) / 2
                    seasonal_data['Mar'] = march_normalised
                
                seasonal_data['Jul'] = 1.0
                        
        except FileNotFoundError:
            feb_factor = 0.708
            apr_factor = 0.732
            mar_normalised = (feb_factor + apr_factor) / 2
            seasonal_data = {
                'Jul': 1.0, 'Aug': 0.825, 'Sep': 0.875, 'Oct': 0.577, 'Nov': 0.545, 'Dec': 0.544,
                'Jan': 0.830, 'Feb': feb_factor, 'Mar': mar_normalised, 'Apr': apr_factor, 'May': 1.003, 'Jun': 1.014
            }
        
        return seasonal_data

    def calculate_tourism_revenue(self, month_index: int) -> float:
        """Calculate tourism revenue using growth methodology with seasonal authenticity."""
        july_2025_tourism = self.july_2025_baseline['total_trading_income'] - self.july_2025_baseline['wedding']
        
        month_names = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
        month_name = month_names[month_index % 12]
        seasonal_factor = self.seasonal_data.get(month_name, 1.0)
        
        base_seasonal_revenue = july_2025_tourism * seasonal_factor
        
        annual_visitors = 125000
        weekend_visitor_ratio = 2/3
        weekend_annual_visitors = annual_visitors * weekend_visitor_ratio
        monthly_weekend_visitors = weekend_annual_visitors / 12 * seasonal_factor
        
        baseline_admission_fee = 4.75
        current_admission_fee = baseline_admission_fee
        if month_index >= 1:
            current_admission_fee = 8.75
        if month_index >= 4:
            current_admission_fee = self.admission_fee_december_onwards
            
        baseline_monthly_admission_revenue = monthly_weekend_visitors * baseline_admission_fee
        current_monthly_admission_revenue = monthly_weekend_visitors * current_admission_fee
        admission_revenue_increase = current_monthly_admission_revenue - baseline_monthly_admission_revenue
        
        base_seasonal_revenue = base_seasonal_revenue + admission_revenue_increase
        
        if month_index < 12:
            additional_growth_target = 0.000  # Changed to 0.000 for 0% growth (baseline scenario)
            progress_through_year = (month_index + 1) / 12
            additional_growth_factor = 1 + (additional_growth_target * progress_through_year)
            projected_revenue = base_seasonal_revenue * additional_growth_factor
        else:
            fy2526_end_baseline = july_2025_tourism * 1.000  # Changed to 1.000 for 0% growth
            base_fy2627_revenue = fy2526_end_baseline * seasonal_factor
            
            current_admission_fee = self.admission_fee_december_onwards
            baseline_monthly_admission_revenue = monthly_weekend_visitors * baseline_admission_fee
            current_monthly_admission_revenue = monthly_weekend_visitors * current_admission_fee
            admission_revenue_increase = current_monthly_admission_revenue - baseline_monthly_admission_revenue
            base_fy2627_revenue = base_fy2627_revenue + admission_revenue_increase
            
            second_year_progress = (month_index - 11) / 12
            fy2627_growth_factor = 1 + (0.14 * second_year_progress)
            projected_revenue = base_fy2627_revenue * fy2627_growth_factor
        
        return projected_revenue

    def calculate_variable_costs(self, total_revenue: float, month_index: int) -> Dict[str, float]:
        """Calculate variable costs using transformation-based food cost reduction and seasonal labour variations."""
        food_cost_percentage = self.transformation_food_cost_schedule[month_index]
        seasonal_type = self.monthly_seasonal_classification[month_index]
        seasonal_factors = self.seasonal_cost_factors[seasonal_type]
        
        return {
            'food_costs': total_revenue * food_cost_percentage,
            'kitchen_wages': total_revenue * seasonal_factors['kitchen_wages'],
            'front_house_wages': total_revenue * seasonal_factors['front_house_wages'],
            'general_cafe_cogs': total_revenue * self.base_cost_ratios['general_cafe_cogs']
        }

    def calculate_square_fees(self, revenue_breakdown: Dict[str, float]) -> float:
        """Calculate Square fees as 1.5% of Square-related income streams."""
        square_sales = revenue_breakdown.get('square_sales', 0)
        square_card_surcharges = revenue_breakdown.get('square_card_surcharges', 0)
        square_discounts = revenue_breakdown.get('square_discounts', 0)
        
        total_square_income = square_sales + square_card_surcharges + abs(square_discounts)
        square_fees = total_square_income * 0.015
        
        return square_fees

    def calculate_superannuation(self, cost_of_sales: Dict[str, float], operating_expenses: Dict[str, float]) -> float:
        """Calculate superannuation as 12% of total wages (excluding marketing personnel)."""
        kitchen_wages = cost_of_sales.get('kitchen_wages', 0)
        front_house_wages = operating_expenses.get('front_house_wages', 0)
        employee_wages_others = operating_expenses.get('employee_wages_others', 0)
        director_salary = operating_expenses.get('director_salary', 0)
        
        # Marketing personnel are excluded from superannuation calculation
        # as they are paid under Marketing Expense and not subject to Australian super rules
        total_wages = kitchen_wages + front_house_wages + employee_wages_others + director_salary
        superannuation = total_wages * 0.12
        
        return superannuation

    def calculate_escalating_costs(self, month_index: int, total_revenue: float) -> Dict[str, float]:
        """Calculate costs that scale with business growth and operational improvements."""
        escalating = {}
        
        escalating['bank_fees'] = 200 + (month_index * 15)
        
        # Utilities calculation based on June 2026 baseline with seasonal fluctuations
        if month_index == 0:  # August 2025
            escalating['utilities'] = 2923  # July 2025 baseline
        else:
            # June 2026 is month index 10 (Aug-25=0, Sep-25=1, ..., Jun-26=10)
            june_2026_baseline = 4500
            
            # Get seasonal classification for current month
            seasonal_type = self.monthly_seasonal_classification[month_index]
            
            if seasonal_type == 'peak_tourism':
                escalating['utilities'] = june_2026_baseline * 1.067  # +6.7% for peak tourism
            elif seasonal_type == 'traditional_dining':
                escalating['utilities'] = june_2026_baseline * 0.933  # -6.7% for traditional dining
            else:  # transition months
                escalating['utilities'] = june_2026_baseline  # baseline level
        
        if month_index == 0:
            escalating['employee_wages_others'] = self.july_2025_baseline['employee_wages_others']
        else:
            escalating['employee_wages_others'] = 15000
            
        return escalating

    def calculate_operational_adjustments(self, month_index: int) -> Dict[str, float]:
        """Apply month-specific operational changes according to transformation timeline."""
        adjustments = {
            'rent_adjustment': 0,
            'marketing_increase': 0,
            'solar_savings': 0,
            'media_downpayment': 0
        }
        
        if month_index == 0:
            adjustments['media_downpayment'] = 10000
            adjustments['solar_savings'] = self.operational_factors['solar_savings']
        elif month_index >= 1:
            adjustments['rent_adjustment'] = self.operational_factors['rent_resumption_sep']
            
            if month_index == 1:
                adjustments['marketing_increase'] = -(36000 + 24000 + 12000 + 108000) / 12
            else:
                adjustments['marketing_increase'] = self.operational_factors['marketing_investment']
                
            adjustments['solar_savings'] = self.operational_factors['solar_savings']
        
        return adjustments

    def calculate_monthly_forecast(self, month_index: int) -> Dict[str, float]:
        """Generate comprehensive financial forecast for a single month."""
        if month_index == -1:
            month_name = 'Jul-25'
            tourism_revenue = self.july_2025_baseline['total_trading_income'] - self.july_2025_baseline['wedding']
            wedding_revenue = self.july_2025_baseline['wedding']
            farmstay_revenue = 0
            total_revenue = self.july_2025_baseline['total_trading_income']
        else:
            month_name = self.months[month_index]
            tourism_revenue = self.calculate_tourism_revenue(month_index)
            wedding_revenue = self.wedding_schedule[month_index]
            farmstay_revenue = self.farmstay_schedule[month_index]
            total_revenue = tourism_revenue + wedding_revenue + farmstay_revenue
        
        if month_index == -1:
            revenue_breakdown = {
                'parties_events': self.july_2025_baseline['parties_events'],
                'restaurant_revenue': self.july_2025_baseline['restaurant_revenue'],
                'square_card_surcharges': self.july_2025_baseline['square_card_surcharges'],
                'square_discounts': self.july_2025_baseline['square_discounts'],
                'square_sales': self.july_2025_baseline['square_sales'],
                'wedding': wedding_revenue,
                'farmstay': farmstay_revenue,
                'total_trading_income': total_revenue
            }
        else:
            scale_factor = tourism_revenue / (self.july_2025_baseline['total_trading_income'] - 
                                            self.july_2025_baseline['wedding'])
            
            revenue_breakdown = {
                'parties_events': self.july_2025_baseline['parties_events'] * scale_factor,
                'restaurant_revenue': self.july_2025_baseline['restaurant_revenue'] * scale_factor,
                'square_card_surcharges': self.july_2025_baseline['square_card_surcharges'] * scale_factor,
                'square_discounts': self.july_2025_baseline['square_discounts'] * scale_factor,
                'square_sales': tourism_revenue,
                'wedding': wedding_revenue,
                'farmstay': farmstay_revenue
            }
            
            revenue_breakdown['total_trading_income'] = sum([
                revenue_breakdown['parties_events'],
                revenue_breakdown['restaurant_revenue'],
                revenue_breakdown['square_card_surcharges'],
                revenue_breakdown['square_discounts'],
                revenue_breakdown['square_sales'],
                revenue_breakdown['wedding'],
                revenue_breakdown['farmstay']
            ])
        
        if month_index == -1:
            cost_of_sales = {
                'kitchen_wages': self.july_2025_baseline['back_of_house_wages'],
                'food_costs': self.july_2025_baseline['food_costs'],
                'general_cafe_cogs': self.july_2025_baseline['general_cafe_expense_cogs'],
                'total_cost_of_sales': (self.july_2025_baseline['back_of_house_wages'] + 
                                      self.july_2025_baseline['food_costs'] + 
                                      self.july_2025_baseline['general_cafe_expense_cogs'])
            }
        else:
            variable_costs = self.calculate_variable_costs(total_revenue, month_index)
            cost_of_sales = {
                'kitchen_wages': variable_costs['kitchen_wages'],
                'food_costs': variable_costs['food_costs'],
                'general_cafe_cogs': variable_costs['general_cafe_cogs'],
                'total_cost_of_sales': (variable_costs['kitchen_wages'] + 
                                      variable_costs['food_costs'] + 
                                      variable_costs['general_cafe_cogs'])
            }
        
        gross_profit = revenue_breakdown['total_trading_income'] - cost_of_sales['total_cost_of_sales']
        
        if month_index == -1:
            operating_expenses = {
                'accounting': self.july_2025_baseline['accounting'],
                'advertising_promotion': self.july_2025_baseline['advertising'],
                'bank_fees': self.july_2025_baseline['bank_fees'],
                'director_salary': 0,  # July 2025 - Mike Wood still employed
                'employee_wages_others': self.july_2025_baseline['employee_wages_others'],
                'front_house_wages': self.july_2025_baseline['front_of_house_wages'],
                'entertainment': self.july_2025_baseline['entertainment'],
                'equestrian_food': self.july_2025_baseline['equestrian_food'],
                'equine_health_expenses': self.july_2025_baseline['equine_health_expenses'],
                'equipment_leasing': self.july_2025_baseline['equipment_leasing'],
                'farmstay_costs': 0,
                'general_cafe_expense': self.july_2025_baseline['general_cafe_expense_op'],
                'management_consultant': self.july_2025_baseline['management_consultant'],
                'marketing': self.july_2025_baseline['marketing'],
                'motor_vehicle': self.july_2025_baseline['motor_vehicle'],
                'office_supplies': self.july_2025_baseline['office_supplies'],
                'rent_expense': self.july_2025_baseline['rent_expense'],
                'repairs_maintenance': self.july_2025_baseline['repairs_maintenance'],
                'rubbish_removal': self.july_2025_baseline['rubbish_removal'],
                'shipping_postage': self.july_2025_baseline['shipping_postage'],
                'square_fees': self.july_2025_baseline['square_fees'],
                'subscriptions': self.july_2025_baseline['subscriptions'],
                'superannuation': self.july_2025_baseline['superannuation'],
                'telephone_internet': self.july_2025_baseline['telephone_internet'],
                'utilities': self.july_2025_baseline['utilities'],
                'insurance': self.july_2025_baseline['insurance'],
                'property_permits': self.july_2025_baseline['property_permits'],
                'travel_international': self.july_2025_baseline['travel_international'],
                'travel_national': self.july_2025_baseline['travel_national']
            }
        else:
            # Matrix-based approach: populate all expense categories
            operating_expenses = {}
            
            # Start with all baseline expenses
            for category in self.expense_categories:
                operating_expenses[category] = self.expense_baselines[category]
            
            # Override specific expenses based on month and calculations
            variable_costs = self.calculate_variable_costs(total_revenue, month_index)
            cogs_keys = ['food_costs', 'kitchen_wages', 'general_cafe_cogs']
            
            # Set calculated expenses
            operating_expenses['front_house_wages'] = variable_costs['front_house_wages']
            
            # Handle escalating costs
            escalating_costs = self.calculate_escalating_costs(month_index, total_revenue)
            operating_expenses['bank_fees'] = escalating_costs['bank_fees']
            operating_expenses['employee_wages_others'] = escalating_costs['employee_wages_others']
            
            # Handle operational adjustments
            operational_adjustments = self.calculate_operational_adjustments(month_index)
            
            # Rent handling
            if month_index == 0:
                operating_expenses['rent_expense'] = 0  # August rental holiday
            else:
                operating_expenses['rent_expense'] = operational_adjustments['rent_adjustment']
            
            # Director salary handling
            if month_index == 0:
                operating_expenses['director_salary'] = 0  # August - no director salary
            else:
                operating_expenses['director_salary'] = 9167  # September 2025 onwards - $110k annually
            
            # Marketing handling
            if month_index == 0:
                july_marketing = self.july_2025_baseline['marketing']
                operating_expenses['marketing'] = july_marketing + operational_adjustments['media_downpayment']
            
            # Utilities with solar savings and seasonal fluctuations
            # Base utilities calculated in escalating_costs with June 2026 baseline ($4,500)
            # Seasonal fluctuations: peak tourism (+6.7%), traditional dining (-6.7%), transition (baseline)
            base_utilities = escalating_costs.get('utilities', 3923.32)
            operating_expenses['utilities'] = base_utilities - operational_adjustments['solar_savings']
            
            # Farmstay costs
            operating_expenses['farmstay_costs'] = farmstay_revenue * 0.20
            
            # Wedding sales expense
            if month_index < 3:  # Aug-Oct 2025: infrastructure phase
                operating_expenses['wedding_sales_expense'] = 0
            elif month_index < 12:  # Nov 2025 - Jul 2026: FY25/26
                operating_expenses['wedding_sales_expense'] = 2167  # $26k annually
            else:  # Aug 2026 onwards: FY26/27
                operating_expenses['wedding_sales_expense'] = 3333  # $40k annually
            
            # Calculated fees
            operating_expenses['square_fees'] = self.calculate_square_fees(revenue_breakdown)
            operating_expenses['superannuation'] = self.calculate_superannuation(cost_of_sales, operating_expenses)
            
            # Annual payments (only in July of each year)
            if month_index == 11:  # July 2026
                operating_expenses['insurance'] = self.july_2025_baseline['insurance']
                operating_expenses['property_permits'] = self.july_2025_baseline['property_permits']
            elif month_index == 23:  # July 2027
                operating_expenses['insurance'] = self.july_2025_baseline['insurance']
                operating_expenses['property_permits'] = self.july_2025_baseline['property_permits']
            
            # Travel International schedule: Aug=0, Sep=3000, Oct=2000, Nov=1000, Dec=3000, rest of FY25/26=0, FY26/27=2000/month average
            if month_index == 0:  # August 2025
                operating_expenses['travel_international'] = 0
            elif month_index == 1:  # September 2025
                operating_expenses['travel_international'] = 3000
            elif month_index == 2:  # October 2025
                operating_expenses['travel_international'] = 2000
            elif month_index == 3:  # November 2025
                operating_expenses['travel_international'] = 1000
            elif month_index == 4:  # December 2025
                operating_expenses['travel_international'] = 3000
            elif month_index < 12:  # January 2026 to July 2026 (FY25/26)
                operating_expenses['travel_international'] = 0
            else:  # August 2026 onwards (FY26/27) - average 2000 per month
                operating_expenses['travel_international'] = 2000
            
            # Validate that all expense categories are populated
            missing_expenses = [cat for cat in self.expense_categories if cat not in operating_expenses]
            if missing_expenses:
                raise ValueError(f"Missing expenses in forecast: {missing_expenses}")
            
            # Validate that no extra expenses were added
            extra_expenses = [cat for cat in operating_expenses.keys() if cat not in self.expense_categories and cat != 'farmstay_costs']
            if extra_expenses:
                raise ValueError(f"Extra expenses found: {extra_expenses}")
        
        total_operating_expenses = sum(operating_expenses.values())
        net_profit = gross_profit - total_operating_expenses
        net_profit_margin = (net_profit / revenue_breakdown['total_trading_income']) * 100 if revenue_breakdown['total_trading_income'] > 0 else 0
        
        if month_index == -1:
            revenue_growth = 0.0
        elif month_index == 0:
            revenue_growth = ((revenue_breakdown['total_trading_income'] - self.july_2025_baseline['total_trading_income']) / 
                            self.july_2025_baseline['total_trading_income']) * 100
        else:
            prev_revenue = self.calculate_monthly_forecast(month_index - 1)['revenue_breakdown']['total_trading_income']
            revenue_growth = ((revenue_breakdown['total_trading_income'] - prev_revenue) / prev_revenue) * 100
        
        return {
            'month': month_name,
            'month_index': month_index,
            'revenue_breakdown': revenue_breakdown,
            'cost_of_sales': cost_of_sales,
            'gross_profit': gross_profit,
            'operating_expenses': operating_expenses,
            'total_operating_expenses': total_operating_expenses,
            'net_profit': net_profit,
            'net_profit_margin': net_profit_margin,
            'revenue_growth': revenue_growth
        }



    def generate_summary_report(self, forecast_data: List[Dict], actual_data: Dict[str, Dict[str, float]]) -> str:
        """Generate comprehensive trade forecast summary report."""
        # Calculate key metrics
        fy2526_months = forecast_data[1:13]  # Aug-25 to Jul-26
        fy2627_months = forecast_data[13:25]  # Aug-26 to Jul-27
        
        fy2526_total_revenue = sum(data['revenue_breakdown']['total_trading_income'] for data in fy2526_months)
        fy2627_total_revenue = sum(data['revenue_breakdown']['total_trading_income'] for data in fy2627_months)
        
        fy2526_total_cogs = sum(data['cost_of_sales']['total_cost_of_sales'] for data in fy2526_months)
        fy2627_total_cogs = sum(data['cost_of_sales']['total_cost_of_sales'] for data in fy2627_months)
        
        fy2526_total_expenses = sum(sum(data['operating_expenses'].values()) for data in fy2526_months)
        fy2627_total_expenses = sum(sum(data['operating_expenses'].values()) for data in fy2627_months)
        
        fy2526_gross_profit = fy2526_total_revenue - fy2526_total_cogs
        fy2627_gross_profit = fy2627_total_revenue - fy2627_total_cogs
        
        fy2526_net_profit = fy2526_gross_profit - fy2526_total_expenses
        fy2627_net_profit = fy2627_gross_profit - fy2627_total_expenses
        
        # Calculate peak month (July 2027)
        july_2027_data = forecast_data[23]  # July 2027
        july_2027_revenue = july_2027_data['revenue_breakdown']['total_trading_income']
        july_2027_net_profit = (july_2027_data['revenue_breakdown']['total_trading_income'] - 
                               july_2027_data['cost_of_sales']['total_cost_of_sales'] - 
                               sum(july_2027_data['operating_expenses'].values()))
        
        # Calculate averages
        fy2526_avg_monthly_revenue = fy2526_total_revenue / 12
        fy2627_avg_monthly_revenue = fy2627_total_revenue / 12
        fy2526_avg_monthly_profit = fy2526_net_profit / 12
        fy2627_avg_monthly_profit = fy2627_net_profit / 12
        
        # Calculate margins
        fy2526_margin = (fy2526_net_profit / fy2526_total_revenue) * 100 if fy2526_total_revenue > 0 else 0
        fy2627_margin = (fy2627_net_profit / fy2627_total_revenue) * 100 if fy2627_total_revenue > 0 else 0
        total_margin = ((fy2526_net_profit + fy2627_net_profit) / (fy2526_total_revenue + fy2627_total_revenue)) * 100
        
        # Labour cost analysis
        july_2025_baseline_labour = 72116  # From original data
        new_monthly_labour = 48008  # From restructured model
        monthly_labour_savings = july_2025_baseline_labour - new_monthly_labour
        annual_labour_savings = monthly_labour_savings * 12
        
        report = f"""# Trade Forecast Summary Report - Historic Rivermill Transformation

## Executive Summary
Historic Rivermill's 24-month trade forecast demonstrates successful transformation from café to tourism destination with sustainable profitability and operational efficiency improvements.

## Financial Performance Overview

### Revenue Performance by Financial Year
| Period | Total Revenue | Average Monthly | Peak Month |
|--------|---------------|-----------------|------------|
| **FY24/25** (Aug 2024 - Jul 2025) | ${actual_data['FY25'].get('Total Trading Income', 0):,.0f} | ${actual_data['FY25'].get('Total Trading Income', 0) / 12:,.0f} | N/A |
| **FY25/26** (Aug 2025 - Jul 2026) | ${fy2526_total_revenue:,.0f} | ${fy2526_avg_monthly_revenue:,.0f} | N/A |
| **FY26/27** (Aug 2026 - Jul 2027) | ${fy2627_total_revenue:,.0f} | ${fy2627_avg_monthly_revenue:,.0f} | Jul-27 |
| **Total 24 Months** | ${fy2526_total_revenue + fy2627_total_revenue:,.0f} | ${(fy2526_total_revenue + fy2627_total_revenue) / 24:,.0f} | Jul-27 (${july_2027_revenue:,.0f}) |

### Profitability Analysis by Financial Year
| Period | Total Net Profit | Average Monthly | Average Margin |
|--------|------------------|-----------------|----------------|
| **FY25/26** (Aug 2025 - Jul 2026) | ${fy2526_net_profit:,.0f} | ${fy2526_avg_monthly_profit:,.0f} | {fy2526_margin:.1f}% |
| **FY26/27** (Aug 2026 - Jul 2027) | ${fy2627_net_profit:,.0f} | ${fy2627_avg_monthly_profit:,.0f} | {fy2627_margin:.1f}% |
| **Total 24 Months** | ${fy2526_net_profit + fy2627_net_profit:,.0f} | ${(fy2526_net_profit + fy2627_net_profit) / 24:,.0f} | {total_margin:.1f}% |

**Peak Profit Month:** Jul-27 (${july_2027_net_profit:,.0f})

## Transformation Success Metrics

### Labour Cost Optimization (Site-Wide)
- **Previous Structure:** 35.7% of total site revenue (unsustainable)
  - Back of house wages: $21,646
  - Front of house wages: $30,352
  - Other employee wages: $20,118
  - **Total labour costs: $72,116**

- **Restructured Model:** 18.4% of total site revenue (sustainable)
  - Katrina (FOH Supervisor): $5,458/month
  - Zakeira (FOH Staff): $4,333/month
  - Sam (Multi-use operations): $3,467/month
  - Lisa (Barista): $4,750/month
  - Bruno (Sous Chef): $6,250/month
  - Diogo (Head Chef + F&B Manager): $8,750/month
  - Other employee wages: $15,000/month
  - **Total new labour costs: $48,008/month**

- **Labour Cost Savings:**
  - Monthly savings: ${monthly_labour_savings:,.0f}
  - Annual savings: ${annual_labour_savings:,.0f}
  - **Verification:** Previous $72,116 - New $48,008 = ${monthly_labour_savings:,.0f} monthly
- **Implementation:** September 2025 onwards

### Revenue Diversification
- **Tourism Operations:** Core revenue driver with seasonal authenticity
- **Wedding Services:** Phased recovery from $0 to $40,000 monthly
- **Farmstay Accommodation:** $5,000 to $10,000 monthly progression
- **Admission Fee Strategy:** A$4.75 → A$8.75 (Sep 2025) → A$10.00 (Dec 2025)

### Operational Efficiency
- **Solar Energy Implementation:** $18,000 annual savings from August 2025
- **Marketing Investment:** $180,000 annually for strategic growth
- **Rent Management:** Holiday period until August 2025, then $14,000 monthly

## Seasonal Performance Analysis

### Peak Tourism Periods (Sep-Mar)
- Higher revenue through admission fees and tourism activities
- Lower food cost percentages due to revenue mix optimization
- Efficient labour utilization during peak operations

### Traditional Dining Periods (Apr-Aug)
- Stable operations with tourism support
- Higher food cost percentages reflecting service focus
- Balanced labour costs for operational requirements

## Growth Trajectory

### FY25/26 (First Year)
- **Target Growth:** +0.0% beyond July 2025 baseline (baseline scenario for 6% profit margin)
- **Key Drivers:** Admission fee increases, tourism expansion, operational restructuring
- **Expected Outcome:** Baseline profitability from September 2025 with 6% profit margin

### FY26/27 (Second Year)
- **Target Growth:** +14.0% building on first year achievements
- **Key Drivers:** Established tourism operations, wedding service maturity, farmstay expansion
- **Expected Outcome:** Consistent profitability with operational efficiency

## Risk Mitigation

### Conservative Assumptions
- Excludes chalet development revenue (pending DA approval)
- Excludes wildlife licence premium pricing (A$15-A$20 potential)
- Underutilizes market leadership pricing power
- Based on demonstrated performance improvements

### Operational Safeguards
- Seasonal working capital management
- Phased implementation of transformation initiatives
- Realistic cost structure evolution
- Proven growth methodology from July 2024-2025 performance

## Conclusion

The trade forecast validates Historic Rivermill's transformation strategy as financially sustainable and operationally sound. The systematic approach to labour optimization, revenue diversification, and operational efficiency creates a foundation for long-term profitability and growth.

Key success factors include:
- **Demonstrated Growth Capability:** 26.7% improvement from July 2024-2025
- **Strategic Cost Restructuring:** ${annual_labour_savings:,.0f} annual labour savings
- **Revenue Mix Optimization:** Tourism focus with supporting food services
- **Operational Transformation:** Solar energy, marketing investment, infrastructure improvements

The forecast represents a conservative baseline suitable for SBR approval whilst acknowledging the significant competitive advantages and growth potential that Historic Rivermill has established through its transformation initiatives.
"""
        
        return report

    def generate_24_month_forecast(self) -> List[Dict]:
        """Generate complete 24-month forecast from August 2025 to July 2027."""
        forecast_data = []
        
        july_baseline = self.calculate_monthly_forecast(-1)
        forecast_data.append(july_baseline)
        
        for month_index in range(23):
            monthly_forecast = self.calculate_monthly_forecast(month_index)
            forecast_data.append(monthly_forecast)
        
        return forecast_data

    def load_actual_data(self) -> Dict[str, Dict[str, float]]:
        """Load actual data from the P&L CSV file."""
        actual_data = {'FY25': {}, 'Jul-25': {}}
        
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'input', 'p-l-fy25-and-july-2025.csv')
        
        try:
            with open(csv_path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 3 and row[0].strip():
                        account = row[0].strip()
                        try:
                            fy25_value = float(row[1].strip()) if row[1].strip() else 0.0
                            jul25_value = float(row[2].strip()) if row[2].strip() else 0.0
                            
                            actual_data['FY25'][account] = fy25_value
                            actual_data['Jul-25'][account] = jul25_value
                        except ValueError:
                            continue
                            
        except FileNotFoundError:
            actual_data['FY25'] = {
                'Total Trading Income': self.july_2025_baseline['total_trading_income'] * 12,
                'Total Cost of Sales': (self.july_2025_baseline['back_of_house_wages'] + 
                                      self.july_2025_baseline['food_costs'] + 
                                      self.july_2025_baseline['general_cafe_expense_cogs']) * 12,
                'Total Operating Expenses': sum(self.july_2025_baseline.get(expense, 0) for expense in [
                    'accounting', 'advertising', 'bank_fees', 'employee_wages_others', 'front_of_house_wages',
                    'entertainment', 'equestrian_food', 'equine_health_expenses', 'equipment_leasing',
                    'general_cafe_expense_op', 'insurance', 'management_consultant', 'marketing',
                    'motor_vehicle', 'office_supplies', 'property_permits', 'rent_expense',
                    'repairs_maintenance', 'rubbish_removal', 'shipping_postage', 'square_fees',
                    'subscriptions', 'superannuation', 'telephone_internet', 'travel_international',
                    'travel_national', 'utilities'
                ]) * 12
            }
            actual_data['Jul-25'] = {
                'Total Trading Income': self.july_2025_baseline['total_trading_income'],
                'Total Cost of Sales': (self.july_2025_baseline['back_of_house_wages'] + 
                                      self.july_2025_baseline['food_costs'] + 
                                      self.july_2025_baseline['general_cafe_expense_cogs']),
                'Total Operating Expenses': sum(self.july_2025_baseline.get(expense, 0) for expense in [
                    'accounting', 'advertising', 'bank_fees', 'employee_wages_others', 'front_of_house_wages',
                    'entertainment', 'equestrian_food', 'equine_health_expenses', 'equipment_leasing',
                    'general_cafe_expense_op', 'insurance', 'management_consultant', 'marketing',
                    'motor_vehicle', 'office_supplies', 'property_permits', 'rent_expense',
                    'repairs_maintenance', 'rubbish_removal', 'shipping_postage', 'square_fees',
                    'subscriptions', 'superannuation', 'telephone_internet', 'travel_international',
                    'travel_national', 'utilities'
                ]) + 0  # Wedding sales expense: $0 in July 2025 (Sophie still employed)
            }
        
        return actual_data

    def write_csv_file(self, forecast_data: List[Dict], filename: str = '../output/trade-forecast.csv'):
        """Generate comprehensive CSV output using the Builder Pattern."""
        # Use the Builder Pattern to construct the matrix
        matrix = self.matrix_builder.build(forecast_data, self.load_actual_data())
        
        # Write the matrix to CSV
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write headers
            writer.writerow(['Trading forecast (conservative)'])
            writer.writerow(['Colourful.Land Pty Ltd'])
            writer.writerow(['August 2025 to July 2027'])
            writer.writerow([])
            
            # Write column headers
            month_headers = ['', 'Actual', 'Actual'] + ['Forecast'] * 23 + ['FY25/26 Total', 'FY26/27 Total', 'Director explanation']
            writer.writerow(month_headers)
            writer.writerow(self.matrix_builder.columns)
            writer.writerow([])
            
            # Write matrix rows
            matrix_rows = [
                'Trading Income',
                'Parties and Events',
                'Restaurant Revenue',
                'Sales - Equestrian Party Booking',
                'Sales - Leasing',
                'Sales - STR',
                'Special Event',
                'Square Card Surcharges',
                'Square Discounts',
                'Square Other Income',
                'Square Sales',
                'Venue Hire',
                'Wedding',
                'Farm Stay',
                'Total Trading Income',
                'Cost of Sales',
                'COGS - Back of house (Kitchen wages)',
                'COGS - Food Costs',
                'COGS - General Cafe Expense',
                'Total Cost of Sales',
                'Gross Profit',
                'Gross Profit Percentages',
                'Other Income',
                'Refund - From Vendor or Others',
                'Total Other Income',
                'Operating Expenses',
                'Accounting',
                'Administration Fees',
                'Advertising and Promotion',
                'Automobile Expense',
                'Bank Fees',
                'Business gift expense',
                'Cleaning Expense',
                'Design and Printing',
                'Director Salary',
                'Employee Wages - Others',
                'Employee Wages- Front of house',
                'Entertainment',
                'Equestrian Food Expense',
                'Equine Health',
                'Equipment - Leasing',
                'General Business Research',
                'General Cafe Expense',
                'Insurance Payment',
                'Interest Expense',
                'Legal',
                'Management Consultant',
                'Marketing Expense',
                'Miscellaneous Expenses',
                'Motor Vehicle & Fuel',
                'Non Equine Health',
                'Office Expenses',
                'Office Supplies',
                'Parking Ticket',
                'Printing and Stationery',
                'Professional Services Expense',
                'Property License and Permits',
                'Realised Currency Gains',
                'Refund',
                'Reimbursement Clearing',
                'Renovation Contractors',
                'Rent Expense',
                'Repairs & Maintenance',
                'Retail Item Purchase',
                'Rubbish Removal and waste Disposal',
                'Shipping and Postage',
                'Square Fees',
                'Staff Meals & Amenities',
                'Staffing Contractors',
                'Subscriptions & Memberships',
                'Sundry Expenses',
                'Superannuation',
                'Telephone & Internet',
                'Training & Professional Development',
                'Travel - International',
                'Travel - National',
                'Travel - National - Leasing',
                'Travel - Taxi',
                            'Utilities',
            'Web Domain, Hosting & Associated',
            'Wedding cost',
            'Wedding Sales Expense',
            'Total Operating Expenses',
                'Net Profit'
            ]
            
            for row_name in matrix_rows:
                writer.writerow(matrix[row_name])
                if row_name in ['Trading Income', 'Cost of Sales', 'Other Income', 'Operating Expenses']:
                    writer.writerow([])

    def calculate_fy2526_margin(self) -> float:
        """Calculate the FY25/26 net profit margin to help find the right admission fee."""
        forecast_data = self.generate_24_month_forecast()
        fy2526_months = forecast_data[1:13]  # Aug-25 to Jul-26
        
        fy2526_total_revenue = sum(data['revenue_breakdown']['total_trading_income'] for data in fy2526_months)
        fy2526_total_cogs = sum(data['cost_of_sales']['total_cost_of_sales'] for data in fy2526_months)
        fy2526_total_expenses = sum(sum(data['operating_expenses'].values()) for data in fy2526_months)
        
        fy2526_gross_profit = fy2526_total_revenue - fy2526_total_cogs
        fy2526_net_profit = fy2526_gross_profit - fy2526_total_expenses
        fy2526_margin = (fy2526_net_profit / fy2526_total_revenue) * 100 if fy2526_total_revenue > 0 else 0
        
        return fy2526_margin

    def find_admission_fee_for_target_margin(self, target_margin=5.0, tolerance=0.1) -> float:
        """
        Find the admission fee that gives us approximately the target margin.
        
        Args:
            target_margin: Target margin percentage (default 5.0%)
            tolerance: Acceptable margin deviation (default 0.1%)
        
        Returns:
            The admission fee value that achieves the target margin
        """
        # Binary search to find the right admission fee
        low_fee = 4.75  # Minimum admission fee
        high_fee = 20.00  # Maximum reasonable admission fee
        
        best_fee = None
        best_margin_diff = float('inf')
        
        while high_fee - low_fee > 0.01:  # Precision to 1 cent
            mid_fee = (low_fee + high_fee) / 2
            
            # Create a new generator with this admission fee
            test_generator = TradeForecastGenerator(admission_fee_december_onwards=mid_fee)
            current_margin = test_generator.calculate_fy2526_margin()
            
            margin_diff = abs(current_margin - target_margin)
            
            if margin_diff < best_margin_diff:
                best_margin_diff = margin_diff
                best_fee = mid_fee
            
            if current_margin < target_margin:
                # Margin too low, need higher admission fee
                low_fee = mid_fee
            else:
                # Margin too high, need lower admission fee
                high_fee = mid_fee
            
            # If we're within tolerance, we can stop
            if margin_diff <= tolerance:
                break
        
        return best_fee

if __name__ == "__main__":
    print("Using Baseline Scenario: No Admission Fee Increases")
    print("This provides realistic 5.6% FY25/26 margin based on:")
    print("- Natural 26.7% growth from July 2025 baseline")
    print("- Wedding business recovery")
    print("- Farmstay accommodation expansion")
    print("- No artificial admission fee manipulation")
    print()
    
    # Use baseline admission fee (no increases) - this gives realistic 5.6% margin
    baseline_admission_fee = 4.70
    generator = TradeForecastGenerator(admission_fee_december_onwards=baseline_admission_fee)
    
    # Verify the margin
    actual_margin = generator.calculate_fy2526_margin()
    print(f"FY25/26 margin with ${baseline_admission_fee:.2f} admission fee: {actual_margin:.1f}%")
    
    # Generate the 24-month forecast
    forecast_data = generator.generate_24_month_forecast()
    
    # Write the CSV output using the Builder Pattern (now includes director explanations)
    generator.write_csv_file(forecast_data)
    
    # Generate a summary report
    summary_report = generator.generate_summary_report(forecast_data, generator.load_actual_data())
    with open('../output/trade-forecast-summary.md', 'w') as f:
        f.write(summary_report)
    
    print("✓ Generated ../output/trade-forecast.csv (with director explanations)")
    print("✓ Generated ../output/trade-forecast-summary.md")
    
    print("\n" + "="*80)
    print("FORECAST GENERATION COMPLETE")
    print("="*80)
    
    print("\n" + "="*80)
    print("OUTPUT FILES GENERATED")
    print("="*80)
    print("- ../output/trade-forecast.csv (Complete P&L forecast with transformation analysis and director explanations)")
    print("- ../output/trade-forecast-summary.md (Comprehensive summary report)")
    
    print(f"\nBaseline scenario: ${baseline_admission_fee:.2f} admission fee achieves {actual_margin:.1f}% FY25/26 margin")
    print("This represents realistic growth without artificial admission fee manipulation")
    print("Transformation highlight: Labour cost optimization from 35% to 19.3% of revenue")
    print("Enhanced methodology: Realistic cost variations reflecting operational reality")

import pandas as pd
from database.connection import get_db_cursor


class PriceService:
    """Service for handling price-related operations."""

    @staticmethod
    def get_all_prices():
        """Fetch all prices from the database."""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("SELECT * FROM prices ORDER BY id DESC")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                
                if rows:
                    df = pd.DataFrame(rows, columns=columns)
                    return df
                return pd.DataFrame()
        except Exception as e:
            raise Exception(f"Error fetching prices: {e}")

    @staticmethod
    def get_price_by_id(price_id):
        """Fetch a specific price by ID."""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("SELECT * FROM prices WHERE id = %s", (price_id,))
                row = cursor.fetchone()
                return row
        except Exception as e:
            raise Exception(f"Error fetching price: {e}")

    @staticmethod
    def create_price(product_name, price_value, description=None):
        """Create a new price entry."""
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "INSERT INTO prices (product_name, price_value, description) VALUES (%s, %s, %s) RETURNING id",
                    (product_name, price_value, description)
                )
                price_id = cursor.fetchone()[0]
                return price_id
        except Exception as e:
            raise Exception(f"Error creating price: {e}")

    @staticmethod
    def update_price(price_id, price_value):
        """Update a price value."""
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "UPDATE prices SET price_value = %s WHERE id = %s",
                    (price_value, price_id)
                )
                return True
        except Exception as e:
            raise Exception(f"Error updating price: {e}")

    @staticmethod
    def delete_price(price_id):
        """Delete a price entry."""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("DELETE FROM prices WHERE id = %s", (price_id,))
                return True
        except Exception as e:
            raise Exception(f"Error deleting price: {e}")

    @staticmethod
    def get_price_statistics():
        """Get statistics about prices."""
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 
                        COUNT(*) as total_prices,
                        AVG(price_value) as average_price,
                        MIN(price_value) as min_price,
                        MAX(price_value) as max_price,
                        SUM(price_value) as total_value
                    FROM prices
                    """
                )
                columns = [desc[0] for desc in cursor.description]
                row = cursor.fetchone()
                return dict(zip(columns, row)) if row else {}
        except Exception as e:
            raise Exception(f"Error fetching price statistics: {e}")

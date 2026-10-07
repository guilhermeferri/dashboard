import streamlit as st
from database.connection import test_connection
from services.price_service import PriceService

# Page configuration
st.set_page_config(
    page_title="Integrated Price Board",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point."""
    st.title("📊 Integrated Price Board")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Select Page:", ["Dashboard", "Prices", "Statistics", "Settings"])

    # Database connection check
    is_connected, message = test_connection()
    if not is_connected:
        st.error(f"❌ Database Connection Error: {message}")
        st.info("Please check your database configuration in the settings.")
        return

    st.success("✅ Database connected successfully")

    # Page routing
    if page == "Dashboard":
        show_dashboard()
    elif page == "Prices":
        show_prices()
    elif page == "Statistics":
        show_statistics()
    elif page == "Settings":
        show_settings()


def show_dashboard():
    """Display the main dashboard."""
    st.header("Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    try:
        stats = PriceService.get_price_statistics()
        
        with col1:
            st.metric(
                "Total Prices",
                stats.get('total_prices', 0)
            )
        
        with col2:
            st.metric(
                "Average Price",
                f"${stats.get('average_price', 0):.2f}"
            )
        
        with col3:
            st.metric(
                "Total Value",
                f"${stats.get('total_value', 0):.2f}"
            )
    except Exception as e:
        st.error(f"Error loading statistics: {e}")

    st.subheader("Recent Prices")
    try:
        df = PriceService.get_all_prices()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No prices found. Add some prices to get started!")
    except Exception as e:
        st.error(f"Error loading prices: {e}")


def show_prices():
    """Display prices management page."""
    st.header("Price Management")
    
    tab1, tab2 = st.tabs(["View Prices", "Add Price"])
    
    with tab1:
        st.subheader("All Prices")
        try:
            df = PriceService.get_all_prices()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No prices found yet.")
        except Exception as e:
            st.error(f"Error loading prices: {e}")
    
    with tab2:
        st.subheader("Add New Price")
        with st.form("add_price_form"):
            product_name = st.text_input("Product Name")
            price_value = st.number_input("Price Value", min_value=0.0, step=0.01)
            description = st.text_area("Description (optional)")
            
            submitted = st.form_submit_button("Add Price")
            
            if submitted:
                if product_name and price_value > 0:
                    try:
                        price_id = PriceService.create_price(product_name, price_value, description)
                        st.success(f"✅ Price added successfully! ID: {price_id}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding price: {e}")
                else:
                    st.warning("Please fill in the required fields.")


def show_statistics():
    """Display statistics page."""
    st.header("Statistics")
    
    try:
        stats = PriceService.get_price_statistics()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Price Summary")
            st.write(f"**Total Prices:** {stats.get('total_prices', 0)}")
            st.write(f"**Average Price:** ${stats.get('average_price', 0):.2f}")
            st.write(f"**Minimum Price:** ${stats.get('min_price', 0):.2f}")
            st.write(f"**Maximum Price:** ${stats.get('max_price', 0):.2f}")
            st.write(f"**Total Value:** ${stats.get('total_value', 0):.2f}")
        
        with col2:
            st.subheader("Metrics")
            if stats.get('total_prices', 0) > 0:
                price_range = stats.get('max_price', 0) - stats.get('min_price', 0)
                st.write(f"**Price Range:** ${price_range:.2f}")
    except Exception as e:
        st.error(f"Error loading statistics: {e}")


def show_settings():
    """Display settings page."""
    st.header("Settings")
    
    st.subheader("Database Configuration")
    
    from utils.config import DB_HOST, DB_PORT, DB_NAME, DB_USER
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Host:** {DB_HOST}")
        st.write(f"**Port:** {DB_PORT}")
    
    with col2:
        st.write(f"**Database:** {DB_NAME}")
        st.write(f"**User:** {DB_USER}")
    
    st.markdown("---")
    
    if st.button("Test Database Connection"):
        is_connected, message = test_connection()
        if is_connected:
            st.success(f"✅ {message}")
        else:
            st.error(f"❌ {message}")


if __name__ == "__main__":
    main()

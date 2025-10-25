import streamlit as st
def show_report():
    st.title("Report")
    st.markdown(
        """
    This Here is a concise Report of what happens in this Project
    """
    )
    # Introduction and Objectives
    st.markdown(
        """
    The Introduction of the project is 'To Analyze the Invalid Traffic occuring in the data'
    Objective : The Objective Of the Project is to analyze why there is invalid traffic in the data with the given specifications from the team
    """
    )
    # Overview of the Dataset
    st.markdown(
        """
    The dataset contains columns of:
    total_requests,unique_uas,unique-ip and other specific columns 
    It also has provided columns like requests_per_idfa,impressions_per_idfa,idfa_ua_ratio,idfa_ip_ratio to help us realize what is going through the dataset in this columns
    """
    )
    # Methodology
    st.markdown(
        """
    The Approach used for this project is as follows:
    1. We collected the dataset and read the csv file
    2. Cleaned the data and showcased its values
    3. Then the data is aggregated is at app level for making the analysis concise
    4. Then feature enginnering is used with the specifications provided to us and the specifications I preffered to be necessary
    5. Then EDA is performed
    """
    )
    # Correlation matrix
    st.markdown(
        """
    Shows how feature relationships align with IVT
    """
    )
    # Line chart
    st.markdown(
        """
    Created a time series visual for key metrics
    """
    )
    # Scatter Plot
    st.markdown(
        """
    Generated a scatter plot of idfa_ua ratio vs idfa_ip ratio
    """
    )
    # Histogram
    st.markdown(
        """
    Generated a histogram of IDfa_UA Ratio
    """
    )
    # comparision of IDFA-UA Ratio and IDFA-IP Ratio 
    st.markdown(
        """
    Showcased the comparision Of IDFa-UA Ratio and IDFa-IP ratio across app categories by showcasing them into boxpot
    """
    )
    # Conclusion
    st.markdown(
        """
    Device spoofing, as measured by 'idfa_ua_ratio', and proxy behaviors (high 'idfa_ip_ratio') are highly associated with IVT labeling.
    Apps with stable, low ratios seldom get flagged. Spikes predict IVT events.
    Going forward: Continuous monitoring of these metrics can trigger early fraud alerts and proactive review.
    """
    )
    # Next Step
    st.markdown(
        """
    We can use various predictive machine learning models for analyzing and predicting the anomalies in the IVT and also we can use clusttering algorithms for dividing the flagged IVT an dother into different clusters
    """
    )
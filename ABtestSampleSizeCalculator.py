import streamlit as st
import numpy as np
from scipy.stats import norm

def calculate_sample_size(stat_confidence, mdd, baseline, beta):
    alpha = 1 - stat_confidence
    p1 = baseline
    d = mdd
    p2 = p1 + d
    pooled_p = (p1 + p2) / 2
    pooled_q = 1 - pooled_p
    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(beta)
    
    n = ((z_alpha * np.sqrt(2 * pooled_p * pooled_q) + z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) / (p2 - p1))**2
    return n

# Streamlit app starts here
st.title('A/B Test Sample Size Calculator')

# Input controls
number_of_groups = st.number_input('Number of test groups including the control group', min_value=2, max_value=10, value=2)
baseline = st.slider('Baseline value of the test metric (%)', min_value=0.0, max_value=100.0, value=10.0, step=1.0, help="This is the expected value in the control group of the key metric being tested across the variant groups.") / 100
mdd = st.slider('Minimum detectable difference in test metric (%)', min_value=0.1, max_value=20.0, value=5.0, step=0.1, help="The test will be able to detect a difference in the key metric between the variant group(s) and the control group only if the difference is larger than this much. If the difference is smaller in reality, the test will fail to detect it.") / 100
beta = st.slider('Statistical power β', min_value=0.1, max_value=0.9, value=0.8, step=0.05, help="Represents the test's power, the likelihood of detecting an effect if there is one. Typically set at 0.8.")
stat_confidence = st.slider('Statistical Confidence in the Results 1-ɑ (%)', min_value=0.80, max_value=0.99, value=0.95, step=0.01, help="Reflects the confidence level that the test outcome didn't come about by chance. Higher values reduce false positive errors. Typically set to 0.95.")

# Calculation based on the current inputs
sample_size_per_group = calculate_sample_size(stat_confidence, mdd, baseline, beta)
total_sample_size = sample_size_per_group * number_of_groups

# Display the dynamic results
st.subheader('Required Sample Size')
st.metric(label="Minimum Sample Size per Group Needed", value=f"{int(sample_size_per_group)}")
st.metric(label="Total Sample Size Needed", value=f"{int(total_sample_size)}")

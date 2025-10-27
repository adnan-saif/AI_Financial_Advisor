import matplotlib.pyplot as plt
import seaborn as sns

# Visualization: Current Financial Health
def plot_current_financial_overview(user_data, analysis_data):
    expenses = user_data["expenses"]
    savings = analysis_data["savings"]

    labels = ["Expenses", "Savings"]
    values = [expenses, savings]
    colors = ["#FF6B6B", "#4D96FF"]

    fig, ax = plt.subplots(1, 2, figsize=(4.2, 2.0), dpi=130)
    
    ax[0].pie(
        values,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=140,
        textprops={'fontsize': 4},
        wedgeprops={'linewidth': 0.4, 'edgecolor': 'white'}
    )
    
    ax[1].bar(labels, values, color=colors, linewidth=0.4)
    ax[1].set_ylabel("Amount (₹)", fontsize=4, labelpad=5)
    ax[1].tick_params(axis='both', labelsize=4)
    ax[1].grid(axis="y", linestyle="--", alpha=0.3)

    plt.tight_layout(rect=[0, 0, 0.8, 0.8], pad=0.5, w_pad=0.6)
    return fig


# Visualization: Detailed Advised Financial Health
def plot_advised_financial_overview(user_data, analysis_data):

    expenses = user_data["expenses"]
    savings = analysis_data["savings"]
    emergency_fund_monthly = analysis_data["emergency_fund_monthly"]

    investment_allocation = analysis_data["recommended_investment_allocation"]
    high_interest = investment_allocation.get("High-Interest Savings / RD", 0)
    stocks = investment_allocation.get("Stocks / Equity Funds", 0)
    etfs = investment_allocation.get("ETFs / Balanced Funds", 0)
    risk_free = investment_allocation.get("Debt Mutual Funds / Bonds", 0)

    total_investments = high_interest + stocks + etfs + risk_free
    remaining_savings = max(0, savings - (emergency_fund_monthly + total_investments))

    labels = [
        "Expenses",
        "Emergency Fund (Monthly)",
        "High-Interest Savings",
        "Stocks",
        "Balanced Funds",
        "Risk-Free Investments",
        "Remaining Savings"
    ]
    values = [
        expenses,
        emergency_fund_monthly,
        high_interest,
        stocks,
        etfs,
        risk_free,
        remaining_savings
    ]

    colors = sns.color_palette("pastel", len(values))

    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor("#F9FAFB")

    wedges, texts, autotexts = ax[0].pie(
        values,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=120,
        pctdistance=0.8,
        labeldistance=1.1,
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    for text in texts: 
        text.set_fontsize(9)
        text.set_color("#333333")
    for autotext in autotexts: 
        autotext.set_fontsize(9)
        autotext.set_color("white")
        autotext.set_weight("bold")
    ax[0].set_title("Savings & Investment Distribution", pad=35, fontweight="bold", fontsize=11, color="#222222")

    sns.set_style("whitegrid")
    sns.barplot(
        x=labels,
        y=values,
        palette=colors,
        ax=ax[1]
    )
    ax[1].set_facecolor("#FFFFFF")
    ax[1].grid(axis="y", linestyle="--", alpha=0.5)
    ax[1].set_ylabel("Amount (₹)", fontsize=10, fontweight="bold", color="#222222")
    ax[1].tick_params(axis="x", rotation=90, labelsize=9)
    ax[1].set_title("Component-wise Financial Impact", pad=35, fontweight="bold", fontsize=11, color="#222222")

    for i, value in enumerate(values):
        ax[1].text(
            i,
            value + max(values) * 0.01,
            f"₹{value:,.0f}",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="#333333"
        )

    plt.tight_layout(rect=[0.05, 0.1, 0.95, 0.95])
    plt.subplots_adjust(wspace=0.4)

    return fig
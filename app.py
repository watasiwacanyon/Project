import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px
from faker import Faker

st.set_page_config(page_title="ITMO Security Monitor", layout="wide")
st.title("Центр мониторинга угроз")

fake = Faker()

country_coords = {
    "Russia": [61.0, 90.0],
    "USA": [37.0, -95.0],
    "China": [35.0, 105.0],
    "Germany": [51.0, 10.0],
    "France": [46.0, 2.0],
    "United Kingdom": [55.0, -3.0],
    "Japan": [36.0, 138.0],
    "Brazil": [-14.0, -51.0],
    "India": [20.0, 77.0],
    "Australia": [-25.0, 134.0],
    "Canada": [56.0, -106.0],
    "Mexico": [23.0, -102.0],
    "Nigeria": [8.0, 8.0],
    "South Africa": [-30.0, 25.0],
    "Egypt": [26.0, 30.0],
    "Saudi Arabia": [24.0, 45.0],
    "Iran": [32.0, 53.0],
    "Pakistan": [30.0, 70.0],
    "Indonesia": [-5.0, 120.0],
    "Italy": [42.0, 12.0],
    "Spain": [40.0, -4.0],
    "Ukraine": [49.0, 31.0],
    "Poland": [52.0, 20.0],
    "Kazakhstan": [48.0, 68.0],
    "Turkey": [39.0, 35.0],
    "Thailand": [15.0, 101.0],
    "Vietnam": [16.0, 108.0],
    "South Korea": [36.0, 128.0],
    "Argentina": [-36.0, -64.0],
    "Chile": [-33.0, -70.0],
    "Peru": [-9.0, -75.0],
    "Venezuela": [8.0, -66.0],
    "Colombia": [4.0, -74.0],
    "Sweden": [60.0, 18.0],
    "Norway": [65.0, 12.0],
    "Finland": [64.0, 26.0],
    "Denmark": [56.0, 10.0],
    "Netherlands": [52.0, 5.0],
    "Belgium": [50.0, 4.0],
    "Switzerland": [47.0, 8.0],
    "Austria": [47.0, 14.0],
    "Greece": [39.0, 22.0],
    "Portugal": [39.0, -8.0],
    "Ireland": [53.0, -8.0],
    "New Zealand": [-42.0, 174.0],
    "Philippines": [13.0, 122.0],
    "Malaysia": [4.0, 102.0],
    "Singapore": [1.3, 103.8],
    "United Arab Emirates": [24.0, 54.0],
    "Israel": [31.0, 35.0],
    "Morocco": [31.0, -7.0],
    "Kenya": [-1.0, 38.0],
}

def generate_threats(count=20):
    threats = []
    countries = list(country_coords.keys())
    for _ in range(count):
        country = random.choice(countries)
        coords = country_coords[country]
        lat = coords[0] + random.uniform(-3, 3)
        lon = coords[1] + random.uniform(-3, 3)
        severity = random.choices(
            ["Низкий", "Средний", "Высокий", "Критичный"],
            weights=[20, 40, 25, 15],
            k=1
        )[0]
        threats.append({
            "country": country,
            "lat": lat,
            "lon": lon,
            "severity": severity,
            "ip": fake.ipv4(),
            "port": random.randint(1, 65535),
            "timestamp": time.strftime("%H:%M:%S")
        })
    return threats

if "threats" not in st.session_state:
    st.session_state.threats = generate_threats(20)
    st.session_state.attack_count = 0
    st.session_state.frame = 0
    st.session_state.history = []


if st.button("Симулировать волну атак", use_container_width=True):
    new_threats = generate_threats(random.randint(5, 10))
    st.session_state.threats.extend(new_threats)
    st.session_state.attack_count += random.randint(1, 5)
    if len(st.session_state.threats) > 60:
        st.session_state.threats = st.session_state.threats[-60:]

if st.session_state.frame % 3 == 0 and len(st.session_state.threats) < 50:
    new_threats = generate_threats(random.randint(1, 2))
    st.session_state.threats.extend(new_threats)

st.session_state.frame += 1


df = pd.DataFrame(st.session_state.threats)

severity_colors = {
    "Низкий": "#00ff88",
    "Средний": "#ffcc00",
    "Высокий": "#ff6600",
    "Критичный": "#ff0044"
}


size_map = {"Низкий": 8, "Средний": 12, "Высокий": 18, "Критичный": 25}
df["size"] = df["severity"].map(size_map)


fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    color="severity",
    hover_name="country",
    hover_data={"ip": True, "severity": True, "port": True, "timestamp": True},
    color_discrete_map=severity_colors,
    title="Карта активных угроз в реальном времени",
    size="size",
    projection="natural earth",
    opacity=0.85,
    center={"lat": 20, "lon": 0}, 
    scope="world",
)


fig.update_layout(
    geo=dict(
        showland=True,
        landcolor="rgb(25, 25, 35)",
        countrycolor="rgb(80, 80, 100)",
        coastlinecolor="rgb(60, 60, 80)",
        showocean=True,
        oceancolor="rgb(10, 10, 20)",
        showcountries=True,
        showframe=False,
        bgcolor="rgb(10, 10, 20)",
        projection_scale=1,
    ),
    paper_bgcolor="rgb(15, 15, 25)",
    plot_bgcolor="rgb(15, 15, 25)",
    font_color="white",
    height=650,
    margin=dict(l=0, r=0, t=50, b=0),
    legend=dict(
        title="Уровень опасности",
        font=dict(color="white"),
        bgcolor="rgba(0,0,0,0.5)"
    ),
    autosize=False,
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Изменение количества угроз во времени")


current_count = len(df)
st.session_state.history.append(current_count)

if len(st.session_state.history) > 30:
    st.session_state.history = st.session_state.history[-30:]


history_df = pd.DataFrame({
    "Время": list(range(len(st.session_state.history))),
    "Угрозы": st.session_state.history
})


history_df["Сглаженное значение"] = history_df["Угрозы"].rolling(window=5, min_periods=1).mean()

fig_line = px.line(
    history_df,
    x="Время",
    y=["Угрозы", "Сглаженное значение"],
    title="Текущее количество угроз (синий) и сглаженный тренд (оранжевый)",
    labels={"value": "Количество угроз", "variable": "Тип"},
    color_discrete_map={"Угрозы": "#00aaff", "Сглаженное значение": "#ff8800"}
)

fig_line.update_layout(
    paper_bgcolor="rgb(15, 15, 25)",
    plot_bgcolor="rgb(15, 15, 25)",
    font_color="white",
    height=350,
    margin=dict(l=0, r=0, t=40, b=0),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig_line, use_container_width=True)

if len(history_df) > 5:
    last_values = history_df["Сглаженное значение"].tail(5)
    trend = last_values.iloc[-1] - last_values.iloc[0]
    future_value = int(last_values.iloc[-1] + trend * 0.3) 
    future_value = max(0, future_value)
else:
    future_value = current_count

col_pred1, col_pred2, col_pred3 = st.columns(3)
col_pred1.metric("Прогноз через 10 сек", f"{future_value} угроз")
col_pred2.metric("Текущий уровень", f"{current_count} угроз")
if future_value > current_count:
    col_pred3.metric(" Тренд", " Рост")
elif future_value < current_count:
    col_pred3.metric(" Тренд", " Спад")
else:
    col_pred3.metric(" Тренд", " Стабильно")

col1, col2, col3, col4 = st.columns(4)
critical = df[df["severity"] == "Критичный"].shape[0]
high = df[df["severity"] == "Высокий"].shape[0]
medium = df[df["severity"] == "Средний"].shape[0]
low = df[df["severity"] == "Низкий"].shape[0]

col1.metric("🔴 Критичных", critical)
col2.metric("🟠 Высоких", high)
col3.metric("🟡 Средних", medium)
col4.metric("🟢 Низких", low)

col5, col6, col7, col8 = st.columns(4)
col5.metric("Стран затронуто", df["country"].nunique())
col6.metric("Атак отражено", st.session_state.attack_count)
col7.metric("Всего угроз", len(df))
col8.metric("Обновлено", df["timestamp"].iloc[-1] if len(df) > 0 else "—")

with st.expander("Детальный лог угроз (последние 20)"):
    st.dataframe(
        df[["ip", "country", "severity", "port", "timestamp"]].tail(20),
        width='stretch',
        hide_index=True
    )

st.caption("Данные обновляются автоматически каждые 3 секунды")

time.sleep(5)
st.rerun()

with st.sidebar:
    st.image("https://itmo.ru/file/pages/231/logo.png", width=200)  # ЛОГО
    st.markdown("### О проекте")
    st.markdown("""
    **Цель:** Мониторинг киберугроз  
    **Технологии:** Python, Streamlit, Plotly  
    **Статус:** 🟢 Активен
    """)
    st.markdown("---")
    st.markdown(f"**Обновлено:** {time.strftime('%H:%M:%S')}")
    st.markdown(f"**Всего угроз:** {len(df)}")

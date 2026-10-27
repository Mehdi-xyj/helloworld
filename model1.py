import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
import plotly.graph_objects as go  # <-- 加上这一行，go 就是它的别名
from plotly.subplots import make_subplots
import pandas as pd
st.set_page_config(layout="wide")

#-----------------------------------------------------------侧边栏--------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
            <!-- 左侧图标 -->
            <div style="background-color: #9E2B2B; color: white; width: 58px; height: 58px; 
                        display: flex; flex-direction: column; justify-content: center; align-items: center; 
                        border-radius: 12px; font-weight: bold; font-size: 16px; line-height: 1.1; 
                        flex-shrink: 0; box-shadow: 0 2px 5px rgba(0,0,0,0.15);">
                <div>黄酒</div>
                <div>仿真</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.header("黄酒工艺仿真系统")
    st.caption("主要工序全要素仿真 · 设计 · 验证 · 优化")

# 定义一个渲染卡片的辅助函数，保持代码整洁
def kpi_card(label, value):
    st.markdown(
        f"""
        <div style="margin-bottom: 10px;">
            <div style="font-size: 14px; color: #808495; margin-bottom: 2px;">{label}</div>
            <div style="font-size: 20px; font-weight: 700; color: var(--text-color); line-height: 1.2;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

#---------------------------------------------------------------------系统运行指标-----------------------------------------------------------
st.subheader("系统运行指标")

# 第一行：直接在 columns 里调用你的函数，不要用 .metric
col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("模型链", "CHAIN-v2.1")
with col2:
    kpi_card("工序数", "10 工序 / 5 要素")
with col3:
    kpi_card("基准批次", "SJ-2026-088")
with col4:
    kpi_card("产能基准", "1,000 kg 糯米 / 批")
st.write("")
#--------------------------------------------------------------------核心工艺指标---------------------------------------------------------------
st.subheader("核心工艺指标")

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric(label="出酒率", value="1.86", help="kg/kg 米", delta="较基准 持平")
col2.metric(label="吨酒成本", value="3,295", help="元/吨", delta="较基准 持平")
col3.metric(label="吨酒综合能耗", value="49.2", help="kgce/t", delta="蒸汽占比 75%")
col4.metric(label="生产周期", value="396", help="天", delta="含陈酿 12 个月")
col5.metric(label="酒精度", value="18.4", help="%vol", delta="达标")
col6.metric(label="总酸", value="6.1", help="g/L", delta="适宜")

# 调用这一行，原生 metric 瞬间变好看
style_metric_cards(
    background_color="transparent", # 透明背景
    border_size_px=1,               # 边框粗细
    border_color="rgba(128,128,128,0.2)", # 边框颜色
    border_radius_px=8,             # 圆角
    border_left_color="#D35400",    # 左侧彩色竖条颜色
)
st.write("")
#-------------------------------------------------------------------工序链-------------------------------------------------------------------
st.subheader("工序链")
st.caption("带 🟡 标识表示该工序为当前瓶颈或风险项")

# 1. 准备数据：把原来的两行参数拆分成 value(主数值) 和 delta(副数值)
process_data = [
    {"id": "01", "title": "浸米", "v": "1,297 kg", "d": "3.0 天", "risk": False},
    {"id": "02", "title": "蒸饭", "v": "糊化 96%", "d": "0.35 天", "risk": False},
    {"id": "03", "title": "摊凉", "v": "28 ℃", "d": "0.25 天", "risk": False},
    {"id": "04", "title": "落缸配料", "v": "2,607 kg", "d": "水 1,200", "risk": False},
    {"id": "05", "title": "前发酵", "v": "7.4 d 主发", "d": "峰温 31.0℃", "risk": False},
    {"id": "06", "title": "后发酵", "v": "17 ℃", "d": "26 天", "risk": False},
    {"id": "07", "title": "压榨", "v": "1,944 kg 酒液", "d": "糟 362 kg", "risk": True}, # 风险项
    {"id": "08", "title": "煎酒", "v": "428 kg 汽", "d": "0.6 天", "risk": False},
    {"id": "09", "title": "陈酿", "v": "12 个月", "d": "损 2.5%", "risk": False},
    {"id": "10", "title": "灌装", "v": "1,857 kg", "d": "1.86 kg/kg", "risk": False},
]
# 2. 第一行：前 6 个指标
cols_row1 = st.columns(6)
for i in range(6):
    item = process_data[i]
    # 用 emoji 替代绝对定位的黄点
    risk_mark = " 🟡" if item["risk"] else ""
    with cols_row1[i]:
        st.metric(
            label=f"{item['id']} {item['title']}{risk_mark}",
            value=item["v"],
            delta=item["d"],
            delta_color="off" # 关闭红绿箭头，保持灰色文本
        )

st.write("") # 加点间距

# 3. 第二行：后 4 个指标
cols_row2 = st.columns(6)
for i in range(4):
    item = process_data[i + 6]
    risk_mark = " 🟡" if item["risk"] else ""
    with cols_row2[i]:
        st.metric(
            label=f"{item['id']} {item['title']}{risk_mark}",
            value=item["v"],
            delta=item["d"],
            delta_color="off"
        )

# 1. 顶部标签页 (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["工艺设计与参数", "物料与能量平衡", "成本与周期", "敏感性与优化"])

with tab1:
    # 将页面划分为左右两列，比例 1:1 (也可以调成 4:6 等)
    col_left, col_right = st.columns([1, 1], gap="large")
    
    # ----------------------------------------
    # 左侧：工序参数
    # ----------------------------------------
    with col_left:
        with st.container(border=True):
            col_title, col_btn = st.columns([8, 2])
            with col_title:
                st.markdown("**工序参数**")
            with col_btn:
                st.button("复位基准", use_container_width=True)
                
            st.divider()
            
            st.markdown('<div class="group-title">原料与浸米</div>', unsafe_allow_html=True)
            # 将滑块的值赋给变量！这里假设吸水率会影响物料
            water_rate = st.slider("浸米吸水率", 0.0, 100.0, 30.0, step=0.01, format="%.2f%%")
            st.slider("浸米天数", 0.0, 10.0, 3.0, step=0.1, format="%.1f 天")
            st.slider("原料淀粉含量", 0.0, 100.0, 78.0, step=0.01, format="%.2f%%")
            
            st.markdown('<div class="group-title">蒸饭</div>', unsafe_allow_html=True)
            st.slider("糊化度", 0.0, 100.0, 96.0, step=0.01, format="%.3f%%")
            # 假设蒸汽单耗影响能量
            steam_usage = st.slider("蒸饭蒸汽单耗", 0.0, 1.0, 0.30, step=0.01, format="%.2f kg/kg")
            
            # ... (中间省略其他滑块) ...

            st.markdown('<div class="group-title">发酵</div>', unsafe_allow_html=True)
            # 假设前发酵天数影响时间
            fementation_days = st.slider("前发酵天数", min_value=2.0, max_value=7.0, value=4.0, step=0.5, format="%.2f 天")
            
            st.divider() 

            st.markdown('<div class="group-title">压榨与后处理</div>', unsafe_allow_html=True)
            # 假设陈酿时长影响时间
            aging_months = st.slider("陈酿时长", min_value=3.0, max_value=36.0, value=12.0, step=1.0, format="%.2f 月")
    # 数据处理：根据左侧参数，动态计算右侧指标
    # ==========================================
    # 这里用简单的公式模拟联动，你需要替换成真实的业务公式
    calc_material = 1.86 + (water_rate - 30) * 0.01     # 吸水率越高，物料产出可能变化
    calc_energy = 49.2 + (steam_usage - 0.30) * 10      # 蒸汽越高，能耗越高
    calc_time = 360 + fementation_days + aging_months * 30 # 发酵+陈酿决定总时间
    calc_cost = 3295 + (calc_energy - 49.2) * 15        # 能耗决定部分成本

    # 动态生成状态列表 (判断是否优于基准)
    data = [
        ("物料", f"{calc_material:.2f} kg/kg 米", "优于基准" if calc_material >= 1.86 else "劣于基准", calc_material >= 1.86),
        ("能量", f"{calc_energy:.1f} kgce/t", "优于基准" if calc_energy <= 49.2 else "劣于基准", calc_energy <= 49.2),
        ("时间", f"{calc_time:.0f} 天", f"含陈酿 {aging_months:.0f} 个月", calc_time <= 396),
        ("成本", f"{calc_cost:,.0f} 元/t", "优于基准" if calc_cost <= 3295 else "劣于基准", calc_cost <= 3295),
        ("质量", "半干型 · 18.4%", "优于基准", True) # 假设质量不变
    ]
    # 右侧：五要素状态（使用动态生成的 data）
    # ==========================================
    with col_right:
        with st.container(border=True):
            st.markdown("**五要素参数**")
            st.write("")
            
            # 循环渲染刚刚计算出的最新数据
            for i, (label, value, tag_text, is_better) in enumerate(data):
                c1, c2, c3 = st.columns([2, 4, 4])
                
                with c1:
                    st.write(label)
                with c2:
                    # 右对齐
                    st.markdown(f"<div style='text-align: right; font-size: 15px;'>{value}</div>", unsafe_allow_html=True)
                with c3:
                    # 根据 True/False 动态切换颜色
                    if is_better:
                        st.markdown(f":green-background[**{tag_text}**]")
                    else:
                        st.markdown(f":orange-background[**{tag_text}**]")
                
                if i < len(data) - 1:
                    st.divider()
            
        st.write("") # 间距
        
        # 卡片 2：发酵过程曲线
        with st.container(border=True):
            # 标题行
            col_t, col_c = st.columns([7, 3])
            with col_t:
                st.markdown("**发酵过程曲线**")
            with col_c:
                st.markdown("<div style='text-align: right; color: #808495; font-size: 12px; margin-top: 5px;'>30 天 · 由 6 维机理模型实时求解</div>", unsafe_allow_html=True)
            
            # 使用 Plotly 绘制双 Y 轴折线图
            # 1. 模拟数据
            days = [0, 5, 10, 15, 20, 25, 30]
            ethanol = [0, 30, 60, 80, 95, 110, 120]
            sugar = [0, 100, 80, 60, 40, 25, 15]
            temp = [25, 32, 18, 17, 17, 17, 17]
            
            # 2. 创建图表
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # 添加轨迹
            fig.add_trace(go.Scatter(x=days, y=ethanol, name="乙醇 g/L", line=dict(color="#8B0000", width=2)), secondary_y=False)
            fig.add_trace(go.Scatter(x=days, y=sugar, name="还原糖 g/L", line=dict(color="#B8860B", width=2, dash='dash')), secondary_y=False)
            fig.add_trace(go.Scatter(x=days, y=temp, name="品温 ℃", line=dict(color="#1f77b4", width=2)), secondary_y=True)
            
            # 3. 美化图表（去掉网格线，调整图例位置）
            fig.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                height=280,
                legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="left", x=0),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            fig.update_xaxes(showgrid=False, tickvals=days, tickprefix="D", tickfont=dict(color="#808495"))
            fig.update_yaxes(showgrid=False, tickfont=dict(color="#808495"))
            
            # 4. 在 Streamlit 中渲染
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})



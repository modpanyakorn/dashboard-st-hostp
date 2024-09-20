import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode
from streamlit_modal import Modal

# ฟังก์ชัน JavaScript สำหรับกำหนดสีพื้นหลังในคอลัมน์ '__df__'
cell_style_js = JsCode("""
    function(params) {
        if (params.value < 0) {
            return {'backgroundColor': 'red'};
        } else if (params.value > 0) {
            return {'backgroundColor': 'green'};
        }
        return {};
    }
""")

# โหลดข้อมูลจาก CSV
df = pd.read_csv('D:/Working/dashboard-st-hostp/src/patient1.csv')

# แสดงเฉพาะบางคอลัมน์ที่ต้องการ
df_show = df.drop(['NUMBER', '__PATIENT_NAME__', '__DEBT_VALUE__'], axis=1)

# ตั้งค่าให้ตารางมีฟังก์ชันเลือกแถวได้
gb = GridOptionsBuilder.from_dataframe(df_show)

# กำหนดสีสำหรับคอลัมน์ '__df__' โดยใช้ JsCode
gb.configure_column('__df__', cellStyle=cell_style_js)

# กำหนดให้สามารถเลือกแถวได้
gb.configure_selection(selection_mode='single')
grid_options = gb.build()

# แสดงตารางพร้อมให้เลือกแถว
st.title("Data Set")
grid_response = AgGrid(
    df_show,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,  # อัปเดตเมื่อเลือกแถว
    theme='streamlit',  # ธีมของตาราง
    height=600,  # ปรับความสูงตาราง
    width='100%',  # ปรับความกว้างตารางให้เต็มหน้าจอ
    fit_columns_on_grid_load=True,  # ปรับขนาดคอลัมน์ให้เต็มพื้นที่ตาราง
    allow_unsafe_jscode=True,  # เปิดใช้งาน unsafe jscode
)

# ดึงข้อมูลแถวที่เลือก
selected_row = grid_response.get('selected_rows', [])

# สร้าง Modal
modal = Modal(
    "ข้อมูลผู้ป่วย", 
    key="demo-modal",
    padding=20,
    max_width=744
)

# จัดปุ่ม "SHOW" ไปทางขวา
col1, col2 = st.columns([8, 2])
with col2:
    btn = st.button("SHOW")  # ปุ่มอยู่ทางขวา

# ตรวจสอบว่ามีการกดปุ่มและมีการเลือกแถวแล้ว
if btn and len(selected_row) > 0:
    modal.open()

if modal.is_open():
    with modal.container():
        # ปรับขนาดของข้อความโดยใช้ HTML
        st.markdown(f"<h3>__HN__: {selected_row.iloc[0, 0]}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h4>__DATE__: {selected_row.iloc[0, 1]}</h4>", unsafe_allow_html=True)

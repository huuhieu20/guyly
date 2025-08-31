import streamlit as st

st.set_page_config(page_title="Thực đơn hôm nay", page_icon="🍽️", layout="centered")

st.title("🍽️ Chọn thực đơn yêu thích")

# Danh sách món ăn mẫu
mon_khai_vi = ["Gỏi cuốn", "Súp bí đỏ", "Salad rau", "Nem rán"]
mon_chinh   = ["Cơm gà", "Bún bò", "Phở bò", "Cá kho", "Thịt kho trứng"]
mon_trang_mieng = ["Trái cây", "Chè đậu xanh", "Bánh flan", "Kem"]

with st.form("form_thuc_don"):
    khai_vi = st.selectbox("Món khai vị ưa thích của bạn?", mon_khai_vi)
    chinh   = st.selectbox("Món chính ưa thích của bạn?", mon_chinh)
    trang_mieng = st.selectbox("Món tráng miệng ưa thích của bạn?", mon_trang_mieng)

    submit = st.form_submit_button("Xác nhận")

if submit:
    st.success("✅ Bạn đã chọn thực đơn:")
    st.write(f"- **Khai vị:** {khai_vi}")
    st.write(f"- **Món chính:** {chinh}")
    st.write(f"- **Tráng miệng:** {trang_mieng}")


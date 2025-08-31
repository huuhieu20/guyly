import streamlit as st

st.set_page_config(page_title="Thực đơn trong ngày", page_icon="🍴", layout="centered")

st.title("🍴 Thực đơn các bữa ăn trong ngày")

# Danh sách món ăn
mon_sang = ["Xôi", "Bánh mì", "Phở", "Bún riêu", "Cháo"]
mon_man = ["Thịt kho", "Cá kho", "Gà rán", "Bò xào", "Tôm rim"]
mon_rau_canh = ["Canh rau ngót", "Canh bí", "Rau muống xào", "Canh chua", "Salad rau"]

# Bữa sáng
buoi_sang = st.multiselect("🍳 Bữa sáng", mon_sang)

# Bữa trưa
buoi_trua_man = st.multiselect("🍛 Bữa trưa - Món mặn (chọn 2)", mon_man)
buoi_trua_rau = st.multiselect("🥗 Bữa trưa - Món rau/canh (chọn 1)", mon_rau_canh)

# Bữa tối
buoi_toi_man = st.multiselect("🍲 Bữa tối - Món mặn (chọn 2)", mon_man)
buoi_toi_rau = st.multiselect("🥬 Bữa tối - Món rau/canh (chọn 1)", mon_rau_canh)

# Hiển thị thực đơn đã chọn
st.subheader("📋 Xem trước thực đơn của bạn")
st.write("**Bữa sáng:**", ", ".join(buoi_sang) if buoi_sang else "Chưa chọn")
st.write("**Bữa trưa:**", ", ".join(buoi_trua_man + buoi_trua_rau) if buoi_trua_man or buoi_trua_rau else "Chưa chọn")
st.write("**Bữa tối:**", ", ".join(buoi_toi_man + buoi_toi_rau) if buoi_toi_man or buoi_toi_rau else "Chưa chọn")

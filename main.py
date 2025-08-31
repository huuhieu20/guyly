import random
import streamlit as st
import pandas as pd
from datetime import date
import io

st.set_page_config(page_title="Thực đơn trong ngày", page_icon="🍲", layout="wide")

# -----------------------------
# DANH SÁCH MÓN ĂN (RÚT GỌN)
# -----------------------------
BUA_SANG = ["Xôi", "Bánh mì", "Phở", "Bún", "Cháo"]
MON_MAN = ["Thịt kho", "Gà chiên", "Cá kho", "Tôm rim", "Trứng chiên"]
RAU = ["Rau muống xào", "Rau lang luộc", "Cải thìa xào"]
CANH = ["Canh chua", "Canh rau ngót", "Canh bí đỏ"]

RAU_HOAC_CANH = ["(Rau) " + r for r in RAU] + ["(Canh) " + c for c in CANH]

# -----------------------------
# HÀM KIỂM TRA
# -----------------------------
def kiem_tra_bua_an(mon_man, mon_phu):
    loi = []
    if len(mon_man) != 2:
        loi.append("Cần chọn đúng **2 món mặn**.")
    if len(mon_phu) != 1:
        loi.append("Cần chọn đúng **1 món rau hoặc canh**.")
    return loi

def tong_hop(thuc_don):
    rows = []
    for b in thuc_don.get("sang", []):
        rows.append({"Bữa": "Sáng", "Món": b})
    for m in thuc_don.get("trua_man", []):
        rows.append({"Bữa": "Trưa (mặn)", "Món": m})
    for s in thuc_don.get("trua_phu", []):
        rows.append({"Bữa": "Trưa (rau/canh)", "Món": s})
    for m in thuc_don.get("toi_man", []):
        rows.append({"Bữa": "Tối (mặn)", "Món": m})
    for s in thuc_don.get("toi_phu", []):
        rows.append({"Bữa": "Tối (rau/canh)", "Món": s})
    return pd.DataFrame(rows)

def tai_xuong(df):
    csv = df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button("⬇️ Tải CSV", data=csv, file_name=f"thuc_don_{date.today()}.csv", mime="text/csv")

    buf = io.StringIO()
    buf.write("# Thực đơn trong ngày\n\n")
    for bua in ["Sáng", "Trưa (mặn)", "Trưa (rau/canh)", "Tối (mặn)", "Tối (rau/canh)"]:
        mon = df[df["Bữa"] == bua]["Món"].tolist()
        buf.write(f"**{bua}**: {', '.join(mon) if mon else '_(chưa chọn)_'}\n\n")
    st.download_button("⬇️ Tải Markdown", data=buf.getvalue(), file_name=f"thuc_don_{date.today()}.md", mime="text/markdown")

# -----------------------------
# GIAO DIỆN
# -----------------------------
st.title("🍲 Thực đơn trong ngày")
st.caption("Bữa trưa và tối phải có **2 món mặn + 1 món rau hoặc canh**.")

tab1, tab2, tab3 = st.tabs(["Bữa sáng", "Bữa trưa", "Bữa tối"])

with tab1:
    st.subheader("🍳 Bữa sáng")
    bua_sang = st.multiselect("Chọn món:", options=BUA_SANG, key="sang")

with tab2:
    st.subheader("🍛 Bữa trưa")
    col1, col2 = st.columns(2)
    with col1:
        trua_man = st.multiselect("Chọn 2 món mặn:", options=MON_MAN, key="trua_man")
    with col2:
        trua_phu = st.multiselect("Chọn 1 món rau hoặc canh:", options=RAU_HOAC_CANH, key="trua_phu")

    for loi in kiem_tra_bua_an(trua_man, trua_phu):
        st.error(loi)

with tab3:
    st.subheader("🍜 Bữa tối")
    col1, col2 = st.columns(2)
    with col1:
        toi_man = st.multiselect("Chọn 2 món mặn:", options=MON_MAN, key="toi_man")
    with col2:
        toi_phu = st.multiselect("Chọn 1 món rau hoặc canh:", options=RAU_HOAC_CANH, key="toi_phu")

    for loi in kiem_tra_bua_an(toi_man, toi_phu):
        st.error(loi)

st.markdown("---")
st.subheader("📋 Thực đơn tổng hợp")

thuc_don = {
    "sang": st.session_state.get("sang", []),
    "trua_man": st.session_state.get("trua_man", []),
    "trua_phu": st.session_state.get("trua_phu", []),
    "toi_man": st.session_state.get("toi_man", []),
    "toi_phu": st.session_state.get("toi_phu", []),
}

df = tong_hop(thuc_don)
st.dataframe(df, hide_index=True, use_container_width=True)

# Kiểm tra hợp lệ
hop_le = not kiem_tra_bua_an(thuc_don["trua_man"], thuc_don["trua_phu"]) \
         and not kiem_tra_bua_an(thuc_don["toi_man"], thuc_don["toi_phu"])

if hop_le:
    st.success("✅ Thực đơn hợp lệ. Bạn có thể tải xuống.")
    tai_xuong(df)
else:
    st.info("👆 Hãy chọn đúng quy tắc cho bữa trưa và tối để tải xuống.")

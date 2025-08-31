import random
import io
from datetime import date

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lên thực đơn trong ngày", page_icon="🍽️", layout="centered")

# --------- DANH SÁCH MÓN ĂN (RÚT GỌN, TIẾNG VIỆT) ----------
BUA_SANG = ["Xôi", "Bánh mì", "Phở", "Bún", "Cháo"]
MON_MAN = ["Thịt kho", "Gà chiên", "Cá kho", "Tôm rim", "Trứng chiên"]
RAU = ["Rau muống xào", "Rau lang luộc", "Cải thìa xào"]
CANH = ["Canh chua", "Canh rau ngót", "Canh bí đỏ"]
RAU_OR_CANH = ["(Rau) " + r for r in RAU] + ["(Canh) " + c for c in CANH]

# --------- HÀM HỖ TRỢ ----------
def kiem_tra_quy_tac(manan, phu):
    """Trả về danh sách lỗi nếu vi phạm: manan phải có 2 món; phu phải có 1 món."""
    loi = []
    if len(manan) != 2:
        loi.append("Cần chọn đúng **2 món mặn**.")
    if len(phu) != 1:
        loi.append("Cần chọn đúng **1 món rau hoặc canh**.")
    return loi

def tao_dataframe(plan):
    rows = []
    for m in plan["sang"]:
        rows.append({"Bữa": "Sáng", "Món": m})
    for m in plan["trua_man"]:
        rows.append({"Bữa": "Trưa (mặn)", "Món": m})
    for m in plan["trua_phu"]:
        rows.append({"Bữa": "Trưa (rau/canh)", "Món": m})
    for m in plan["toi_man"]:
        rows.append({"Bữa": "Tối (mặn)", "Món": m})
    for m in plan["toi_phu"]:
        rows.append({"Bữa": "Tối (rau/canh)", "Món": m})
    return pd.DataFrame(rows)

def download_buttons(df):
    csv = df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button("⬇️ Tải CSV", data=csv, file_name=f"thuc_don_{date.today()}.csv", mime="text/csv")
    md = io.StringIO()
    md.write("# Thực đơn trong ngày\n\n")
    for bua in ["Sáng", "Trưa (mặn)", "Trưa (rau/canh)", "Tối (mặn)", "Tối (rau/canh)"]:
        items = df[df["Bữa"] == bua]["Món"].tolist()
        md.write(f"**{bua}**: {', '.join(items) if items else '_(chưa chọn)_'}\n\n")
    st.download_button("⬇️ Tải Markdown", data=md.getvalue(), file_name=f"thuc_don_{date.today()}.md", mime="text/markdown")

# --------- GIAO DIỆN (FORM + MULTISELECT) ----------
st.title("🍲 Lên thực đơn trong ngày")
st.caption("Quy tắc: Bữa trưa & bữa tối = **2 món mặn** + **1 món rau hoặc canh**.")

with st.form("form_thuc_don"):
    st.subheader("Bữa sáng")
    sang = st.multiselect("Chọn món cho bữa sáng (có thể chọn nhiều):", options=BUA_SANG, default=[])

    st.subheader("Bữa trưa")
    trua_man = st.multiselect("Chọn 2 món mặn (trưa):", options=MON_MAN, default=[])
    trua_phu = st.multiselect("Chọn 1 món rau hoặc canh (trưa):", options=RAU_OR_CANH, default=[])

    st.subheader("Bữa tối")
    toi_man = st.multiselect("Chọn 2 món mặn (tối):", options=MON_MAN, default=[])
    toi_phu = st.multiselect("Chọn 1 món rau hoặc canh (tối):", options=RAU_OR_CANH, default=[])

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        submit = st.form_submit_button("Xác nhận")
    with col2:
        if st.form_submit_button("Gợi ý nhanh"):
            # Gợi ý: random nhưng tuân thủ quy tắc
            trua_man = random.sample(MON_MAN, 2)
            trua_phu = [random.choice(RAU_OR_CANH)]
            toi_man = random.sample(MON_MAN, 2)
            toi_phu = [random.choice(RAU_OR_CANH)]
            # lưu tạm vào session để khi submit hiện lên
            st.session_state["g_trua_man"] = trua_man
            st.session_state["g_trua_phu"] = trua_phu
            st.session_state["g_toi_man"] = toi_man
            st.session_state["g_toi_phu"] = toi_phu
            st.experimental_rerun()
    with col3:
        if st.form_submit_button("Xoá chọn"):
            for k in ["sang","trua_man","trua_phu","toi_man","toi_phu"]:
                st.session_state[k] = []

# Nếu người dùng vừa bấm "Gợi ý nhanh" chúng ta có dữ liệu trong session
if "g_trua_man" in st.session_state:
    trua_man = st.session_state.get("g_trua_man", trua_man)
    trua_phu = st.session_state.get("g_trua_phu", trua_phu)
    toi_man = st.session_state.get("g_toi_man", toi_man)
    toi_phu = st.session_state.get("g_toi_phu", toi_phu)

# Hiện kết quả khi nhấn xác nhận
if submit:
    loi_trua = kiem_tra_quy_tac(trua_man, trua_phu)
    loi_toi = kiem_tra_quy_tac(toi_man, toi_phu)
    if loi_trua or loi_toi:
        st.error("Thực đơn chưa hợp lệ:")
        for e in loi_trua + loi_toi:
            st.write("- " + e)
        st.info("Vui lòng sửa để đúng: **2 món mặn** và **1 món rau hoặc canh** cho cả trưa & tối.")
    else:
        st.success("✅ Thực đơn hợp lệ")
        plan = {
            "sang": sang,
            "trua_man": trua_man,
            "trua_phu": trua_phu,
            "toi_man": toi_man,
            "toi_phu": toi_phu
        }
        df = tao_dataframe(plan)
        st.subheader("📋 Tổng hợp thực đơn")
        st.dataframe(df, use_container_width=True, hide_index=True)
        download_buttons(df)

# Nếu chưa submit, vẫn hiển thị tổng quan dựa trên session để người dùng thấy lựa chọn
else:
    preview = {
        "sang": st.session_state.get("sang", []),
        "trua_man": st.session_state.get("trua_man", []),
        "trua_phu": st.session_state.get("trua_phu", []),
        "toi_man": st.session_state.get("toi_man", []),
        "toi_phu": st.session_state.get("toi_phu", []),
    }
    df_preview = tao_dataframe(preview)
    st.subheader("📋 Xem trước (chưa xác nhận)")
    st.dataframe(df_preview, use_container_width=True, hide_index=True)

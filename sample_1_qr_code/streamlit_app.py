from io import BytesIO
import streamlit as st
import qrcode
import cv2
import numpy as np


error_corrections = {
    "L": qrcode.constants.ERROR_CORRECT_L,
    "M": qrcode.constants.ERROR_CORRECT_M,
    "Q": qrcode.constants.ERROR_CORRECT_Q,
    "H": qrcode.constants.ERROR_CORRECT_H,
}


st.title("QRコード生成・確認アプリ")
st.write("QRコードの生成やQRコード画像の確認を行います")


@st.cache_data
def generate_qr_code(text, version, error_correction, box_size, border) -> bytes:
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    with BytesIO() as output:
        img.save(output, format="PNG")
        img_value = output.getvalue()
    return img_value


st.subheader("QRコード生成")
text = st.text_input("QRコードに変換したい文字列を入力してください")
version = st.slider("バージョン", 1, 40, 1)
error_level = st.selectbox(
    "誤り訂正レベル",
    ["L", "M", "Q", "H"],
)
box_size = st.slider("ボックスサイズ (QRコードの各「ボックス」のピクセル数)", 1, 50, 5)
border = st.slider("ボーダー(画像の隙間サイズ)", 1, 20, 4)
if text or st.button("QRコードを確認"):
    if error_level is not None:
        error_correction = error_corrections.get(
            error_level, qrcode.constants.ERROR_CORRECT_L
        )
    else:
        error_correction = qrcode.constants.ERROR_CORRECT_L
    img_value = generate_qr_code(text, version, error_correction, box_size, border)
    st.image(img_value)
    st.write(f"QRコード文字列: {text}")
    st.download_button(
        "QRコードをダウンロード",
        data=img_value,
        file_name="qr_code.png",
        mime="image/png",
    )


st.subheader("QRコード確認")
uploaded_file = st.file_uploader(
    "QRコード画像をアップロード",
    type=["png", "jpg", "jpeg", "svg", "gif", "bmp", "tiff", "webp"],
)

if uploaded_file:
    uploaded_file_bytes = uploaded_file.read()
    uploaded_array = np.frombuffer(uploaded_file_bytes, np.uint8)
    uploaded_img = cv2.imdecode(uploaded_array, cv2.IMREAD_COLOR)
    qrdetector = cv2.QRCodeDetectorAruco()
    retval, decoded_info, points, straight_code = qrdetector.detectAndDecodeMulti(
        uploaded_img
    )
    if retval:
        for i, info in enumerate(decoded_info):
            st.write(f"No.{i+1} QRコード文字列: {info}")
    else:
        st.error("QRコードが見つかりませんでした")
    st.write("アップロードしたファイルの画像")
    st.image(uploaded_file_bytes)

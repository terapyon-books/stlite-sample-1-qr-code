from io import BytesIO
import streamlit as st
import qrcode  # type: ignore
import cv2
import numpy as np


st.title("QRコード生成・確認アプリ")
st.text("QRコードの生成やQRコード画像の確認を行います")


@st.cache_data
def generate_qr_code(text) -> bytes:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
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
if text or st.button("QRコードを確認"):
    img_value = generate_qr_code(text)
    st.image(img_value, width=150)
    st.text(f"QRコード文字列: {text}")
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
        new_img = cv2.polylines(
            uploaded_img, points.astype(int), True, (0, 0, 255), thickness=2
        )
        text_offset = 10
        for i, info in enumerate(decoded_info):
            st.text(f"No.{i+1} QRコード文字列: {info}")
            points_of_this = points[i, :, :].astype(int)
            new_img = cv2.putText(
                new_img,
                f"No. {i+1}",
                (points_of_this[0, 0], points_of_this[0, 1] - text_offset),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (0, 0, 255),
                thickness=2,
                lineType=cv2.LINE_AA,
            )
        st.image(new_img, width=300)
    else:
        st.text("QRコードが見つかりませんでした")

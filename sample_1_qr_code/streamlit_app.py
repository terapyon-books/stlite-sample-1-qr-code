from io import BytesIO
import streamlit as st
import qrcode


st.title("QRコード生成・確認アプリ")
st.text("QRコードの生成やQRコード画像の確認を行います")


@st.cache_data
def generate_qr_code(text: str) -> bytes:
    with BytesIO() as output:
        img.save(output, format="PNG")
        img_value = output.getvalue()
        return img_value


text = st.text_input("QRコードに変換したい文字列を入力してください")
if text:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    if st.button("QRコードを確認"): 
        img_value = generate_qr_code(text)
        st.image(img_value, use_column_width=True)
        st.download_button(
            "QRコードをダウンロード",
            data=img_value,
            file_name="qr_code.png",
            mime="image/png",
        )

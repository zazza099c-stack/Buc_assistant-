import time
import streamlit as st
from google import genai
from google. genai import types
st.set_page_config(page_title="مساعد البكالوريا الذكي", page_icon="🎒")
with st.sidebar:
  st.header("⚙️ إعدادات المنصه")
  api_key = st.text_input( 
                                  "type="password ,":الخاص بك Gemini API أدخل المفتاح"
)
st.divider()
st.subheader("☕️ ادعم استمرارية الموقع")
                    ,"(https://www.buymecoffee.com) [إضغط لاستمرار دعم المنصه 👈]"

   unsafe_allow_html=True,
)
st.divider()
st.caption("مساحه إعلانيه / إعلان ممول")
st.info("مذكرات وملازم للبكالوريا الشامله متاحه الآن ..إضغط هنا للتفاصيل.")
st.title("🎒مساعد البكالوريا: البرمجه والثقافه المالية")
st.write(
  "أنا معلمك الذكي أساعدك في حل تدريبات البرمجه والثقافه الماليه!"
)
if not api_key:
    st.warning("⚠️ يرجى إدخال مفتاح Gemini API في القائمة الجانبية للبدء.")
    st.stop()

# 4. إعداد الذكاء الاصطناعي
client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTIONS = """
أنت معلم خبير ومحفز لطلاب مرحلة البكالوريا، متخصص في مادتين:
1. البرمجة (Programming).
2. والثقافة المالية (Financial Literacy).

- في البرمجة: لا تعطِ الطالب كود الحل النهائي مباشرة. اشرح له الخطأ برمجياً واطرح أسئلة توجيهية تساعده على اكتشاف الحل بنفسه.
- في الثقافة المالية: اشرح المفاهيم بأمثلة واقعية وبسيطة، وحل المسائل خطوة بخطوة.
- أسلوبك مشجع، واضح، وباللغة العربية المبسطة.
"""

# 5. إدارة المحادثة والرسائل
if "messages" not in st.session_state:
    st.session_state.messages = []

# نظام عداد الأسئلة لإظهار الإعلان بعد كل 3 أسئلة
if "question_count" not in st.session_state:
    st.session_state.question_count = 0# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. استقبال مدخلات الطالب
if prompt := st.chat_input(
    "اكتب سؤالك البرمجي أو المالي هنا (سيظهر إعلان بعد كل 3 أسئلة)..."
):

    # فحص ما إذا حان وقت ظهور الإعلان (بعد كل 3 أسئلة)
  if st.session_state.question_count > 0 and st.session_state.question_count % 3 == 0:
        ad_placeholder = st.empty()
        with ad_placeholder.container():
            st.warning(
                "📢 *إعلان تجاري مهم:* يرجى الانتظار قليلاً لدعم استمرار الموقع مجاناً..."
            )
            # محاكاة إعلان لمدة 30 ثانية
            progress_bar = st.progress(0)
            status_text = st.empty()

            for seconds_left in range(30, 0, -1):
                status_text.text(
                    f"الإعلان سينتهي خلال {seconds_left} ثانية..."
                )
              progress_bar.progress((30 - seconds_left) / 30)
                time.sleep(1)

            status_text.success("شكراً لك! يمكنك المتابعة الآن.")
            time.sleep(1.5)
            ad_placeholder.empty()

    # تسجيل وإرسال السؤال للذكاء الاصطناعي
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.question_count += 1

    with st.chat_message("user"):
        st.markdown(prompt)
      with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTIONS,
                    temperature=0.3,
                ),
            )
            bot_reply = response.text
            st.markdown(bot_reply)
            st.session_state.messages.append(
                {"role": "assistant", "content": bot_reply}
              )
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
      
